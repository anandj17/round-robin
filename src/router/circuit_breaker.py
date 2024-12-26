import asyncio
from ..config.settings import FAILURE_THRESHOLD, LATENCY_THRESHOLD, RECOVERY_TIME

class CircuitBreaker:
    def __init__(self):
        self.failure_threshold = FAILURE_THRESHOLD
        self.recovery_time = RECOVERY_TIME
        self.latency_threshold = LATENCY_THRESHOLD
        self.failure_count = 0
        self.state = "CLOSED"  # "CLOSED", "OPEN", or "HALF-OPEN"
        self.last_failure_time = None

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_failure_time = asyncio.get_event_loop().time()

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_latency(self, response_time):
        if response_time > self.latency_threshold:
            self.record_failure()
        else:
            self.record_success()

    def can_attempt(self):
        if self.state == "OPEN":
            if (
                asyncio.get_event_loop().time() - self.last_failure_time
                > self.recovery_time
            ):
                self.state = "HALF-OPEN"
                return True
            return False
        return True