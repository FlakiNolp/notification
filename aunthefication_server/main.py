from fastapi import FastAPI
import uvicorn
from aunthefication_server import users_routers
from aunthefication_server import aunth


app = FastAPI()
app.include_router(users_routers.router)
app.include_router(aunth.router)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.70", port=1000)