from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List
import pynvml
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

public_dir = os.path.join(os.path.dirname(__file__), "public")

app.mount("/public", StaticFiles(directory=public_dir), name="public")

@app.get("/", response_class=Response)
async def serve_index():
    index_path = os.path.join(public_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(content=html_content, media_type="text/html")

class GPUInfo(BaseModel):
    index: int
    name: str
    memory_total: int  # in MiB
    memory_used: int   # in MiB
    memory_free: int   # in MiB
    utilization: int   # in percentage
    temperature: int   # in Celsius

@app.on_event("startup")
def init_nvml():
    pynvml.nvmlInit()

@app.on_event("shutdown")
def shutdown_nvml():
    pynvml.nvmlShutdown()

@app.get("/gpus", response_model=List[GPUInfo])
def get_gpu_info():
    device_count = pynvml.nvmlDeviceGetCount()
    gpus = []

    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

        gpus.append(GPUInfo(
            index=i,
            name=name,
            memory_total=mem.total // 1024**2,
            memory_used=mem.used // 1024**2,
            memory_free=mem.free // 1024**2,
            utilization=util.gpu,
            temperature=temp
        ))

    return gpus
