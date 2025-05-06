import aiohttp
from fastapi import Request
from yarl import URL
from env import BACKEND_URL

async def forward_request(request: Request):
    # Build the complete target URL
    url = str(URL(BACKEND_URL).with_path(request.url.path).with_query(request.url.query))

    # Clean headers: use dict directly and remove Host
    headers = dict(request.headers)
    headers.pop("host", None)

    # Forward the request
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method,
            url=url,
            headers=headers,
            data=await request.body()
        ) as resp:
            content = await resp.read()
            return resp.status, content, dict(resp.headers)
