from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from dd_lingua.core.utils import LinguaSupportedISO639_3, LinguaSupportedISO15924


class Settings(BaseSettings):
    host: str = Field("0.0.0.0", validation_alias="HOST", description="Host to bind to")
    port: int = Field(8080, validation_alias="PORT", description="Port to bind to")
    eager_mode: bool = Field(False, description="Eager mode by default loads all models which can alleviate load times")
    high_accuracy: bool = Field(False, description="High accuracy mode which is slower but more accurate")
    script: Optional[LinguaSupportedISO15924] = Field(None, description="Loads all the language models for that script")
    languages: Optional[list[LinguaSupportedISO639_3]] = Field(None, description="Languages to l the language models for those languages")
    reload: Optional[bool] = Field(True, description="Reload mode")
    log_file: Optional[str] = Field(None, description="File to write logs to if desired")
    log_level: Optional[str] = Field("INFO", validation_alias="LOG_LEVEL", description="Log level")
    model_config = SettingsConfigDict(env_file=".env", protected_namespaces=[])


settings = Settings()
