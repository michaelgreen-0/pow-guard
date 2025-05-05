import aiohttp
from config import BACKEND_URL

async def forward_request(request):
    # Convert headers to a regular string-key dictionary
    headers = {k.decode(): v.decode() for k, v in request.headers.raw}

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method,
            url=f"{BACKEND_URL}{request.url.path}",
            headers=headers,
            data=await request.body()
        ) as resp:
            content = await resp.read()
            return resp.status, content, resp.headers