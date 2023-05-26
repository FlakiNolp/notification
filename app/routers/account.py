from fastapi import APIRouter, Depends, Request, Header, BackgroundTasks, Query, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, Response, JSONResponse, FileResponse
from app.utils.auth import decode_access_token, decode_registration_token
from app.config import templates, HOST_DOMAIN
from sqlalchemy.orm import Session
from app.database.connection import DataBase
import app.utils.db_utils as db_utils
from app.utils.utils import send_token_email, get_hash, send_token_update_password

router = APIRouter()

database = DataBase()
database._create_schema()


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(f"home-page.html", context={"request": request, "host": HOST_DOMAIN})


@router.get("/log-in")
async def log_in(request: Request):
    return templates.TemplateResponse("log-in.html", context={"request": request, "host": HOST_DOMAIN})


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse("sign-up.html", context={"request": request, "host": HOST_DOMAIN})


@router.post("/sign-up")
async def sign_up(background_tasks: BackgroundTasks, request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                  db: Session = Depends(database._get_db)):
    if db_utils.check_email(form_data.username, db):
        background_tasks.add_task(send_token_email, email=form_data.username, password=get_hash(form_data.password))
        return templates.TemplateResponse("sign-up.html", context={"request": request, "host": HOST_DOMAIN})


@router.get("/me")
async def my_page(request: Request):
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request, "host": HOST_DOMAIN})


@router.post("/me")
async def my_page(Authorization: str = Header(),
                  db: Session = Depends(database._get_db)):
    id = decode_access_token(Authorization[7:])
    user = db_utils.get_services_by_id(id, db)
    return user


@router.get("/registration")
async def registration(token: str = Query(),
                       db: Session = Depends(database._get_db)):
    data = decode_registration_token(token)
    db_utils.new_user(data[0], data[1], db)
    return RedirectResponse(f"http://{HOST_DOMAIN}/log-in")


@router.post("/me/update-services")
async def services(background_tasks: BackgroundTasks,
                   email: str = Form(default=None, media_type="application/x-www-form-urlencoded"),
                   telegram_id: int = Form(default=None, media_type="application/x-www-form-urlencoded"),
                   vk_domain: str = Form(default=None, media_type="application/x-www-form-urlencoded"),
                   website: str = Form(default=None, media_type="application/x-www-form-urlencoded"),
                   Authorization: str = Header(),
                   db: Session = Depends(database._get_db)):
    user_id = decode_access_token(Authorization[7:])
    if user_id:
        background_tasks.add_task(db_utils.edit_services, db, user_id, email, telegram_id, vk_domain, website)
        return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get("/me/reset-api-token")
async def post_update_api_token(Authorization: str = Header(),
                                db: Session = Depends(database._get_db)):
    user_id = decode_access_token(Authorization[7:])
    api_token = db_utils.update_api_token(db, user_id)
    return JSONResponse(content={"api_token": api_token}, status_code=status.HTTP_200_OK)


@router.get("/reset-password")
async def reset_password_page(request: Request):
    return templates.TemplateResponse("reset_password_email", context={"request": request})


@router.get("/me/update-password")
async def update_password(background_tasks: BackgroundTasks,
                          Authorization: str = Header(),
                          db: Session = Depends(database._get_db)):
    user_id = decode_access_token(Authorization[7:])
    background_tasks.add_task(send_token_update_password, db, user_id)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/me/new-password")
async def new_password(request: Request,
                       token: str = Query()):
    decode_access_token(token)
    return templates.TemplateResponse("reset_password.html", context={"request": request, "host": HOST_DOMAIN})


@router.post("/me/reset-password")
async def post_reset_password(background_tasks: BackgroundTasks,
                              password: str = Form(media_type="application/x-www-form-urlencoded"),
                              Authorization: str = Header(),
                              db: Session = Depends(database._get_db)):
    user_id = decode_access_token(Authorization)
    background_tasks.add_task(db_utils.reset_password, db, user_id, password)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/help/{path}")
async def help_path(path: str):
    return FileResponse(f'/usr/src/app/templates/help/{path}')


@router.get("/help/{path}/{filename}")
async def help_path_filename(path: str, filename: str):
    return FileResponse(f'/usr/src/app/templates/help/{path}/{filename}')


@router.get("/help/{path1}/{path2}/{path3}/{filename}")
async def help_path_filename(path1: str, path2: str, path3: str, filename: str):
    return FileResponse(f'/usr/src/app/templates/help/{path1}/{path2}/{path3}/{filename}')
