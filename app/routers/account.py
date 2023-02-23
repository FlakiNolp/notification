from fastapi import APIRouter, Depends, Request, Header, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from app.utils.aunth import decode_access_token, decode_email_token
from app.config import templates
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.utils.db_utils import get_user_by_id, check_email, new_user
from app.utils.utils import send_token_email, get_hash


router = APIRouter()


@router.get("/log-in")
async def sign_up(request: Request):
    return templates.TemplateResponse("log-in.html", context={"request": request})


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse("sign-up.html", context={"request": request})


@router.post("/sign-up")
async def sign_up(background_tasks: BackgroundTasks, request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if check_email(form_data.username, db):
        background_tasks.add_task(send_token_email, email=form_data.username, password=get_hash(form_data.password))
        return templates.TemplateResponse("sign-up.html", context={"request": request})


@router.get("/me")
async def my_page(request: Request):
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request})


@router.post("/me")
async def my_page(Authorization: str = Header(), db: Session = Depends(get_db)):
    id = decode_access_token(Authorization[7:])
    user = get_user_by_id(id, db)
    return user


@router.get("/registration")
async def registration(email_token: str = Query(), db: Session = Depends(get_db)):
    data = decode_email_token(email_token)
    new_user(data[0], data[1], db)
    return RedirectResponse("http://127.0.0.1:1002/log-in")


