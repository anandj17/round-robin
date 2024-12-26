import httpx
import asyncio
from fastapi import FastAPI, HTTPException
from .circuit_breaker import CircuitBreaker
from ..config.settings import get_backend_instances
from ..utils.logger import Logger

logger = Logger(__name__).setup_logger()

class RoundRobinAPI:
    def __init__(self):
        self.app = FastAPI()
        self.instances = get_backend_instances()
        self.current_index = 0
        self.timeout = 10
        self.circuit_breakers = {url: CircuitBreaker() for url in self.instances}
        self._setup_routes()
        self.lock = asyncio.Lock()

    async def get_next_instance(self):
        async with self.lock:
            for _ in range(len(self.instances)):
                instance = self.instances[self.current_index]
                self.current_index = (self.current_index + 1) % len(self.instances)
                logger.info(f"Circuit breaker state for {instance} : {self.circuit_breakers[instance].state}")
                if self.circuit_breakers[instance].can_attempt():
                    return instance
            return None

    def _setup_routes(self):
        @self.app.post("/")
        async def route_request(payload: dict):
            last_error = None

            for _ in range(len(self.instances)):
                instance = await self.get_next_instance()
                if instance is None:
                    logger.error(f"No healthy instances available")
                    raise HTTPException(
                        status_code=503, detail="No healthy instances available"
                    )
                try:
                    async with httpx.AsyncClient(timeout=self.timeout) as client:
                        logger.info(f"Sending request to : {instance}")
                        start_time = asyncio.get_event_loop().time()
                        response = await client.post(
                            instance + "/process", json=payload
                        )
                        response_time = asyncio.get_event_loop().time() - start_time

                        logger.info(f"Successfully received response from : {instance}")

                        if response.status_code == 200:
                            self.circuit_breakers[instance].record_latency(
                                response_time
                            )
                            return response.json()
                        else:
                            raise Exception(f"HTTP {response.status_code}")
                except httpx.TimeoutException as e:
                    logger.warning(f"Timeout occurred for {instance}")
                    last_error = e
                    self.circuit_breakers[instance].record_failure()
                except httpx.RequestError as e:
                    logger.warning(f"Request failure for {instance}")
                    last_error = e
                    self.circuit_breakers[instance].record_failure()
                except Exception as e:
                    last_error = e
                    logger.warning(f"Request failed for {instance} : {str(e)}")
                    self.circuit_breakers[instance].record_failure()

            logger.error(f"All instances failed: {str(last_error)}")
            raise HTTPException(
                status_code=503, detail=f"All instances failed: {str(last_error)}"
            )