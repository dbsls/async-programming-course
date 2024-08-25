from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()


class MessageResponse(BaseModel):
    message: str


hello_world_response = MessageResponse(message="hello world")


def get_hello_world_response():
    global hello_world_response
    return hello_world_response


@app.get("/", response_model=MessageResponse)
async def read_root(
        res: Annotated[MessageResponse, Depends(get_hello_world_response)]
) -> MessageResponse:
    return res


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
