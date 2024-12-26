from fastapi import FastAPI, Request, HTTPException

class AppProcess:
    def __init__(self, instance_name: str):
        self.instance_name = instance_name
        self.app = FastAPI()
        self._create_routes()

    def _create_routes(self):
        @self.app.get("/health")
        def health():
            return {"status": "UP"}

        @self.app.post("/process")
        async def process(request: Request):
            try:
                json_data = await request.json()
                return json_data
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid JSON")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_app(self) -> FastAPI:
        return self.app
