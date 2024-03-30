import gpustat
import psutil
import bittensor as bt
from ..protocol import (
    CPUInfo, GPUInfo, MemoryInfo, DiskInfo
)

def get_cpu_info():
    return CPUInfo(
        usage_percent=psutil.cpu_percent(interval=1),
        freq=psutil.cpu_freq().current,
        count=psutil.cpu_count(),
    )

def get_mem_info():
    virtual_memory = psutil.virtual_memory()
    return MemoryInfo(
        usage_percent=virtual_memory.percent,
        free=virtual_memory.free,
        total=virtual_memory.total,
        used=virtual_memory.used,
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

def get_disk_info():
    disk_usage = psutil.disk_usage("/")
    return DiskInfo(
        total=disk_usage.total,
        used=disk_usage.used,
        free=disk_usage.free,
        usage_percent=disk_usage.percent,
    )