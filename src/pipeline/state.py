from typing import TypedDict, Optional, Dict

class PipelineState(TypedDict):
    user_id: str
    user_input: str
    response: str
    blocked: bool
    block_layer: str
    block_reason: str
    pii_redacted: bool
    judge_scores: Dict[str, int]
    judge_verdict: str
    latency_ms: float
    start_time: float
