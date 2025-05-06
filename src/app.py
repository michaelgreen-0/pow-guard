from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from middlewares.verifier import verify_pow_middleware
from routes import pow

app = FastAPI()
app.include_router(pow.router)

templates = Jinja2Templates(directory="templates")
app.middleware("http")(verify_pow_middleware)
