from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()


# Define a Pydantic model for request body
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
