from fastapi import FastAPI, Request, Depends, Form, HTTPException
from starlette.responses import RedirectResponse, Response
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend.config.connection import Base, engine, sess_db
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware  # Подготовка REACT

from backend.apps.user.models import UserModel
from backend.apps.auth.repositoryuser import UserRepository, SendEmailVerify
from backend.apps.auth.scurity import get_password_hash, create_access_token, verify_token, verify_password, COOKIE_NAME

templates = Jinja2Templates(directory="templates")
admin = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Подготовка REACT
app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    allow_origins=["http://localhost:3000"]
)

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


@app.post("/signinuser")
async def signin_user(response: Response, db: Session = Depends(sess_db), username: str = Form(default=""), password: str = Form(default="")):
    print(username)
    print(password)
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "Username or password is not valid"
    if verify_password(password, db_user.password):
        token = create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return {COOKIE_NAME: token, "token_type": "@~sc%WnNfMbi{o2d3q#wM@rOac@1*"}


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
    SendEmailVerify.sendVerify(token)

    if success:
        return "create user successfully"
    else:
        raise HTTPException(
            status_code=401,
            detail="Credentials not correct"
        )


@app.get('/user/verify/{token}')
async def verify_user(token, db: Session = Depends(sess_db)):
    userRepository = UserRepository(db)
    payload = verify_token(token)
    username = payload.get("username")
    db_user = userRepository.get_user_by_username(username)

    if not username:
        raise HTTPException(
            status_code=401, detail="Credentails not correct"
        )
    if db_user.is_active == True:
        return "Your account has been allreay activeed"
    db_user.is_active = True
    db.commit()
    response = RedirectResponse(url="/user/signi")
    return response


@app.get("/pageadmin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})