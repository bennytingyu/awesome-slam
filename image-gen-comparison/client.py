"""Model API clients for text-to-image generation.

This module exposes a single high-level entrypoint per model that accepts a
text prompt and returns PNG image bytes.
"""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any


class MissingAPIKeyError(RuntimeError):
    """Raised when a required provider API key is missing."""


@dataclass(slots=True)
class ImageGenerationClient:
    """Unified client used by the UI and scripts for model calls."""

    gemini_model: str = "gemini-3-pro-image-generation-preview"
    gpt_model: str = "gpt-image-2"

    def __post_init__(self) -> None:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not gemini_api_key:
            raise MissingAPIKeyError(
                "GEMINI_API_KEY is not set. Export it before running this app."
            )
        if not openai_api_key:
            raise MissingAPIKeyError(
                "OPENAI_API_KEY is not set. Export it before running this app."
            )

        from google import genai
        from openai import OpenAI

        self._gemini = genai.Client(api_key=gemini_api_key)
        self._openai = OpenAI(api_key=openai_api_key)

    @staticmethod
    def _extract_gemini_image_bytes(response: Any) -> bytes:
        candidates = getattr(response, "candidates", None)
        if not candidates:
            raise RuntimeError("Gemini response contained no candidates.")

        first_candidate = candidates[0]
        content = getattr(first_candidate, "content", None)
        parts = getattr(content, "parts", None) if content else None
        if not parts:
            raise RuntimeError("Gemini response contained no content parts.")

        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            data = getattr(inline_data, "data", None) if inline_data else None
            if data:
                return data

        raise RuntimeError("Gemini returned no image bytes in response.")

    @staticmethod
    def _extract_gpt_image_bytes(result: Any) -> bytes:
        data_items = getattr(result, "data", None)
        if not data_items:
            raise RuntimeError("GPT Image API returned no data entries.")

        b64_payload = getattr(data_items[0], "b64_json", None)
        if not b64_payload:
            raise RuntimeError("GPT Image API returned no b64 image data.")

        try:
            return base64.b64decode(b64_payload)
        except Exception as exc:  # pragma: no cover - defensive error wrapping
            raise RuntimeError("GPT Image API returned invalid base64 image data.") from exc

    def generate_with_gemini(self, prompt: str) -> bytes:
        """Generate an image from text using Gemini image generation."""
        from google.genai import types

        response = self._gemini.models.generate_content(
            model=self.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
        return self._extract_gemini_image_bytes(response)

    def generate_with_gpt_image2(self, prompt: str) -> bytes:
        """Generate an image from text using GPT Image API."""
        result = self._openai.images.generate(
            model=self.gpt_model,
            prompt=prompt,
            size="1024x1024",
        )
        return self._extract_gpt_image_bytes(result)
