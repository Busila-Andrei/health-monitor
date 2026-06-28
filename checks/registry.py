from checks.system_checks import CpuThresholdCheck, RamThresholdCheck, DiskThresholdCheck
from checks.process_check import ProcessRunningCheck
from checks.port_check import PortOpenCheck

CHECK_REGISTRY = {
    "cpu_threshold": CpuThresholdCheck,
    "ram_threshold": RamThresholdCheck,
    "disk_threshold": DiskThresholdCheck,
    "process_running": ProcessRunningCheck,
    "port_open": PortOpenCheck,
}


def build_checks(check_configs):
    checks = []
    for cfg in check_configs:
        if not cfg.get("enabled", True):
            continue

        check_type = cfg["type"]
        if check_type not in CHECK_REGISTRY:
            raise ValueError(f"Unknown check type: {check_type}")
        check_class = CHECK_REGISTRY[check_type]
        checks.append(check_class(cfg))
    return checks
