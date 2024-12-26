def get_backend_instances():
    return [
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003"
    ]

# Circuit breaker settings
FAILURE_THRESHOLD = 3 
RECOVERY_TIME = 30  # seconds
LATENCY_THRESHOLD = 2 #seconds