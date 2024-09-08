from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .db import CVES as cve_model
from .schemas import CVE as cve_schema


async def create_item(request: cve_schema, db: AsyncSession, commit: bool = True):
    create_data = request.model_dump(exclude_unset=True)
    new_example = cve_model(**create_data)
    db.add(new_example)
    if commit:
        await db.commit()
        await db.refresh(new_example)
    return new_example


async def get_item(item_id: str, db: AsyncSession):
    result = await db.execute(select(cve_model).filter(cve_model.cve_id == item_id))
    example = result.scalars().first()
    if not example:
        raise ValueError(f"Item with the id {item_id} not found")
    return example


async def get_items_by_date_or_description(
    start_date: Optional[date],
    end_date: Optional[date],
    description: Optional[str],
    offset: int,
    limit: int,
    db: AsyncSession
):
    query = select(cve_model)
    if start_date and end_date:
        query = query.where(cve_model.published_date >= start_date, cve_model.published_date <= end_date)
    if description:
        query = query.where(cve_model.description.ilike(f"%{description}%"))
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
