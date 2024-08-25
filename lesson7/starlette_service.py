import uvicorn

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def hello_world(request):
    return JSONResponse({'message': 'hello world'})

app = Starlette(debug=True, routes=[
    Route('/', hello_world),
])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
