from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..config import get_settings
from ..models import EvaluationConfigResponse, EvaluationRequest, EvaluationResponse, LLMConfig
from ..services.evaluation import run_evaluation
from ..services.llm_client import LLMClient

router = APIRouter()


def _build_llm_client(config: LLMConfig | None) -> LLMClient:
    settings = get_settings()
    base_url = config.base_url if config and config.base_url else settings.default_llm_base_url
    api_key = config.api_key if config and config.api_key else settings.default_llm_api_key
    return LLMClient(base_url=base_url, api_key=api_key)


@router.get("/config", response_model=EvaluationConfigResponse)
async def get_config() -> EvaluationConfigResponse:
    return EvaluationConfigResponse(
        models=[
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Balanced cost and quality."},
            {"id": "gpt-4o", "name": "GPT-4o", "description": "High quality reasoning."},
            {"id": "qwen-plus", "name": "Qwen Plus", "description": "Chinese optimized model."},
        ],
        detectors=[
            {
                "id": "consistency",
                "label": "一致性检测",
                "description": "识别语义与事实冲突",
                "default_threshold": 0.6,
            },
            {
                "id": "readability",
                "label": "可读性",
                "description": "结构与表达清晰度",
                "default_threshold": 0.5,
            },
            {
                "id": "compliance",
                "label": "合规与敏感",
                "description": "识别政策敏感内容",
                "default_threshold": 0.4,
            },
        ],
        jury_roles=[
            {"id": "product", "name": "产品评审", "description": "关注业务目标与用户体验"},
            {"id": "legal", "name": "法务合规", "description": "重点识别风险与违规"},
            {"id": "seo", "name": "SEO", "description": "优化搜索表现"},
            {"id": "marketing", "name": "营销运营", "description": "评估传播与渠道匹配"},
        ],
    )


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    try:
        llm_client = _build_llm_client(request.llm)
        return await run_evaluation(request, llm_client)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
