from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from api.routers import api


app = FastAPI()
app.include_router(api.router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.on_event("startup")
async def startup():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1001)