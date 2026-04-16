import json
from ollama import Client, ResponseError

from app.config import settings
from app.schemas import (
    SummarizeRequest,
    SummarizeResponse,
    SummarizeLLMOutput,
    ClassifyRequest,
    ClassifyResponse,
    ClassifyLLMOutput,
    ExtractRequest,
    ExtractResponse,
    ExtractLLMOutput,
)


class LLMService:
    def __init__(self) -> None:
        self.client = Client(host=settings.OLLAMA_HOST)
        self.model = settings.OLLAMA_MODEL

    def _get_json_from_model(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response["message"]["content"]
        except ResponseError as exc:
            raise ValueError(f"Ollama error: {exc.error}") from exc
        except Exception as exc:
            raise ValueError(f"Failed to call Ollama: {exc}") from exc

    def _parse_json_output(self, raw_text: str, schema):
        cleaned = raw_text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.removeprefix("```json").strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned.removesuffix("```").strip()

        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            cleaned = cleaned[start:end + 1]

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model did not return valid JSON. Raw output: {raw_text}") from exc

        try:
            return schema.model_validate(data)
        except Exception as exc:
            raise ValueError(f"Model JSON did not match schema. Parsed data: {data}") from exc

    def summarize(self, payload: SummarizeRequest) -> SummarizeResponse:
        system_prompt = (
            "You are a precise summarization assistant. "
            "Return ONLY valid JSON in this exact format: "
            '{"summary":"..."} '
            "Do not add markdown, code fences, or extra text."
        )

        user_prompt = (
            f"Summarize the following text in at most {payload.max_words} words.\n\n"
            f"TEXT:\n{payload.text}"
        )

        raw_output = self._get_json_from_model(system_prompt, user_prompt)
        parsed = self._parse_json_output(raw_output, SummarizeLLMOutput)

        return SummarizeResponse(
            summary=parsed.summary,
            original_word_count=len(payload.text.split()),
            summary_word_count=len(parsed.summary.split()),
            provider="ollama",
            model=self.model,
        )

    def classify(self, payload: ClassifyRequest) -> ClassifyResponse:
        labels_text = ", ".join(payload.labels)

        system_prompt = (
            "You are a careful text classification assistant. "
            "Choose exactly one label from the provided labels. "
            "Return ONLY valid JSON in this exact format: "
            '{"label":"...","confidence":0.0,"reasoning":"..."} '
            "Do not add markdown, code fences, or extra text."
        )

        user_prompt = (
            f"Available labels: {labels_text}\n\n"
            f"Classify the following text into exactly one of those labels.\n"
            f"Confidence must be between 0 and 1.\n\n"
            f"TEXT:\n{payload.text}"
        )

        raw_output = self._get_json_from_model(system_prompt, user_prompt)
        parsed = self._parse_json_output(raw_output, ClassifyLLMOutput)

        if parsed.label not in payload.labels:
            raise ValueError(
                f"Model returned label '{parsed.label}', which is outside the provided labels."
            )

        return ClassifyResponse(
            label=parsed.label,
            confidence=parsed.confidence,
            reasoning=parsed.reasoning,
            provider="ollama",
            model=self.model,
        )

    def extract(self, payload: ExtractRequest) -> ExtractResponse:
        fields_text = ", ".join(payload.fields)

        system_prompt = (
            "You are an information extraction assistant. "
            "Extract only the requested fields from the text. "
            "If a field is missing, include it in missing_fields. "
            "Return ONLY valid JSON in this exact format: "
            '{"extracted_data":{"field":"value"},"missing_fields":["field"]} '
            "Do not add markdown, code fences, or extra text."
        )

        user_prompt = (
            f"Requested fields: {fields_text}\n\n"
            f"Extract the requested fields from the following text.\n\n"
            f"TEXT:\n{payload.text}"
        )

        raw_output = self._get_json_from_model(system_prompt, user_prompt)
        parsed = self._parse_json_output(raw_output, ExtractLLMOutput)

        return ExtractResponse(
            extracted_data=parsed.extracted_data,
            missing_fields=parsed.missing_fields,
            provider="ollama",
            model=self.model,
        )