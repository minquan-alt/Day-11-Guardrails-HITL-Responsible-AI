import time
from langgraph.graph import StateGraph, END

from src.pipeline.state import PipelineState
from src.pipeline.nodes import (
    check_rate_limit,
    check_input_guards,
    check_session_anomaly,
    run_llm,
    run_output_guard,
    run_judge
)
from src.pipeline.audit import run_audit

def route_blocked(state: PipelineState) -> str:
    """Route to audit if blocked, otherwise proceed to next."""
    if state.get("blocked"):
        return "blocked"
    return "pass"

def create_pipeline() -> StateGraph:
    workflow = StateGraph(PipelineState)
    
    # Add nodes
    workflow.add_node("rate_limit", check_rate_limit)
    workflow.add_node("input_guard", check_input_guards)
    workflow.add_node("session_anomaly", check_session_anomaly)
    workflow.add_node("llm", run_llm)
    workflow.add_node("output_guard", run_output_guard)
    workflow.add_node("judge", run_judge)
    workflow.add_node("audit", run_audit)
    
    # Set entry point
    workflow.set_entry_point("rate_limit")
    
    # Edges from rate limit
    workflow.add_conditional_edges("rate_limit", route_blocked, {"blocked": "audit", "pass": "input_guard"})
    
    # Edges from input guard
    workflow.add_conditional_edges("input_guard", route_blocked, {"blocked": "audit", "pass": "session_anomaly"})
    
    # Edges from session anomaly
    workflow.add_conditional_edges("session_anomaly", route_blocked, {"blocked": "audit", "pass": "llm"})
    
    # Flow after LLM
    workflow.add_edge("llm", "output_guard")
    workflow.add_conditional_edges("output_guard", route_blocked, {"blocked": "audit", "pass": "judge"})
    workflow.add_conditional_edges("judge", route_blocked, {"blocked": "audit", "pass": "audit"})
    
    # Audit always goes to END
    workflow.add_edge("audit", END)
    
    return workflow.compile()

# Global pipeline instance
pipeline_app = create_pipeline()

def process_request(user_input: str, user_id: str = "default") -> str:
    """Main entry point to use the pipeline."""
    initial_state = PipelineState({
        "user_id": user_id,
        "user_input": user_input,
        "start_time": time.time(),
        "blocked": False,
        "block_layer": "",
        "block_reason": "",
        "pii_redacted": False,
        "response": "",
        "judge_scores": {},
        "judge_verdict": "",
        "latency_ms": 0.0
    })
    
    final_state = pipeline_app.invoke(initial_state)
    
    if final_state.get("blocked"):
        return final_state["block_reason"]
    return final_state.get("response", "Internal Error: No response generated.")
