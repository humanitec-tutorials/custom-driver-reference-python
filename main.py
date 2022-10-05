from fastapi import FastAPI

from app.api import router as api_router
from app.pydantic_models import Health

APPNAME = 'reference-driver'
VERSION = '0.0.0'
fastapi = FastAPI(
    description="""This is a **reference** implementation of a custom *Driver* for Humanitec.
It operates similarly to the Built-in AWS driver, deploying new S3 buckets on-demand.
test-2
To test it out, you'll need to deploy it as a public facing webserver, and then register it via the Humanitec API.
To learn more about registering drivers checkout the [documentation](https://docs.humanitec.com/integrations/create-own-resource-driver).
    """,
    version="0.0.0",
    title="Humanitec Reference Driver",
    contact={"email": "you@your-company.com"},
    license={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/docs/spec.json",
    redoc_url="/docs",
    docs_url=None)
fastapi.include_router(api_router, prefix="/s3")


@fastapi.get("/alive", response_model=str)
def is_alive():
    return f"{APPNAME} {VERSION}"


@fastapi.get("/health", response_model=Health)
def status():
    return Health(app=APPNAME, version=VERSION, status="OK")
