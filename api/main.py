from fastapi import FastAPI
import uvicorn

from api import routers


app = FastAPI()
app.include_router(routers.router)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.70", port=1001)