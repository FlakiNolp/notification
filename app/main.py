from fastapi import FastAPI
import uvicorn
from app.routers import account



app = FastAPI()
app.include_router(account.router)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1002)