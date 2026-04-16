import time
from src.pipeline.rate_limiter import RateLimiter

def test_rate_limiter():
    limiter = RateLimiter(max_requests=2, window_seconds=1.0)
    
    # First two should pass
    assert limiter.check("user1") is False
    assert limiter.check("user1") is False
    
    # Third should be blocked
    assert limiter.check("user1") is True
    
    # Other user should pass
    assert limiter.check("user2") is False
    
    # Wait for window to expire
    time.sleep(1.1)
    
    # Should pass again
    assert limiter.check("user1") is False
