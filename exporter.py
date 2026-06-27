from fastapi import FastAPI
from fastapi.responses import Response
import psutil

app = FastAPI()

def get_cpu_usage():
  return psutil.cpu_percent(interval=1)


def get_ram_usage():
  return psutil.virtual_memory().percent

def get_disk_usage(path="/"):
  return psutil.disk_usage(path).percent


@app.get("/metrics")
def metrics():
  cpu = get_cpu_usage()
  ram = get_ram_usage()
  disk = get_disk_usage()

  output = f"""# HELP system_cpu_usage_percent Current CPU usage percentage
# TYPE system_cpu_usage_percent gauge
system_cpu_usage_percent {cpu}
# HELP system_ram_usage_percent Current RAM usage percentage
# TYPE system_ram_usage_percent gauge
system_ram_usage_percent {ram}
# HELP system_disk_usage_percent Current disk usage percentage
# TYPE system_disk_usage_percent gauge
system_disk_usage_percent {disk}
"""

  return Response(content=output, media_type="text/plain")


