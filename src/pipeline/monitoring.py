from typing import List, Dict, Any

class MonitoringDashboard:
    def __init__(self, audit_logger):
        self.audit_logger = audit_logger
        
    def check_alerts(self) -> List[str]:
        alerts = []
        logs = self.audit_logger.logs
        if not logs:
            return alerts
            
        recent = logs[-100:]
        total = len(recent)
        
        blocked = sum(1 for log in recent if log.get("blocked"))
        if blocked / total > 0.3:
            alerts.append(f"WARNING: Overall block rate > 30% ({blocked}/{total})")
            
        rate_limit_hits = sum(1 for log in recent if log.get("block_layer") == "rate_limit")
        if rate_limit_hits / total > 0.1:
            alerts.append(f"WARNING: Rate limit hits > 10% ({rate_limit_hits}/{total})")
            
        judge_fails = sum(1 for log in recent if log.get("block_layer") == "judge")
        if count_passed_llm := sum(1 for log in recent if "response" in log and not log.get("blocked", False) or log.get("block_layer") == "judge"):
           if count_passed_llm > 0 and judge_fails / count_passed_llm > 0.2:
               alerts.append(f"WARNING: Judge fail rate > 20% ({judge_fails}/{count_passed_llm})")
               
        return alerts
