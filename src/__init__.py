from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .middlewares.router import router_middleware
from .routes import pow

app = FastAPI()
app.include_router(pow.router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")
app.middleware("http")(router_middleware)
