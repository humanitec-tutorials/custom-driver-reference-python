from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api import router as api_router

APPNAME = 'reference-driver'
VERSION = '0.0.0'
fastapi = FastAPI(openapi_url="/docs/spec.json", redoc_url="/docs", docs_url=None)
fastapi.include_router(api_router, prefix="")


@fastapi.get("/alive")
def is_alive():
    return f"{APPNAME} {VERSION}"


@fastapi.get("/status")
def is_alive():
    return JSONResponse(
        status_code=200,
        content={
            "app": APPNAME,
            "version": VERSION,
            "status": "OK"
        }
    )
