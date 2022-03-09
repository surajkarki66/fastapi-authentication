from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, auth


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router, tags=["Post"], prefix="/posts")
app.include_router(auth.router, tags=["Auth"], prefix="/auth")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome! FastAPI Authentication"}
