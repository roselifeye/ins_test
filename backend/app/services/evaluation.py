from __future__ import annotations

import asyncio
import difflib
from datetime import datetime
from typing import Dict, Iterable, List

from ..models import (
    CompareRequest,
    CompareResult,
    DetectorIssue,
    DetectorSelection,
    DiffSnippet,
    EvaluationMode,
    EvaluationRequest,
    EvaluationResponse,
    JuryAggregate,
    JuryRequest,
    JuryResult,
    JuryRoleOpinion,
)
from .llm_client import LLMClient


async def _run_detectors(detectors: Iterable[DetectorSelection], content: str) -> List[DetectorIssue]:
    issues: List[DetectorIssue] = []
    for detector in detectors:
        if not detector.enabled:
            continue
        threshold_display = detector.threshold if detector.threshold is not None else "default"
        issues.append(
            DetectorIssue(
                detector_id=detector.id,
                severity="medium",
                summary=f"Stub finding for {detector.id} (threshold={threshold_display}).",
                evidence=content[:120] + ("..." if len(content) > 120 else ""),
            )
        )
    return issues


async def _run_compare(
    request: CompareRequest,
    llm_client: LLMClient,
) -> CompareResult:
    if not request.models:
        raise ValueError("At least one model must be selected for compare mode")

    async def generate(model_id: str) -> tuple[str, str]:
        messages = [
            {"role": "system", "content": "You are an assistant analysing inspection drafts."},
            {"role": "user", "content": request.input_text},
        ]
        completion = await llm_client.generate_completion(model_id, messages)
        return model_id, completion

    completions_list = await asyncio.gather(*(generate(model_id) for model_id in request.models))
    completions: Dict[str, str] = {model_id: text for model_id, text in completions_list}

    diffs: List[DiffSnippet] = []
    if len(completions_list) >= 2:
        base_text = completions_list[0][1].splitlines()
        for model_id, text in completions_list[1:]:
            other_lines = text.splitlines()
            diff = difflib.unified_diff(base_text, other_lines, lineterm="")
            diffs.append(
                DiffSnippet(
                    model_id=model_id,
                    content=text,
                    highlighted_diff=list(diff),
                )
            )
    else:
        model_id, text = completions_list[0]
        diffs.append(DiffSnippet(model_id=model_id, content=text, highlighted_diff=[]))

    detector_issues = await _run_detectors(request.detectors, "\n\n".join(completions.values()))

    return CompareResult(
        generated_at=datetime.utcnow(),
        completions=completions,
        diffs=diffs,
        detector_issues=detector_issues,
    )


async def _run_jury(request: JuryRequest, llm_client: LLMClient) -> JuryResult:
    if not request.roles:
        raise ValueError("At least one jury role must be selected")

    async def evaluate(role_id: str, weight: float) -> JuryRoleOpinion:
        prompt = f"Role: {role_id}\nWeight: {weight}\nContent:\n{request.input_text}"
        messages = [
            {"role": "system", "content": "You are part of an AI review board."},
            {"role": "user", "content": prompt},
        ]
        completion = await llm_client.generate_completion(role_id, messages)
        return JuryRoleOpinion(
            role_id=role_id,
            summary=completion[:180],
            score=min(100.0, 60.0 + weight * 10.0),
            recommendations=[completion],
        )

    opinions = await asyncio.gather(*(evaluate(role.id, role.weight) for role in request.roles))

    overall_score = sum(opinion.score for opinion in opinions) / len(opinions)
    radar = {opinion.role_id: min(100.0, opinion.score) for opinion in opinions}
    consensus = {"agreement": 0.75, "dissent": 0.25}
    detector_issues = await _run_detectors(request.detectors, request.input_text)

    return JuryResult(
        generated_at=datetime.utcnow(),
        opinions=list(opinions),
        aggregate=JuryAggregate(overall_score=overall_score, radar=radar, consensus=consensus),
        detector_issues=detector_issues,
    )


async def run_evaluation(payload: EvaluationRequest, llm_client: LLMClient) -> EvaluationResponse:
    if payload.mode is EvaluationMode.compare:
        if not payload.compare:
            raise ValueError("Compare configuration missing")
        compare_result = await _run_compare(payload.compare, llm_client)
        return EvaluationResponse(mode=payload.mode, compare_result=compare_result)

    if payload.mode is EvaluationMode.jury:
        if not payload.jury:
            raise ValueError("Jury configuration missing")
        jury_result = await _run_jury(payload.jury, llm_client)
        return EvaluationResponse(mode=payload.mode, jury_result=jury_result)

    raise ValueError(f"Unsupported evaluation mode: {payload.mode}")
