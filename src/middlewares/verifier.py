from fastapi import Request
from fastapi.responses import RedirectResponse, Response
from urllib.parse import quote
from ..proxy.forwarder import forward_request
from ..services.verifier import Verifier
from ..utils.redis import get_redis


async def verify_pow_middleware(request: Request, call_next):
    if request.url.path.startswith("/pow") or request.url.path.startswith("/static"):
        return await call_next(request)

    redis = get_redis()
    ip = request.client.host
    verifier = Verifier(redis, ip)

    if not verifier.is_verified():
        next_url = quote(str(request.url.path))
        return RedirectResponse(url=f"/pow?next={next_url}")

    status, content, headers = await forward_request(request)
    content_type = headers.get("content-type", "text/plain")
    return Response(content=content, status_code=status, media_type=content_type)
