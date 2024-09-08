import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from .http_client import download_delta_json

from .config import get_settings
from .path_scan import scan


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(schedule_download())
    yield
    task.cancel()


app = FastAPI(**{"lifespan": lifespan})
templates = Jinja2Templates(directory="templates")
semaphore = asyncio.Semaphore(get_settings().concurrent_requests)


async def limit_concurrent_requests(request: Request, call_next):
    async with semaphore:
        response = await call_next(request)
        return response


app.middleware("http")(limit_concurrent_requests)


@app.get("/download-cve")
async def trigger_download_cve():
    path = get_settings().cve_path
    await scan(path)
    return JSONResponse(content={"message": f"Path {path} scanning initiated!"})


@app.get("/download-cve-last-changes")
async def trigger_download_cve_last_changes():
    await download_delta_json()
    return JSONResponse(content={"message": "CVE Last changes download initiated!"})


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def schedule_download():
    while True:
        await download_delta_json()
        await asyncio.sleep(get_settings().schedule_interval)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
