import json
from datetime import datetime
from typing import List, Dict, Any

from src.pipeline.state import PipelineState

class AuditLog:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        
    def record(self, state: PipelineState):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            **state
        }
        self.logs.append(log_entry)
        
    def export_json(self, filepath: str = "audit_log.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)

# Global instances
audit_logger = AuditLog()

def run_audit(state: PipelineState) -> PipelineState:
    import time
    if "start_time" in state:
        state["latency_ms"] = (time.time() - state["start_time"]) * 1000.0
    audit_logger.record(state)
    return state
