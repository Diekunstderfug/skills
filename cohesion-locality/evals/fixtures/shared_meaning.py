from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    minor_units: int
    currency: str
