from redis import Redis
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import quote

from env import POW_DIFFICULTY, REDIS_HOST, REDIS_PORT
from proxy import forward_request
from services import Challenger, Verifier

app = FastAPI()
templates = Jinja2Templates(directory="templates")
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/pow", response_class=HTMLResponse)
async def get_pow(request: Request, next: str = "/"):
    ip = request.client.host
    challenger = Challenger(redis, ip)
    challenge = challenger.generate_challenge()
    challenger.save_challenge(challenge=challenge)
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
    challenger = Challenger(redis, ip)
    challenge = challenger.get_challenge()
    if not challenge:
        raise HTTPException(status_code=400, detail="Challenge expired or not found")

    solution = data.get("solution")
    verifier = Verifier(redis, ip)
    is_valid_solution = verifier.verify_pow(challenge, solution, POW_DIFFICULTY)
    if not is_valid_solution:
        raise HTTPException(status_code=403, detail="Invalid proof of work")

    verifier.mark_verified()
    return {"status": "verified"}

@app.middleware("http")
async def verify_middleware(request: Request, call_next):
    if request.url.path.startswith("/pow") or request.url.path.startswith("/static"):
        return await call_next(request)

    ip = request.client.host
    verifier = Verifier(redis, ip)
    is_ip_verified = verifier.is_verified()
    if not is_ip_verified:
        next_url = quote(str(request.url.path))
        return RedirectResponse(url=f"/pow?next={next_url}")

    status, content, headers = await forward_request(request)
    return JSONResponse(content=content.decode(), status_code=status)