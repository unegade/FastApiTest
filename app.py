from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from starlette.responses import Response, PlainTextResponse, JSONResponse
from starlette.requests import Request
from data_models import PutData
from logger import logger
import uvicorn
import settings


app = FastAPI(title="BFS put message", version="1.0")


@app.post("/put",
    summary="Добавить данные",
    description = "Функция добавляет данные")
async def read_root(data: PutData, request: Request):
    return JSONResponse(status_code=200, content='success')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    a = request.json()
    logger.debug(f'{request.client.host}')
    response : Response = await call_next(request)
    logger.debug(f'{response.status_code}')
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    logger.error(f'{request.url} {str(exc)}')
    return PlainTextResponse(str(exc), status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)