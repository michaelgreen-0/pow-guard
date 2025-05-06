from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.challenger import Challenger
from services.verifier import Verifier
from utils.redis import get_redis
from env import POW_DIFFICULTY

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/pow", response_class=HTMLResponse)
async def get_pow(
    request: Request,
    next: str = Query("/"),
    redis=Depends(get_redis)
):
    client_ip = request.client.host
    challenger = Challenger(redis, client_ip)
    challenge = challenger.generate_challenge()
    challenger.save_challenge(challenge=challenge)
    return templates.TemplateResponse("pow.html", {
        "request": request,
        "challenge": challenge,
        "difficulty": POW_DIFFICULTY,
        "next": next
    })

@router.post("/pow")
async def submit_pow(request: Request, redis=Depends(get_redis)):
    client_ip = request.client.host
    data = await request.json()
    challenger = Challenger(redis, client_ip)
    challenge = challenger.get_challenge()

    if not challenge:
        raise HTTPException(status_code=400, detail="Challenge expired or not found")

    solution = data.get("solution")
    verifier = Verifier(redis, client_ip)
    if not verifier.verify_pow(challenge, solution, POW_DIFFICULTY):
        raise HTTPException(status_code=403, detail="Invalid proof of work")

    verifier.mark_verified()
    return {"status": "verified"}
