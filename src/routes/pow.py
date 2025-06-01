import uuid
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from ..services.challenger import Challenger
from ..services.verifier import Verifier
from ..env import POW_DIFFICULTY, COOKIE_LIFETIME, CHALLENGE_LIFETIME
from ..logger import Logger

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")


@router.get("/pow", response_class=HTMLResponse)
async def get_pow(
    request: Request,
    next: str = Query("/"),
    logger: Logger = Depends(),
):
    logger.info("Received GET request")

    challenge_id = str(uuid.uuid4())
    challenger = Challenger(challenge_id)
    challenge = challenger.generate_challenge()
    challenger.save_challenge(challenge, time=CHALLENGE_LIFETIME)
    logger.info("Generated and saved challenge", extra={"challenge": challenge})

    return templates.TemplateResponse(
        "pow.html",
        {
            "request": request,
            "challenge_id": challenge_id,
            "challenge": challenge,
            "difficulty": POW_DIFFICULTY,
            "next": next,
        },
    )


@router.post("/pow")
async def submit_pow(request: Request, logger: Logger = Depends()):
    logger.info("Client sent POST request to verify challenge")
    data = await request.json()
    challenge_id = data.get("challenge_id")
    solution = data.get("solution")

    challenger = Challenger(challenge_id)
    challenge = challenger.get_challenge()
    challenge_verifier = Verifier(challenge_id)

    if not challenge:
        raise HTTPException(status_code=400, detail="Challenge expired or not found")

    solution_set = {
        "challenge_id": challenge_id,
        "challenge": challenge,
        "solution": solution,
        "difficulty": POW_DIFFICULTY,
    }

    logger.info(
        "Verifying solution against challenge",
        extra=solution_set,
    )

    if not challenge_verifier.verify_pow(challenge, solution, POW_DIFFICULTY):
        logger.info("Incorrect solution", extra=solution_set)
        raise HTTPException(status_code=403, detail="Invalid proof of work")

    logger.info("Solution successfully verified")
    challenge_verifier.mark_verified(time=CHALLENGE_LIFETIME)

    response = JSONResponse(content={"status": "verified"})

    # Setup cookie for session (abstract this out later)
    session_token = uuid.uuid4().hex
    session_verifier = Verifier(session_token)
    session_verifier.mark_verified(time=COOKIE_LIFETIME)

    response.set_cookie(
        key="pow_session_token",
        value=session_token,
        max_age=COOKIE_LIFETIME,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="Lax",
    )
    return response
