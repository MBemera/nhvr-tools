"""Formatting helpers for tool responses."""

from __future__ import annotations

import json
from typing import Any


def format_response(data: Any, output_format: str) -> str:
    if output_format == "json":
        return json.dumps({"data": data}, indent=2, sort_keys=True)

    return render_markdown(data)


def render_markdown(data: Any, depth: int = 2) -> str:
    if isinstance(data, dict):
        lines = []
        heading = "#" * min(depth, 6)
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{heading} {key}\n{render_markdown(value, depth + 1)}")
            elif isinstance(value, list):
                items = "\n".join(f"- {item}" for item in value)
                lines.append(f"{heading} {key}\n{items}")
            else:
                lines.append(f"{heading} {key}\n{value}")
        return "\n\n".join(lines)

    if isinstance(data, list):
        return "\n".join(f"- {item}" for item in data)

    return str(data)
