from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
import uvicorn
from app.routers import api, account
from app.utils import aunth

app = FastAPI()
app.include_router(api.router)
app.include_router(account.router)
app.include_router(aunth.router)




if __name__ == "__main__":
    uvicorn.run(app)