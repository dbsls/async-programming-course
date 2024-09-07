from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import CVES as cve_model
from schemas import CVE as cve_schema


async def get_all_items(db: AsyncSession):
    result = await db.execute(select(cve_model))
    return result.scalars().all()


async def create_item(request: cve_schema, db: AsyncSession, commit: bool = True):
    create_data = request.model_dump(exclude_unset=True)
    new_example = cve_model(**create_data)
    db.add(new_example)
    if commit:
        await db.commit()
        await db.refresh(new_example)
    return new_example


async def get_item(item_id: int, db: AsyncSession):
    result = await db.execute(select(cve_model).filter(cve_model.id == item_id))
    example = result.scalars().first()
    if not example:
        raise ValueError(f"Item with the id {item_id} not found")
    return example
