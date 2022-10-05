from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ValuesSecrets(BaseModel):
    Values: Dict[str, object] = Field(alias='values', default={})
    Secrets: Dict[str, object] = Field(alias='secrets', default={})


class ResourceCookie(BaseModel):
    GUResID: Optional[str] = Field(alias='id')
    Type: Optional[str] = Field(alias='type')
    CreatedAt: Optional[datetime] = Field(alias='created_at')
    Region: Optional[str] = Field(alias='region')
    HostedZoneID: Optional[str] = Field(alias='hosted_zone_id')
    AWSAccessKeyID: Optional[str] = Field(alias='aws_access_key_id')
    AWSAccessSecret: Optional[str] = Field(alias='aws_secret_access_key')
    Resource: Optional[ValuesSecrets] = Field(alias='resource', default=ValuesSecrets())

    class Config:
        orm_mode = True


class DriverInputs(BaseModel):
    Type: str = Field(alias='type')
    Resource: Dict[str, object] = Field(alias='resource')
    Driver: Optional[ValuesSecrets] = Field(alias='driver')


class DriverOutputs(BaseModel):
    GUResID: str = Field(alias='id')
    Type: str = Field(alias='type')
    Resource: ValuesSecrets = Field(alias='resource', default=ValuesSecrets())
    Manifests: List["Manifest"] = Field(alias='manifests', default=[])


class Manifest(BaseModel):
    Location: str = Field(alias='location')
    Data: object = Field(alias='data')
