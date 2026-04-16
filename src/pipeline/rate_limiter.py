from collections import defaultdict, deque
import time

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.windows = defaultdict(deque)

    def check(self, user_id: str) -> bool:
        """Returns True if the user should be blocked, False otherwise."""
        now = time.time()
        window = self.windows[user_id]
        
        # Remove expired
        while window and window[0] < now - self.window_seconds:
            window.popleft()
            
        if len(window) >= self.max_requests:
            return True
            
        window.append(now)
        return False
        
    def get_wait_time(self, user_id: str) -> float:
        """Get seconds until the next request is allowed."""
        now = time.time()
        window = self.windows[user_id]
        if not window:
            return 0.0
        # Wait time is time until the oldest request expires
        return max(0.0, (window[0] + self.window_seconds) - now)
