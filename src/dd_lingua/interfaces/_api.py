from contextlib import asynccontextmanager

from dd_lingua.core.model import Lingua
from dd_lingua.schemas.request import LinguaTextRequest
from dd_lingua.schemas.response import LanguageDetection, SimplifiedMultlilingualDetection
from dd_lingua.schemas.settings import settings
from dd_lingua.utils.health import ServiceHealthStatus, service_health
from dd_lingua.utils.info import ServiceInfo, service_info
from dd_lingua.utils.logging import logger

try:
    import uvicorn
    from fastapi import FastAPI
except ImportError:
    logger.error("Failed to import uvicorn and/or fastapi. Please install them with `pip install uvicorn fastapi`")
    exit(1)


state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["model"] = Lingua(
        eager_mode=settings.eager_mode,
        low_accuracy=settings.low_accuracy,
        script=settings.script,
        languages=settings.languages
    )
    service_health.status = ServiceHealthStatus.OK
    yield
    state.clear()


app = FastAPI(title=service_info.title, version=service_info.version, description=service_info.description, lifespan=lifespan)


@app.get("/health")
async def health() -> ServiceHealthStatus:
    return service_health.status


@app.get("/info")
async def info() -> ServiceInfo:
    return service_info


@app.post("/inference", response_model_exclude_none=True)
async def infer_image(request: LinguaTextRequest) -> LanguageDetection | list[LanguageDetection] | SimplifiedMultlilingualDetection:
    output =  state["model"].infer(
        text=request.text, 
        multilingual=request.multilingual, 
        max_chars=request.max_chars, 
        simplified=request.simplified
    )
    logger.info(f"Detected language(s) {output}")
    return output


def main():
    uvicorn.run("dd_lingua.interfaces._api:app", host=settings.host, port=settings.port, reload=settings.reload)


if __name__ == "__main__":
    main()
