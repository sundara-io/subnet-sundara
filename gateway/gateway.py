from dataclasses import dataclass, asdict

from fastapi import FastAPI
import uvicorn
import bittensor as bt
from sundara.utils.config import check_config, add_args, config
from sundara.base.neuron import BaseNeuron
from sundara.protocol import Inference, State
from pydantic import BaseModel
from sundara.utils.uids import get_random_uids
from neurons.validator import Validator

class Input(BaseModel):
    model: str
    input: str = ""

class Gateway(Validator):
    async def inference(self, input: Input):
        miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)
        print("miner_uids", miner_uids)
        print([self.metagraph.axons[uid] for uid in miner_uids])
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            synapse=Inference(model=input.model, input=input.input),
            deserialize=True,
        )
        print(responses)
        return responses
    
    async def get_states(self):
        responses = await self.dendrite(
            axons=self.metagraph.axons,
            synapse=State(),
            deserialize=False,
        )
        print(responses)
        return responses

gateway = Gateway()

app = FastAPI()



@app.post("/chat")
async def chat(input: Input):
    results = await gateway.inference(input)
    return {"results": results}

@dataclass
class Node:
    neuron: bt.NeuronInfo
    state: int

@app.get("/nodes")
async def get_nodes():
    neurons = gateway.metagraph.neurons
    states = await gateway.get_states()
    nodes = []
    for i, x in enumerate(neurons):
        nodes.append(Node(neuron=x, state=states[i].state))
    return {"nodes": nodes}

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")