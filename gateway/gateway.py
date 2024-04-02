from dataclasses import dataclass, asdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import bittensor as bt
from sundara.utils.config import check_config, add_args, config
from sundara.base.neuron import BaseNeuron
from sundara.protocol import InferenceSynapse, SystemInfo, SystemInfoSynapse
from pydantic import BaseModel
from sundara.utils.uids import get_random_uids
from neurons.validator import Validator


class ChatInput(BaseModel):
    model: str
    input: str = ""


class Gateway(Validator):
    async def inference(self, input: dict, meta: dict = None):
        self.sync()
        responses = await self.dendrite(
            axons=self.metagraph.axons,
            synapse=InferenceSynapse(meta=meta, input=input),
            deserialize=True,
            timeout=5.0
        )
        print(responses)
        return responses

    async def get_system_info(self):
        self.sync()
        responses = await self.dendrite(
            axons=self.metagraph.axons,
            synapse=SystemInfoSynapse(),
            deserialize=True,
            timeout=5.0
        )
        print(responses)
        return responses


gateway = Gateway()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InferenceReq(BaseModel):
    meta: dict = {}
    input: dict


@app.post("/chat")
async def chat(input: ChatInput):
    resps = await gateway.inference(input={"model": input.model, "prompt": input.input})
    results = []
    for resp in resps:
        if resp:
            results.append(resp["response"])
        else:
            results.append(None)
    return {"results": results}


@app.post("/inference")
async def inference(req: InferenceReq):
    resps = await gateway.inference(meta=req.meta, input=req.input)
    for resp in resps:
        if resp:
            return {"meta": req.meta, "output": resp}
    return {"meta": req.meta, "output": None}


@dataclass
class Node:
    neuron: bt.NeuronInfo
    system_info: SystemInfo


@app.get("/nodes")
async def get_nodes():
    neurons = gateway.metagraph.neurons
    system_infos = await gateway.get_system_info()
    nodes = []
    for i, x in enumerate(neurons):
        nodes.append(Node(neuron=x, system_info=system_infos[i]))
    return {"nodes": nodes}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
