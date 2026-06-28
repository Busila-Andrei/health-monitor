import socket
from checks.base import Check, CheckResult


class PortOpenCheck(Check):
    def run(self):
        host = self.config["host"]
        port = self.config["port"]
        timeout = self.config.get("timeout", 2)

        try:
            with socket.create_connection((host, port), timeout=timeout):
                return CheckResult("port_open", True, None, f"Port {host}:{port} is open")
        except ConnectionRefusedError:
            message = f"Port {host}:{port} refused connection (service likely not running)"
            return CheckResult("port_open", False, "refused", message)
        except socket.timeout:
            message = f"Port {host}:{port} timed out (possible network/firewall issue)"
            return CheckResult("port_open", False, "timeout", message)
        except OSError as e:
            message = f"Port {host}:{port} error: {e}"
            return CheckResult("port_open", False, "error", message)
        