import uvicorn
from src.router.round_robin import RoundRobinAPI

router_api = RoundRobinAPI()

if __name__ == "__main__":
    uvicorn.run(router_api.app, host="0.0.0.0", port=3000)