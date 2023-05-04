from fastapi import FastAPI, Request
from typing import Union
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/pricing")
def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})


@app.get("/faq")
def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})


@app.get("/user/singin")
def login(req: Request):
    return templates.TemplateResponse("/login.html", {"request": req})


@app.get("/user/singup")
def singup(req: Request):
    return templates.TemplateResponse("/singup.html", {"request": req})

