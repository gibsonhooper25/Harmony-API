from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import song, album, playlist, user, discovery
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
HarmonyAPI is the premier ecommerce site for all your musical desires.
"""

app = FastAPI(
    title="HarmonyAPI",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Gibson Hooper",
        "email": "gdhooper@calpoly.edu",
    },
)

origins = ["https://potion-exchange.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(song.router)
app.include_router(album.router)
app.include_router(playlist.router)
app.include_router(user.router)
app.include_router(discovery.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to HarmonyAPI."}
