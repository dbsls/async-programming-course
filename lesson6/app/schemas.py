from datetime import datetime
from pytz import timezone as tz

from pydantic import BaseModel, field_validator


class Descriptions(BaseModel):
    lang: str
    description: str
    type: str | None = None


class ProblemTypes(BaseModel):
    descriptions: list[Descriptions]


class CVECNA(BaseModel):
    problemTypes: list[ProblemTypes] | None = []
    title: str | None = None


class CVEContainers(BaseModel):
    cna: CVECNA


class CVEMetadata(BaseModel):
    cveId: str
    datePublished: datetime | None = None
    dateUpdated: datetime | None = None

    @field_validator("datePublished", "dateUpdated")
    def parse_date(cls, value):
        if value:
            return value.replace(tzinfo=None)


class CVESFile(BaseModel):
    cveMetadata: CVEMetadata
    containers: CVEContainers
