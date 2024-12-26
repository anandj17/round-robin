import os

def get_backend_instances():
    # Check if running in Docker
    if os.environ.get('DOCKER_ENV'):
        return [
            "http://app1:3001",
            "http://app2:3002",
            "http://app3:3003"
        ]
    
    # Local development
    return [
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003"
    ]

# Circuit breaker settings
FAILURE_THRESHOLD = 3 
RECOVERY_TIME = 30  # seconds
LATENCY_THRESHOLD = 2 #seconds