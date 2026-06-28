import psutil
from checks.base import Check, CheckResult


class CpuThresholdCheck(Check):
    def run(self):
        usage = psutil.cpu_percent(interval=1)
        threshold = self.config["threshold"]
        ok = usage <= threshold
        message = f"CPU at {usage}% (threshold {threshold}%)"
        return CheckResult("cpu_threshold", ok, usage, message)


class RamThresholdCheck(Check):
    def run(self):
        usage = psutil.virtual_memory().percent
        threshold = self.config["threshold"]
        ok = usage <= threshold
        message = f"RAM at {usage}% (threshold {threshold}%)"
        return CheckResult("ram_threshold", ok, usage, message)


class DiskThresholdCheck(Check):
    def run(self):
        path = self.config.get("path", "/")
        usage = psutil.disk_usage(path).percent
        threshold = self.config["threshold"]
        ok = usage <= threshold
        message = f"Disk at {usage}% on {path} (threshold {threshold}%)"
        return CheckResult("disk_threshold", ok, usage, message)
    