from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote

from pow import generate_challenge, verify_pow
from session import save_challenge, get_challenge, mark_verified, is_verified
from proxy import forward_request
from config import POW_DIFFICULTY

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/pow", response_class=HTMLResponse)
async def get_pow(request: Request, next: str = "/"):
    ip = request.client.host
    challenge = generate_challenge()
    save_challenge(ip, challenge)
    return templates.TemplateResponse("pow.html", {
        "request": request,
        "challenge": challenge,
        "difficulty": POW_DIFFICULTY,
        "next": next
    })

@app.post("/pow")
async def submit_pow(request: Request):
    ip = request.client.host
    data = await request.json()
    challenge = get_challenge(ip)
    if not challenge:
        raise HTTPException(status_code=400, detail="Challenge expired or not found")

    solution = data.get("solution")
    if not verify_pow(challenge, solution, POW_DIFFICULTY):
        raise HTTPException(status_code=403, detail="Invalid proof of work")

    mark_verified(ip)
    return {"status": "verified"}

@app.middleware("http")
async def verify_middleware(request: Request, call_next):
    if request.url.path.startswith("/pow") or request.url.path.startswith("/static"):
        return await call_next(request)

    ip = request.client.host
    if not is_verified(ip):
        next_url = quote(str(request.url.path))
        return RedirectResponse(url=f"/pow?next={next_url}")

    status, content, headers = await forward_request(request)
    return JSONResponse(content=content.decode(), status_code=status)