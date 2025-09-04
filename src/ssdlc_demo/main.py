from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

from .logging_config import configure_logging
import requests


class EchoRequest(BaseModel):
    message: str


class EchoResponse(BaseModel):
    message: str


configure_logging()
app = FastAPI(title="SSDLCDemo", version="0.1.0")


class AnimeInfo(BaseModel):
    id: int
    name: str
    altName: str | None = None


class CharacterInfo(BaseModel):
    id: int
    name: str


class AnimechanData(BaseModel):
    content: str
    anime: AnimeInfo
    character: CharacterInfo


class AnimechanResponse(BaseModel):
    status: str
    data: AnimechanData


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/echo", response_model=EchoResponse, status_code=status.HTTP_200_OK)
def echo(payload: EchoRequest, response: Response) -> EchoResponse:
    # Any validation is handled by Pydantic models
    return EchoResponse(message=payload.message)


@app.get("/anime/quote", response_model=AnimechanResponse)
def get_random_anime_quote() -> AnimechanResponse:
    """Fetch a random anime quote from Animechan and return it.

    Docs: https://animechan.io/
    Endpoint used: https://api.animechan.io/v1/quotes/random
    """
    try:
        res = requests.get("https://api.animechan.io/v1/quotes/random", timeout=5)
    except requests.RequestException as exc:  # network, DNS, timeout
        raise HTTPException(status_code=502, detail="Upstream Animechan unavailable") from exc

    if res.status_code != 200:
        raise HTTPException(status_code=502, detail="Animechan returned non-200 status")

    try:
        payload = res.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="Invalid JSON from Animechan") from exc

    # Validate and coerce to our response model
    try:
        validated = AnimechanResponse.model_validate(payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unexpected Animechan schema") from exc

    return validated
