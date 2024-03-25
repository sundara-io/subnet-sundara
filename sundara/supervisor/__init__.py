from fastapi import FastAPI, APIRouter, Request, Response, Depends
import bittensor as bt
import uvicorn
import threading


class Supervisor:
    def __init__(self, miner) -> None:
        self.miner = miner

        log_level = "trace" if bt.logging.__trace_on__ else "critical"
        self.app = FastAPI()
        self.fast_config = uvicorn.Config(
            self.app, host="0.0.0.0", port=10111, log_level=log_level
        )
        self.fast_server = uvicorn.Server(config=self.fast_config)
        self.router = APIRouter()
        self.router.add_api_route("/state", self.get_state)
        self.app.include_router(self.router)

    def start(self):
        bt.logging.info(f"sundara supervisor listening on {self.fast_config.port}")
        thread = threading.Thread(target=self.fast_server.run)
        thread.start()

    def get_state(self):
        return {
            "state": "busy" if self.miner.miner_state.get_state() else "idle"
        }

