import asyncio
import json

from aiohttp import ClientSession, ClientConnectionError

from .schemas import CVESFile, CVEAPISchema
from .config import get_settings


async def fetch_url(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
        
async def run_fetching(url: str) -> tuple:
    print(f"Fetching url: {url}")
    try:
        async with asyncio.timeout(get_settings().fetch_timeout):
            result = await fetch_url(url)
    except asyncio.TimeoutError:
        error_msg = f"Timeout error occurred during fetching: {url}"
        print(error_msg)
        result = error_msg
    except ClientConnectionError as e:
        error_msg = f"Error occurred during fetching: {e}"
        print(error_msg)
        result = error_msg
    return url, result


async def send_post_request(url, payload):
    async with ClientSession() as session:
        async with session.post(url, json=payload, headers={"Content-Type": "application/json"}) as response:
            print(f"Status Code: {response.status}")
            response_content = await response.json()
            print(f"Response Content: {response_content}")
            return response_content


async def process_url(url: str):
    res = await fetch_url(url)
    cve_data = json.loads(res)
    payload = CVEAPISchema.from_file(CVESFile(**cve_data)).model_dump()
    await send_post_request(get_settings().cve_api_endpoint, payload)


async def download_delta_json():
    res = await fetch_url(get_settings().delta_json_url)
    data = json.loads(res)
    tasks = []
    for cve in data.get("new", []):
        url = cve.get("githubLink")
        tasks.append(asyncio.create_task(process_url(url)))
    print(f"Create/Update {len(tasks)} CVEs")
