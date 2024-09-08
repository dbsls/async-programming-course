from datetime import datetime
from typing import Self

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


class CVEAPISchema(BaseModel):
    cve_id: str
    published_date: str | None = None
    updated_date: str | None = None
    title: str | None = None
    description: str | None = None
    problem_type: str | None = None

    @classmethod
    def from_file(cls, data: CVESFile) -> Self:
        try:
            desc_section = data.containers.cna.problemTypes[0].descriptions[0]
            desc = desc_section.description
            problem_type = desc_section.type
        except IndexError:
            desc = None
            problem_type = None
        return cls(
            cve_id=data.cveMetadata.cveId,
            published_date=str(data.cveMetadata.datePublished),
            updated_date=str(data.cveMetadata.dateUpdated),
            title=data.containers.cna.title,
            description=desc,
            problem_type=problem_type,
        )
