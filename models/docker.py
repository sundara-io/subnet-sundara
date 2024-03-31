from .inference import BaseInferenceEngine
import subprocess
import httpx
import bittensor as bt
from dataclasses import dataclass

SUNDARA_CONTAINER_PREFIX = "sundara_model__"


@dataclass
class Ollama(BaseInferenceEngine):
    image_name = "ollama/ollama"
    model_name = "llama2"
    host = "127.0.0.1"
    port = 11434

    @property
    def endpoint(self):
        return f"http://{self.host}:{self.port}"

    @property
    def container_name(self):
        return SUNDARA_CONTAINER_PREFIX + self.model_name

    def start(self):
        try:
            bt.logging.info("starting ollama instance")
            subprocess.run(
                [
                    "docker",
                    "run",
                    "--gpus",
                    "all",
                    "--rm",
                    "-d",
                    "--name",
                    self.container_name,
                    "-p",
                    f"{self.port}:{self.port}",
                    "-e",
                    f"OLLAMA_HOST=0.0.0.0:{self.port}",
                    "-e",
                    "OLLAMA_MODELS=/data/",
                    "-v",
                    f"/tmp/sundara/ollama/{self.model_name}:/data",
                    self.image_name,
                    "serve",
                ]
            )
            bt.logging.info(f"loading model {self.model_name}")

            with httpx.stream(
                "POST",
                f"{self.endpoint}/api/pull",
                json={
                    "model": self.model_name,
                    "stream": True,
                },
            ) as resp:
                for line in resp.iter_lines():
                    bt.logging.info(f"ollama: {line}")
                resp.raise_for_status()
        except Exception as e:
            bt.logging.error(e)

    def stop(self):
        bt.logging.info("stopping ollama instance")
        subprocess.run(["docker", "rm", "-f", self.container_name])

    async def inference(self, model, input:dict):
        input["model"] = model
        input["stream"] = True
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.endpoint}/api/generate",
                    json=input,
                    timeout=120,
                )
                resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            bt.logging.error(e)
            return ""
        return resp.json()["response"]
