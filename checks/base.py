from abc import ABC, abstractmethod


class CheckResult:
    def __init__(self, name, ok, value=None, message=""):
        self.name = name
        self.ok = ok
        self.value = value
        self.message = message

    def __repr__(self):
        status = "OK" if self.ok else "FAIL"
        return f"[{status}] {self.name}: {self.message}"


class Check(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def run(self) -> CheckResult:
        pass
    