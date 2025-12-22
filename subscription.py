from typing import Any


class Subsciber:
    def __init__(self, value_getter) -> None:
        self.getter = value_getter

    def __str__(self) -> str:
        return self.getter()