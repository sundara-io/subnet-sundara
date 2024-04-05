
import time

import bittensor as bt
import sundara
from sundara.validator import forward
from sundara.base.validator import BaseValidatorNeuron

class GatewayNeuron(BaseValidatorNeuron):
    def __init__(self, config=None):
        super(GatewayNeuron, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()

    async def forward(self):
        return await forward(self)


if __name__ == "__main__":
    with GatewayNeuron() as validator:
        while True:
            bt.logging.info("GatewayNeuron running...", time.time())
            time.sleep(5)