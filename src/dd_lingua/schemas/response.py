from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from dd_lingua.utils.info import service_info


class ModelAnnotation(BaseModel):
    """Generic annotation object"""

    model_name: Optional[str] = Field(service_info.title, description="Name of the model that created the annotation")
    model_version: Optional[str] = Field(service_info.version, description="Version of the model that created the annotation")

    model_config = ConfigDict(protected_namespaces=())


class LanguageDetection(ModelAnnotation):
    """Language annotation object"""

    language: str = Field(..., description="Language of the text")
    offset: Optional[int] = Field(None, description="Offset of the text")
    length: Optional[int] = Field(None, description="Length of the text")
    conf: Optional[float] = Field(None, description="Confidence of the prediction")


class SimplifiedMultlilingualDetection(ModelAnnotation):
    """Language annotation object"""

    languages: list[str] = Field(..., description="List of languages detected in the text")
