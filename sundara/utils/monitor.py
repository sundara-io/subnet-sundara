import gpustat
import psutil
import bittensor as bt
from ..protocol import (
    CPUInfo, GPUInfo, MemoryInfo, SystemInfoSynapse
)

def get_cpu_info():
    return CPUInfo(
        cpu_percent=psutil.cpu_percent(interval=1),
        cpu_freq=psutil.cpu_freq().current,
        cpu_count=psutil.cpu_count(),
    )

def get_mem_info():
    virtual_memory = psutil.virtual_memory()
    return MemoryInfo(
        mem_percent=virtual_memory.percent,
        mem_free=virtual_memory.free,
        mem_total=virtual_memory.total,
        mem_used=virtual_memory.used,
    )

def get_gpu_infos():
    gpus = []
    try:
        for gpu in gpustat.GPUStatCollection.new_query():
            gpus.append(
                GPUInfo(
                    index=gpu.index,
                    name=gpu.name,
                    utilization=gpu.utilization
                )
            )
    except Exception as e:
        bt.logging.warning(e)
    return gpus

    