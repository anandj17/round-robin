from fastapi import FastAPI, Request, HTTPException
from src.utils.logger import Logger

class AppProcess:
    def __init__(self, instance_name: str):
        self.instance_name = instance_name
        self.app = FastAPI()
        self._create_routes()
        self.logger = Logger(f"app.api.{instance_name}").setup_logger()

    def _create_routes(self):
        @self.app.get("/health")
        def health():
            return {"status": "UP"}

        @self.app.post("/process")
        async def process(request: Request):
            try:
                json_data = await request.json()
                self.logger.info(f"Received request with payload: {json_data}")
                return json_data
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid JSON")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_app(self) -> FastAPI:
        return self.app
