from pydantic import BaseModel, ConfigDict, Field


class LinguaTextRequest(BaseModel):
    text: str = Field(..., description="Text to embed")
    multilingual: bool = Field(False, description="Whether to detect multiple languages (ie. code-switching)")
    max_chars: int = Field(5_000, description="Maximum number of characters to use for prediction")
    simplified: bool = Field(False, description="Whether to condense multilingual output to an array of languages")
    model_config: ConfigDict = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "他能在多大程度上对此施加影响是很重要的，因为无论结果如何，他都将难脱干系。",
                    "multilingual": False,
                    "max_chars": 5_000,
                    "simplified": False
                }
            ]
        }
    }
