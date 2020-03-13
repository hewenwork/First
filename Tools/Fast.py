import os
import aiofiles
from uvicorn import run
from fastapi import FastAPI, Response
from socket import gethostbyname, gethostname


app = FastAPI()
file_dir = os.path.dirname(__file__)
cloud_dir = r"\\192.168.1.254\部门共享\TEST\Hw贺文\Get&Post"


@app.get("/{model}/{path}")
async def root(path: str, model: str):
    file_path_true = os.path.join(file_dir, path)
    if os.path.exists(file_path_true) is False:
        file_path_true = os.path.join(cloud_dir, path)
    async with aiofiles.open(file_path_true, "rb")as file:
        content = await file.read()
    return Response(content=content, status_code=200)


@app.post("/{model}/{path}")
async def test(path: str, model: str):
    file_path_true = os.path.join(file_dir, path)
    if os.path.exists(file_path_true) is False:
        file_path_true = os.path.join(cloud_dir, path)
    async with aiofiles.open(file_path_true, "rb")as file:
        content = await file.read()
    return Response(content=content, status_code=200)


@app.get("/{model}/{model1}/{path}")
async def do_get_2(model: str, model1: str, path: str):
    file_path = os.path.join(file_dir, path)
    if os.path.exists(file_path) is False:
        file_path = os.path.join(cloud_dir, path)
    async with aiofiles.open(file_path, "rb")as file:
        content = await file.read()
    return Response(content=content, status_code=200)


@app.post("/{model}/{model1}/{path}")
async def do_post_2(model: str, model1: str, path: str):
    file_path = os.path.join(file_dir, path)
    if os.path.exists(file_path) is False:
        file_path = os.path.join(cloud_dir, path)
    async with aiofiles.open(file_path, "rb")as file:
        content = await file.read()
    return Response(content=content, status_code=200)


if __name__ == "__main__":
    option = {
        "port": 80,
        "host": gethostbyname(gethostname())
    }
    run(app, **option)
