from fastapi import FastAPI, Response, status
from pydantic import BaseModel

from .logging_config import configure_logging


class EchoRequest(BaseModel):
    message: str


class EchoResponse(BaseModel):
    message: str


configure_logging()
app = FastAPI(title="SSDLCDemo", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/echo", response_model=EchoResponse, status_code=status.HTTP_200_OK)
def echo(payload: EchoRequest, response: Response) -> EchoResponse:
    # Any validation is handled by Pydantic models
    return EchoResponse(message=payload.message) 