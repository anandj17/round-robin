# Round Robin API system

A round-robin API system that efficiently distributes requests across multiple application instances while handling instance failures and slowness.

## Features

- Distribute requests evenly across instances
- Detect and handle slow or failed instances
- Ensure a consistent response to clients

## Setup

### Using Docker Compose (Recommended)

1. Build and start all services:
```bash
docker-compose up --build
```

This will start:
- Round Robin on port 3000
- Three application instances on ports 3001, 3002, and 3003

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start app instances:
```bash
python -m src.run_app 3001
python -m src.run_app 3002
python -m src.run_app 3003
```

3. Start the router:
```bash
python -m src.run_router
```

### Git hooks
```bash
python scripts/add_git_hooks.py
```

## Testing

Run the test suite:

```bash
pytest
```

Test coverage includes:
- App API functionality
   - Successful Request
   - Bad request (Invalid JSON)
   - Internal server error
- Round robin API functionality
   - All app instances are healthy
   - No app instances are healthy
   - One of the instances is not healthy
   - One of the instance is slow
   - Round robin flow