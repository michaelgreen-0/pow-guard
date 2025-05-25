import aiohttp
from fastapi import Request
from yarl import URL
from ..env import BACKEND_URL


async def forward_request(request: Request):
    """Forwards request to backend and returns content
    - Given a request
        1. Forms the full backend URL given the env variable
        2. Includes the path and query params in the request url
        3. Removes the host header (as we are not after the guard host)
        4. Sends the request to the desired backend service
        5. Waits and returns the response as a tuple
    """
    url = str(
        URL(BACKEND_URL).with_path(request.url.path).with_query(request.url.query)
    )
    headers = dict(request.headers)
    headers.pop("host", None)

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method, url=url, headers=headers, data=await request.body()
        ) as resp:
            content = await resp.read()
            return resp.status, content, dict(resp.headers)
