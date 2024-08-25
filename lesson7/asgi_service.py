from aiohttp import web


async def hello_world(request):
    return web.json_response({'message': 'hello world'})

app = web.Application()
app.router.add_get('/', hello_world)


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8001)
