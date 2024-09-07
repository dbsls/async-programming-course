from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

from config import Settings, get_settings

Base = declarative_base()


class CVES(Base):
    __tablename__ = "cves"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, index=True)
    published_date = Column(DateTime)
    updated_date = Column(DateTime)
    title = Column(String)
    description = Column(String)
    problem_type = Column(String)


def get_engine(settings: Settings):
    return create_async_engine(settings.postgres_dsn)


def get_session_maker(settings: Settings = Depends(get_settings)):
    return sessionmaker(
        bind=get_engine(settings=settings),
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


async def get_db(session_maker=Depends(get_session_maker)) -> AsyncSession:
    async with session_maker() as db:
        try:
            yield db
        finally:
            await db.close()
