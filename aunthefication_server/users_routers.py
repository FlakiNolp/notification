from fastapi import APIRouter, Depends
import aunthefication_server.utils as users_utils
from aunthefication_server.database import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/email")
async def test(email: str, db: Session = Depends(get_db)):
    return users_utils.get_user_by_email(email=email, db=db)


@router.get("/new_user")
async def test(db: Session = Depends(get_db)):
    info = users_utils.new_user(db)
    return info