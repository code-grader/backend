from fastapi import FastAPI
from .utils.http_response import create_response

app = FastAPI()


@app.get("/")
async def read_root():
    return create_response(message="Server is running!")
