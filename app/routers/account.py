from fastapi import APIRouter, Depends, Request, Cookie
from app.utils.aunth import User, Token, get_current_user, get_current_active_user, login_for_access_token
from app.config import templates


router = APIRouter()


@router.get("/sign-up")
async def sign_up(request: Request):
    return templates.TemplateResponse("registration.html", context={"request": request})


@router.get("/my", response_model=User)
async def my_page(request: Request, ads_id: str | None = Cookie(default=None)):#, current_user: User = Depends(get_current_active_user)):
    print(ads_id)
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request})


@router.post("/my")
async def my_page(request: Request, current_user: Token = Depends(login_for_access_token)):
    return templates.TemplateResponse("personal_cabinet.html", context={"request": request, "user": await get_current_user(token=current_user["access_token"])}, headers={"Authorization": f'''Bearer {current_user["access_token"]}'''})


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]