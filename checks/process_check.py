import psutil
from checks.base import Check, CheckResult


class ProcessRunningCheck(Check):
    def run(self):
        pattern = self.config["pattern"].lower()
        found = False

        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if pattern in proc.info['name'].lower() or pattern in cmdline.lower():
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        message = f"Process matching '{pattern}' {'found' if found else 'NOT found'}"
        return CheckResult("process_running", found, None, message)
    