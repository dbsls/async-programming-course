import uvicorn
from blacksheep import Application, get

app = Application()


@get("/")
async def hello_world(request):
    return {"message": "hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
