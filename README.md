# Round Robin API system

A round-robin API system that efficiently distributes requests across multiple application instances while handling instance failures and slowness.

## Features

- Distribute requests evenly across instances
- Detect and handle slow or failed instances
- Ensure a consistent response to clients

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