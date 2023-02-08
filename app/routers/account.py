from fastapi import APIRouter, Depends, Request, Form
from app.utils.aunth import User, Token, get_current_user, login_for_access_token
from app.config import templates
import app.utils.users as users_utils
from sqlalchemy.orm import Session
from app.models.database import get_db
import requests


router = APIRouter()


@router.get("/log-in")
async def sign_up(request: Request):
    return templates.TemplateResponse("log-in.html", context={"request": request})


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse("sign-up.html", context={"request": request})


@router.post("/sign-up")
async def sign_up(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if users_utils.get_user_by_email(username):
        return False
    else:
        print("ok")


@router.get("/my", response_model=User)
async def my_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request, "user": current_user})


@router.post("/my")
async def my_page(request: Request, current_user: Token = Depends(login_for_access_token)):
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request, "user": current_user}, headers={"Authorization": f'''Bearer {current_user["access_token"]}'''})


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.email}]


@router.get("/test")
async def test(db: Session = Depends(get_db)):
    info = users_utils.get_users(db)
    return info


@router.get("/new_user")
async def test(db: Session = Depends(get_db)):
    info = users_utils.new_user(db)
    return info