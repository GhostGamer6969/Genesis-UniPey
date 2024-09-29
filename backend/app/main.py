from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="UniPe",
    description="This is the authentication server for UniPe. This will be used in all the UniPe services to authenticate the users.",
    version="1.0.0"
)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}
