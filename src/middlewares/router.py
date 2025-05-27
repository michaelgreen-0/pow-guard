from fastapi import Request
from fastapi.responses import RedirectResponse, Response
from urllib.parse import quote
from ..proxy.forwarder import forward_request
from ..services.verifier import Verifier
from ..utils.redis import get_redis
from ..logger import Logger


async def router_middleware(request: Request, call_next):
    """Middleware for deciding where to route a request as it arrives.
    - If the request is already going for verification (starts with /pow) then continue to pow service
    - we're also not interested in requiring pow verification when serving static files
    - If the request is to another resource then:
        - Check if client is verified
        - If not verified then redirect to /pow service before continuing
        - If verified then forward client through to requested service
    """
    logger = Logger()
    logger.info("Received request. Deciding where to route")
    if request.url.path.startswith("/pow") or request.url.path.startswith("/static"):
        logger.info("Request starts with pow or static. Passing through.")
        return await call_next(request)

    logger.info("Request does not start with pow or static")
    redis = get_redis()
    ip = request.client.host
    verifier = Verifier(redis, ip)

    if not verifier.is_verified():
        logger.info("IP is not verified. Redirecting to pow service.")
        next_url = quote(str(request.url.path))
        return RedirectResponse(url=f"/pow?next={next_url}")

    # NOTE: Headers aren't pulled through. Maybe later we can pull them all through
    # Ran into content length issues with compression...
    logger.info("IP is verified. Proxying to service.")
    status, content, headers = await forward_request(request)
    content_type = headers.get("content-type")
    return Response(content=content, status_code=status, media_type=content_type)
