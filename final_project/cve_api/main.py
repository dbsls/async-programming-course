import asyncio
from typing import Optional

from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CVE
from .db import get_db
from .crud import get_items_by_date_or_description, create_item, get_item
from .config import get_settings


app = FastAPI()

semaphore = asyncio.Semaphore(get_settings().concurrent_requests)


async def limit_concurrent_requests(request: Request, call_next):
    async with semaphore:
        response = await call_next(request)
        return response


app.middleware("http")(limit_concurrent_requests)


@app.get("/items/{item_id}")
async def read_item(item_id: str, db: AsyncSession = Depends(get_db)):
    try:
        return await get_item(item_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/search/")
async def search_items(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    description: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    return await get_items_by_date_or_description(start_date, end_date, description, offset, limit, db)


@app.post("/items/")
async def add_item(cve: CVE, db: AsyncSession = Depends(get_db)):
    try:
        existing_item = await get_item(cve.cve_id, db)
        for key, value in cve.model_dump(exclude_unset=True).items():
            setattr(existing_item, key, value)
        await db.commit()
        await db.refresh(existing_item)
        return existing_item
    except ValueError:
        return await create_item(cve, db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
