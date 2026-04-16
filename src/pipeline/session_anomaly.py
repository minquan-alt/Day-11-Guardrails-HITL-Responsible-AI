from collections import defaultdict
import time

class SessionAnomalyDetector:
    def __init__(self, max_strikes: int = 3, block_duration_sec: float = 300.0):
        self.max_strikes = max_strikes
        self.block_duration_sec = block_duration_sec
        self.strikes = defaultdict(int)
        self.block_until = defaultdict(float)
        
    def record_injection_attempt(self, user_id: str):
        """Record a strike for a user. Call this when input guard catches injection."""
        self.strikes[user_id] += 1
        if self.strikes[user_id] >= self.max_strikes:
            self.block_until[user_id] = time.time() + self.block_duration_sec
            
    def is_blocked(self, user_id: str) -> bool:
        """Check if user is currently blocked due to anomalies."""
        now = time.time()
        if user_id in self.block_until and now < self.block_until[user_id]:
            return True
        # Clean up if expired
        if user_id in self.block_until and now >= self.block_until[user_id]:
            del self.block_until[user_id]
            self.strikes[user_id] = 0
        return False
