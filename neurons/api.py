# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Copyright © 2023 Sundara Team

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import time
import typing

import bittensor as bt
from sundara.base.api import BaseAPINeuron
from sundara.protocol import APIInferenceSynapse, InferenceSynapse


class API(BaseAPINeuron):
    def __init__(self, config=None):
        super(API, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()

    async def forward(self, synapse: APIInferenceSynapse) -> APIInferenceSynapse:
        responses = await self.dendrite(
            axons=self.metagraph.axons,
            synapse=InferenceSynapse(meta=synapse.meta, input=synapse.input),
            deserialize=True,
            timeout=synapse.meta.get("timeout", 5),
        )
        for resp in responses:
            if resp:
                synapse.output = resp.output
                return synapse
        return synapse


    async def blacklist(
        self, synapse: APIInferenceSynapse
    ) -> typing.Tuple[bool, str]:
        if self.config.api.insecure_public:
            return False,"Insecure Public Enabled"

        if synapse.dendrite.hotkey in self.config.api.allowed_hotkeys:
            return False, f"Hotkey {synapse.dendrite.hotkey} whitelisted."

        return True, f"Request rejected. Hotkey {synapse.dendrite.hotkey}"

    async def priority(self, synapse: APIInferenceSynapse) -> float:
        """
        The priority function determines the order in which requests are handled. More valuable or higher-priority
        requests are processed before others. You should design your own priority mechanism with care.

        This implementation assigns priority to incoming requests based on the calling entity's stake in the metagraph.

        Args:
            synapse (template.protocol.Dummy): The synapse object that contains metadata about the incoming request.

        Returns:
            float: A priority score derived from the stake of the calling entity.

        Miners may recieve messages from multiple entities at once. This function determines which request should be
        processed first. Higher values indicate that the request should be processed first. Lower values indicate
        that the request should be processed later.

        Example priority logic:
        - A higher stake results in a higher priority value.
        """
        # TODO(developer): Define how miners should prioritize requests.
        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )  # Get the caller index.
        priority = float(
            self.metagraph.S[caller_uid]
        )  # Return the stake as the priority.
        bt.logging.trace(
            f"Prioritizing {synapse.dendrite.hotkey} with value: ", priority
        )
        return priority
    

if __name__ == "__main__":
    with API() as validator:
        while True:
            bt.logging.info("GatewayNeuron running...", time.time())
            time.sleep(5)
