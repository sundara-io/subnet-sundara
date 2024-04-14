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
import os
import time
import typing
import bittensor as bt

# Bittensor Miner Template:
import sundara

# import base miner class which takes care of most of the boilerplate
from sundara.base.miner import BaseMinerNeuron
from engine import get_engine_factory_by_name
from sundara.utils.monitor import (
    get_cpu_info,
    get_gpu_infos,
    get_mem_info,
    get_disk_info,
)
from threading import Lock
from sundara.protocol import SystemInfo


class MinerState:
    def __init__(self) -> None:
        self.working_state = 0
        self._lock = Lock()

    def set_state(self, new_state):
        self._lock.acquire()
        self.working_state = new_state
        self._lock.release()

    def get_state(self):
        return self.working_state


class Miner(BaseMinerNeuron):
    def __init__(self, config=None):
        super(Miner, self).__init__(config=config)
        self.engine = get_engine_factory_by_name(self.config.engine.name)(models=self.config.engine.models)
        if not os.getenv("SUNDARA_DISABLE_INFERENCE_ENGINE"):
            self.engine.start()
        self.miner_state = MinerState()

    def stop(self):
        self.engine.stop()

    async def get_stats(
        self, synapse: sundara.protocol.SystemInfoSynapse
    ) -> sundara.protocol.SystemInfoSynapse:
        synapse.system_info = SystemInfo(
            status=self.miner_state.get_state(),
            cpu=get_cpu_info(),
            mem=get_mem_info(),
            disk=get_disk_info(),
            gpus=get_gpu_infos(),
        )
        return synapse

    async def forward(
        self, synapse: sundara.protocol.InferenceSynapse
    ) -> sundara.protocol.InferenceSynapse:
        bt.logging.info(f"receive request: {synapse}")
        self.miner_state.set_state(1)
        result = await self.engine.inference(synapse.input)
        bt.logging.info("inference result", result)
        self.miner_state.set_state(0)
        synapse.output = result
        return synapse

    async def blacklist(
        self, synapse: sundara.protocol.InferenceSynapse
    ) -> typing.Tuple[bool, str]:
        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            # Ignore requests from un-registered entities.
            bt.logging.trace(
                f"Blacklisting un-registered hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        if self.config.blacklist.force_validator_permit:
            # If the config is set to force validator permit, then we should only allow requests from validators.
            if not self.metagraph.validator_permit[uid]:
                bt.logging.warning(
                    f"Blacklisting a request from non-validator hotkey {synapse.dendrite.hotkey}"
                )
                return True, "Non-validator hotkey"

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"

    async def priority(self, synapse: sundara.protocol.InferenceSynapse) -> float:
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


# This is the main function, which runs the miner.
if __name__ == "__main__":
    with Miner() as miner:
        while True:
            bt.logging.info("Miner running...", time.time())
            time.sleep(5)
