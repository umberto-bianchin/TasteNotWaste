from dataclasses import dataclass


@dataclass
class Ingredient:
    name: str
    amount: int
    unit: str

