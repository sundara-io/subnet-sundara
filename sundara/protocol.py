# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
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

import typing
import bittensor as bt
import typing
import pydantic


class InferenceSynapse(bt.Synapse):
    meta: dict = {}
    input: dict
    output: typing.Optional[dict] = None

    def deserialize(self) -> dict:
        return self.output


class CPUInfo(pydantic.BaseModel):
    count: int
    freq: float
    usage_percent: int


class MemoryInfo(pydantic.BaseModel):
    total: int
    used: int
    free: int
    usage_percent: float


class DiskInfo(pydantic.BaseModel):
    total: int
    used: int
    free: int
    usage_percent: float


class GPUInfo(pydantic.BaseModel):
    index: int
    name: str
    utilization: int


class SystemInfo(pydantic.BaseModel):
    # -2 i'm validator
    # -1 unknown
    # 0 miner idle
    # 1 miner busy
    cpu: typing.Optional[CPUInfo]
    mem: typing.Optional[MemoryInfo]
    disk: typing.Optional[DiskInfo]
    status: int = -1
    gpus: typing.List[GPUInfo] = []


class SystemInfoSynapse(bt.Synapse):
    system_info: typing.Optional[SystemInfo]

    def deserialize(self) -> SystemInfo:
        return self.system_info

class APIInferenceSynapse(bt.Synapse):
    meta: dict = {}
    input: dict
    output: typing.Optional[dict] = None

    def deserialize(self) -> dict:
        return self.output