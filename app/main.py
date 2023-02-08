from fastapi import FastAPI
import uvicorn
from app.routers import api, account
from app.utils import aunth


app = FastAPI()
app.include_router(api.router)
app.include_router(account.router)
app.include_router(aunth.router)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app)