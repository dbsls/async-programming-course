from datetime import datetime
from pydantic import BaseModel, field_validator


class CVE(BaseModel):
    cve_id: str
    published_date: datetime | None = None
    updated_date: datetime | None = None
    title: str | None = None
    description: str | None = None
    problem_type: str | None = None

    @field_validator("published_date", "updated_date")
    def parse_date(cls, value):
        if value:
            return value.replace(tzinfo=None)
