from fastapi import FastAPI, Request, Depends, Form, HTTPException
from typing import Union
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from connection import Base, engine, sess_db
from sqlalchemy.orm import Session

from app.user.models import UserModel
from app.user.repositoryuser import UserRepository
from app.user.scurity import get_password_hash, create_access_token

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


#db engin
Base.metadata.create_all(bind=engine)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/pricing")
async def pricing(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})


@app.get("/faq")
async def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})


@app.get("/user/signin")
async def signin(req: Request):
    return templates.TemplateResponse("/signin.html", {"request": req})


@app.get("/user/signup")
async def signup(req: Request):
    return templates.TemplateResponse("/signup.html", {"request": req})


@app.post("/signupuser")
async def signup_user(db: Session = Depends(sess_db),
                      username: str = Form(default=""),
                      email: str = Form(default=""),
                      password: str = Form(default="")):

    userRepository = UserRepository(db)
    # Схожость имен в базе
    db_user = userRepository.get_user_by_username(username)
    if db_user:
        return "username is not valid"

    signup = UserModel(email=email, username=username, password=get_password_hash(password))
    success = userRepository.create_user(signup)
    token = create_access_token(signup)
    print(token)

    if success:
        return "create user successfully"
    else:
        raise HTTPException(
            status_code=401,
            detail="Credentials not correct"
        )



