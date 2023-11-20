from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ModelAnnotation(BaseModel):
    """Generic annotation object"""

    model_name: Optional[str] = Field(None, description="Name of the model that created the annotation")
    model_version: Optional[str] = Field(None, description="Version of the model that created the annotation")

    model_config = ConfigDict(protected_namespaces=())


class LanguageDetection(ModelAnnotation):
    """Language annotation object"""

    language: str = Field(..., description="Language of the text")
    offset: Optional[int] = Field(None, description="Offset of the text")
    length: Optional[int] = Field(None, description="Length of the text")
    conf: Optional[float] = Field(None, description="Confidence of the prediction")
