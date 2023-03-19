from fastapi import APIRouter, Depends, Request, Header, BackgroundTasks, Query, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, Response, JSONResponse
from app.utils.aunth import decode_access_token, decode_registration_token
from app.config import templates
from sqlalchemy.orm import Session
from app.models.database import get_db
import app.utils.db_utils as db_utils
from app.utils.utils import send_token_email, get_hash, send_token_update_password

router = APIRouter()


@router.get("/log-in")
async def sign_up(request: Request):
    return templates.TemplateResponse("log-in.html", context={"request": request})


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse("sign-up.html", context={"request": request})


@router.post("/sign-up")
async def sign_up(background_tasks: BackgroundTasks, request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                  db: Session = Depends(get_db)):
    if db_utils.check_email(form_data.username, db):
        background_tasks.add_task(send_token_email, email=form_data.username, password=get_hash(form_data.password))
        return templates.TemplateResponse("sign-up.html", context={"request": request})


@router.get("/me")
async def my_page(request: Request):
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request})


@router.post("/me")
async def my_page(Authorization: str = Header(),
                  db: Session = Depends(get_db)):
    id = decode_access_token(Authorization[7:])
    user = db_utils.get_services_by_id(id, db)
    return user


@router.get("/registration")
async def registration(token: str = Query(),
                       db: Session = Depends(get_db)):
    data = decode_registration_token(token)
    db_utils.new_user(data[0], data[1], db)
    return RedirectResponse("http://localhost:1002/log-in")


@router.post("/me/services")
async def services(background_tasks: BackgroundTasks,
                   email: str = Form(default=None, media_type="form-data"),
                   telegram_id: int = Form(default=None, media_type="form-data"),
                   vk_domain: str = Form(default=None, media_type="form-data"),
                   website: str = Form(default=None, media_type="form-data"),
                   Authorization: str = Header(),
                   db: Session = Depends(get_db)):
    user_id = decode_access_token(Authorization[7:])
    if user_id:
        background_tasks.add_task(db_utils.edit_services, db, user_id, email, telegram_id, vk_domain, website)
        return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get("/me/reset-api-token")
async def post_update_api_token(Authorization: str = Header(),
                                db: Session = Depends(get_db)):
    user_id = decode_access_token(Authorization[7:])
    api_token = db_utils.update_api_token(db, user_id)
    return JSONResponse(content={"api_token": api_token}, status_code=status.HTTP_200_OK)


@router.get("/me/reset-password")
async def update_password(background_tasks: BackgroundTasks,
                          Authorization: str = Header(),
                          db: Session = Depends(get_db)):
    user_id = decode_access_token(Authorization[7:])
    background_tasks.add_task(send_token_update_password, db, user_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/new-password")
async def new_password(request: Request,
                       token: str = Query()):
    decode_access_token(token)
    return templates.TemplateResponse("reset_password", context={"request": request})


@router.post("/reset-password")
async def post_reset_password(background_tasks: BackgroundTasks,
                              password: str = Form(media_type="x-www-form-urlencoded"),
                              Authorization: str = Header(),
                              db: Session = Depends(get_db)):
    user_id = decode_access_token(Authorization[7:])
    background_tasks.add_task(db_utils.reset_password, db, user_id, password)
    return Response(status_code=status.HTTP_200_OK)
