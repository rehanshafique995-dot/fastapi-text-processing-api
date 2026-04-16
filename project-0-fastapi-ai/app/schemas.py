from pydantic import BaseModel, Field, ConfigDict, field_validator


class SummarizeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, description="Text to summarize")
    max_words: int = Field(80, ge=10, le=300, description="Maximum summary length in words")


class SummarizeLLMOutput(BaseModel):
    summary: str


class SummarizeResponse(BaseModel):
    summary: str
    original_word_count: int
    summary_word_count: int
    provider: str
    model: str


class ClassifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, description="Text to classify")
    labels: list[str] = Field(..., min_length=2, description="Candidate labels")

    @field_validator("labels")
    @classmethod
    def validate_labels(cls, value: list[str]) -> list[str]:
        cleaned = [label.strip() for label in value if label.strip()]
        if len(cleaned) < 2:
            raise ValueError("At least 2 non-empty labels are required.")
        return cleaned


class ClassifyLLMOutput(BaseModel):
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str


class ClassifyResponse(BaseModel):
    label: str
    confidence: float
    reasoning: str
    provider: str
    model: str


class ExtractRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., min_length=1, description="Text to extract data from")
    fields: list[str] = Field(..., min_length=1, description="Fields to extract")

    @field_validator("fields")
    @classmethod
    def validate_fields(cls, value: list[str]) -> list[str]:
        cleaned = [field.strip() for field in value if field.strip()]
        if not cleaned:
            raise ValueError("At least one non-empty field is required.")
        return cleaned


class ExtractLLMOutput(BaseModel):
    extracted_data: dict[str, str]
    missing_fields: list[str] = []


class ExtractResponse(BaseModel):
    extracted_data: dict[str, str]
    missing_fields: list[str]
    provider: str
    model: str