from fastapi import FastAPI
import uvicorn
from app.routers import api, account


app = FastAPI()
app.include_router(api.router)
app.include_router(account.router)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.70", port=1002)