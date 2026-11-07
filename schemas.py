
from pydantic import BaseModel, Field
from typing import Literal


class Sentiment(BaseModel):
    label: Literal["positive", "negative", "neutral"]

    confidence: float = Field(
        ge=0,
        le=1,
        description="Model-estimated confidence from 0 to 1"
    )


class TextAnalysis(BaseModel):
    summary: str = Field(
        description="A concise summary of the input text"
    )

    sentiment: Sentiment

    keywords: list[str] = Field(
        description="Important keywords extracted from the text"
    )

    topics: list[str] = Field(
        description="Main topics discussed in the text"
    )

    category: str = Field(
        description="The primary category of the input text"
    )
