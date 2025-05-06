from dataclasses import dataclass
from enum import Enum
from typing import List
from .ingredient import Ingredient


class DishType(Enum):
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"
    SIDE = "Side Dish"
    SALAD = "Salad"
    SOUP = "Soup"
    BEVERAGE = "Beverage"
    OTHER = "Other"


@dataclass
class Recipe:
    name: str
    dish_type: DishType
    ingredients: List[Ingredient]
    prep_time: int
    description: str

    def __repr__(self):
        ing_lines = "\n".join(
            f"  - {ing.name} {ing.amount} {ing.unit}" for ing in self.ingredients
        )
        return (
            f"{self.name} ({self.dish_type.value})\n"
            f"Prep time: {self.prep_time} minutes\n"
            f"Ingredients:\n{ing_lines}\n"
            f"{self.description}\n"
        )
