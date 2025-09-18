from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class EvaluationMode(str, Enum):
    compare = "compare"
    jury = "jury"


class LLMConfig(BaseModel):
    base_url: str = Field(
        default="",
        description="Base URL for the OpenAI compatible endpoint (e.g., https://api.openai.com/v1).",
    )
    api_key: str = Field(default="", description="Token used for authenticating against the LLM service.")


class ModelOption(BaseModel):
    id: str
    name: str
    description: str | None = None


class DetectorOption(BaseModel):
    id: str
    label: str
    description: str | None = None
    default_threshold: float = Field(default=0.5, ge=0, le=1)


class JuryRoleOption(BaseModel):
    id: str
    name: str
    description: str


class EvaluationConfigResponse(BaseModel):
    models: List[ModelOption]
    detectors: List[DetectorOption]
    jury_roles: List[JuryRoleOption]


class DetectorSelection(BaseModel):
    id: str
    enabled: bool = True
    threshold: Optional[float] = Field(default=None, ge=0, le=1)


class JuryRoleSelection(BaseModel):
    id: str
    weight: float = Field(default=1.0, ge=0)


class CompareRequest(BaseModel):
    input_text: str
    models: List[str] = Field(default_factory=list, max_items=3)
    detectors: List[DetectorSelection] = Field(default_factory=list)


class JuryRequest(BaseModel):
    input_text: str
    roles: List[JuryRoleSelection] = Field(default_factory=list)
    detectors: List[DetectorSelection] = Field(default_factory=list)


class EvaluationRequest(BaseModel):
    mode: EvaluationMode
    compare: Optional[CompareRequest] = None
    jury: Optional[JuryRequest] = None
    llm: Optional[LLMConfig] = None


class DiffSnippet(BaseModel):
    model_id: str
    content: str
    highlighted_diff: List[str] = Field(default_factory=list)


class DetectorIssue(BaseModel):
    detector_id: str
    severity: str
    summary: str
    evidence: str


class CompareResult(BaseModel):
    generated_at: datetime
    completions: Dict[str, str]
    diffs: List[DiffSnippet]
    detector_issues: List[DetectorIssue]


class JuryRoleOpinion(BaseModel):
    role_id: str
    summary: str
    score: float
    recommendations: List[str]


class JuryAggregate(BaseModel):
    overall_score: float
    radar: Dict[str, float]
    consensus: Dict[str, float]


class JuryResult(BaseModel):
    generated_at: datetime
    opinions: List[JuryRoleOpinion]
    aggregate: JuryAggregate
    detector_issues: List[DetectorIssue]


class EvaluationResponse(BaseModel):
    mode: EvaluationMode
    compare_result: Optional[CompareResult] = None
    jury_result: Optional[JuryResult] = None
