from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import CVE
from db import get_db
from crud import get_all_items, create_item, get_item


app = FastAPI()


@app.get("/items/")
async def read_items(db: AsyncSession = Depends(get_db)):
    return await get_all_items(db)


@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_item(item_id, db)
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items/")
async def add_item(cve: CVE, db: AsyncSession = Depends(get_db)):
    return await create_item(cve, db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
