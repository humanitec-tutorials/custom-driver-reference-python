import binascii
import re
from base64 import b64decode, b64encode
from json import JSONDecodeError
from typing import Tuple, Dict

from pydantic import json, ValidationError

from app.pydantic_models import ResourceCookie


def is_valid_id(GUResID: str) -> bool:
    pattern = re.compile(r"^([a-z\d][a-z\d-]+[a-z\d]$)")
    return pattern.match(GUResID) is not None


def get_credentials(driverSecrets: Dict[str, object]) -> Tuple[str, str]:
    account = driverSecrets['account']
    if not isinstance(account, dict):
        raise ValueError("driver secrets should contain 'account' map")
    if (accessKeyID := account.get('aws_access_key_id')) is None:
        raise ValueError("'account' details should include 'aws_access_key_id'")
    if (secretAccessKey := account.get('aws_secret_access_key')) is None:
        raise ValueError("'account' details should include 'aws_secret_access_key'")
    return accessKeyID, secretAccessKey


def cookie_encode(data: ResourceCookie) -> str:
    jdata = data.json(by_alias=True, exclude_none=True, exclude_unset=True, exclude_defaults=True)
    encoded = b64encode(jdata.encode("utf-8")).decode("utf-8")
    return encoded


def cookie_decode(cookie: str, default: ResourceCookie = None) -> ResourceCookie:
    try:
        jdata = b64decode(cookie.encode("utf-8")).decode("utf-8")
    except binascii.Error:
        raise ValueError("Invalid base64")
    try:
        data = ResourceCookie.parse_raw(jdata)
    except JSONDecodeError:
        raise ValueError("Invalid JSON data")
    except ValidationError:
        raise ValueError("Missing fields")
    if default is None:
        default = ResourceCookie()
    updated_default = default.dict(by_alias=True, exclude_none=True, exclude_unset=True)
    updated_default.update(data.dict(by_alias=True, exclude_none=True, exclude_unset=True))
    return ResourceCookie(**updated_default)
