from .inference import BaseInferenceEngine
import subprocess
import aiohttp
import bittensor as bt
from dataclasses import dataclass

@dataclass  
class Ollama(BaseInferenceEngine):
    model_image = "ollama/ollama"
    model_name = "ollama"
    host = "127.0.0.1"
    port = 11434

    @property
    def endpoint(self):
        return f"http://{self.host}:{self.port}"

    def start(self):
        subprocess.run(["docker", "run", "--gpus", "all", "--rm", "-d", "--name", self.model_name, "-p", f"{self.port}:{self.port}", 
                    "-e", "OLLAMA_HOST=0.0.0.0:11434", "-e", "OLLAMA_MODELS=/data/", "-v", "/tmp/ollama:/data",self.model_image, "serve"])

    def stop(self):
        subprocess.run["docker", "rm", "-f", self.model_name]

    async def inference(self, model, prompt):
        try:
            async with aiohttp.ClientSession() as session:
                resp = session.post(f"{self.endpoint}/api/generate", json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }, timeout=120)
                resp.raise_for_status()
        except Exception as e:
            bt.logging.error(e)
            return ""
        return resp.json()["response"]