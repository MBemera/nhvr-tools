"""Pydantic models for NHVR MCP inputs and outputs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class OutputFormatModel(BaseModel):
    output_format: str = Field(default="markdown", pattern="^(markdown|json)$")


class FatigueRulesInput(OutputFormatModel):
    scheme: str = Field(default="standard", pattern="^(standard|bfm|afm)$")


class MassLimitsInput(OutputFormatModel):
    include_hml: bool = False


class BreachCategoriesInput(OutputFormatModel):
    breach_type: str | None = None


class CorDutiesInput(OutputFormatModel):
    role: str | None = None


class AccreditationInput(OutputFormatModel):
    module: str | None = None


class PermitTypesInput(OutputFormatModel):
    permit_type: str | None = None


class VehicleRegistrationInput(OutputFormatModel):
    plate_number: str = Field(min_length=1)


class SearchRegulationsInput(OutputFormatModel):
    query: str = Field(min_length=1)


class ScrapePageInput(OutputFormatModel):
    url: str = Field(min_length=1)


class ToolResponse(BaseModel):
    data: Any
    output_format: str
