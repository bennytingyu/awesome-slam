from __future__ import annotations

import base64
from types import SimpleNamespace

import pytest

from client import ImageGenerationClient


def test_extract_gemini_image_bytes_success() -> None:
    response = SimpleNamespace(
        candidates=[
            SimpleNamespace(
                content=SimpleNamespace(
                    parts=[SimpleNamespace(inline_data=SimpleNamespace(data=b"img-bytes"))]
                )
            )
        ]
    )

    assert ImageGenerationClient._extract_gemini_image_bytes(response) == b"img-bytes"


def test_extract_gemini_image_bytes_missing_data_raises() -> None:
    response = SimpleNamespace(candidates=[SimpleNamespace(content=SimpleNamespace(parts=[]))])

    with pytest.raises(RuntimeError, match="no content parts"):
        ImageGenerationClient._extract_gemini_image_bytes(response)


def test_extract_gpt_image_bytes_success() -> None:
    encoded = base64.b64encode(b"png-data").decode("utf-8")
    result = SimpleNamespace(data=[SimpleNamespace(b64_json=encoded)])

    assert ImageGenerationClient._extract_gpt_image_bytes(result) == b"png-data"


def test_extract_gpt_image_bytes_missing_payload_raises() -> None:
    result = SimpleNamespace(data=[SimpleNamespace(b64_json=None)])

    with pytest.raises(RuntimeError, match="no b64 image data"):
        ImageGenerationClient._extract_gpt_image_bytes(result)
