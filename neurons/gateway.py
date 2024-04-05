
import time

import bittensor as bt
from sundara.validator import forward
from sundara.base.validator import BaseValidatorNeuron
from sundara.protocol import APIInferenceSynapse,InferenceSynapse

class GatewayNeuron(BaseValidatorNeuron):
    def __init__(self, config=None):
        super(GatewayNeuron, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()

    async def forward(
        self, synapse: APIInferenceSynapse
    ) -> APIInferenceSynapse:
        responses = await self.dendrite(
            axons=self.metagraph.axons,
            synapse=InferenceSynapse(meta=synapse.meta, input=synapse.input),
            deserialize=True,
            timeout=synapse.meta.get("timeout", 5)
        )
        for resp in responses:
            if resp:
                synapse.output = resp.output
                return synapse
        return synapse


if __name__ == "__main__":
    with GatewayNeuron() as validator:
        while True:
            bt.logging.info("GatewayNeuron running...", time.time())
            time.sleep(5)