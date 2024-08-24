from typing import Self

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from schemas import CVESFile

Base = declarative_base()


class CVES(Base):
    __tablename__ = "cves"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, index=True)  # cveId
    published_date = Column(DateTime)  # datePublished
    updated_date = Column(DateTime)  # dateUpdated
    title = Column(String)  # containers.cna.title
    description = Column(String)  # containers.cna.problemTypes.descriptions.description
    problem_type = Column(String)  # containers.cna.problemTypes.descriptions.type

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
            published_date=data.cveMetadata.datePublished,
            updated_date=data.cveMetadata.dateUpdated,
            title=data.containers.cna.title,
            description=desc,
            problem_type=problem_type,
        )
