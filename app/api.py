import binascii
from datetime import datetime
from typing import Union
from uuid import uuid4

from fastapi import APIRouter, Header
from starlette.responses import JSONResponse, Response

from .aws import create_bucket, delete_bucket
from .pydantic_models import DriverInputs, ResourceCookie, DriverOutputs, ValuesSecrets
from .utils import is_valid_id, get_credentials, cookie_decode, cookie_encode

router = APIRouter()


@router.put('/s3/{GUResID:str}',
            responses={'200': {'model': DriverOutputs}, '400': {'model': str}, '422': {'model': str}})
async def upsert_s3(GUResID: str,
                    inputs: DriverInputs,
                    encoded_cookie: Union[str, None] = Header(default=None, alias="Humanitec-Driver-Cookie")):  # todo: custom error on json fail (422, "Unable to process the request")

    if not is_valid_id(GUResID):
        return Response(status_code=400, content="GUResID is not a valid Humanitec ID")

    # Parse and validate request payload
    if inputs.Type != "s3":
        return Response(status_code=422, content="Invalid resource type")

    # Validate AWS access credentials
    region = inputs.Driver.Values.get('region', '')
    try:
        access_key_id, secret_access_key = get_credentials(inputs.Driver.Secrets)
    except ValueError as e:
        return Response(status_code=400, content=e.args)

    # Parse the resource cookie
    cookie = ResourceCookie(CreatedAt=datetime.now())
    if encoded_cookie is not None:
        try:
            cookie = cookie_decode(encoded_cookie, cookie)
        except ValueError as e:
            return Response(status_code=400, content=e.args)

    # Prepare outputs (draft)
    res = DriverOutputs(
        id=GUResID,
        type=inputs.Type,
        resource=cookie.Resource
    )

    bucket_name_uuid = uuid4()
    bucket_name = str(bucket_name_uuid)

    # Provision a new resource
    if cookie.GUResID is None:
        try:
            region = create_bucket(access_key_id, secret_access_key, region, bucket_name)
        except:
            return Response(status_code=400, content="Unable to provision the resource")
        res.Resource = ValuesSecrets(
            values={
                "region": region,
                "bucket": bucket_name
            }
        )
    else:
        pass  # Don't need to handle existing resource for S3 as it's immediately ready meaning this will never be hit

    # Refresh AWS credentials
    res.Resource.Secrets["aws_access_key_id"] = access_key_id
    res.Resource.Secrets["aws_secret_access_key"] = secret_access_key

    # Set/Update the resource cookie
    cookie = ResourceCookie(
        id=res.GUResID,
        type=res.Type,
        created_at=cookie.CreatedAt,
        region=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        resource=res.Resource
    )

    encoded_cookie = cookie_encode(cookie)

    return JSONResponse(res.dict(by_alias=True, exclude_none=True, exclude_unset=True), headers={'Set-Humanitec-Driver-Cookie': encoded_cookie})


@router.delete('/s3/{GUResID:str}',
               responses={'200': {'model': DriverOutputs}, '400': {'model': str}, '422': {'model': str}})
async def delete_s3(GUResID: str,
                    encoded_cookie: Union[str, None] = Header(default=None, alias="Humanitec-Driver-Cookie")):  # todo: custom error on json fail (422, "Unable to process the request")

    if not is_valid_id(GUResID):
        return Response(status_code=400, content="GUResID is not a valid Humanitec ID")

    # Parse the resource cookie
    try:
        cookie = cookie_decode(encoded_cookie)
    except ValueError as e:
        return Response(status_code=400, content=e.args[0])
    if (cookie.GUResID is None) or (cookie.GUResID == '') or (cookie.GUResID != GUResID):
        return Response(status_code=404, content="Not Found")
    if cookie.Type != 's3':
        return Response(status_code=400, content="Invalid resource type")
    if (bucket_name := cookie.Resource.Values.get("bucket", "")) is "":
        return Response(status_code=400, content="Missing bucket name")
    if (aws_access_key_id := cookie.AWSAccessKeyID) is None:
        return Response(status_code=400, content="Missing AWSAccessKeyID")
    if (aws_secret_access_key := cookie.AWSAccessSecret) is None:
        return Response(status_code=400, content="Missing AWSAccessSecret")
    if (region := cookie.Region) is None:
        return Response(status_code=400, content="Missing AWS Region")

    # Delete the resource
    try:
        delete_bucket(aws_access_key_id, aws_secret_access_key, region, bucket_name)
    except ValueError:
        return Response(status_code=400, content=f"Unable to delete the S3 bucket record {bucket_name}")

    return Response(status_code=204, headers={'Set-Humanitec-Driver-Cookie': ''})
