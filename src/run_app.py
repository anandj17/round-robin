import uvicorn
import sys
import os
from src.api.app_api import AppProcess

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3001
    instance_name = os.environ.get("INSTANCE_NAME", f"app{port-3000}")
    app_api = AppProcess(instance_name)
    uvicorn.run(app_api.app, host="0.0.0.0", port=port)