from dataclasses import dataclass
from enum import Enum
from typing import List
from .ingredient import Ingredient
import copy


class DishType(Enum):
    APPETIZER = "Appetizer"
    MAIN_COURSE = "Main Course"
    DESSERT = "Dessert"
    SIDE = "Side Dish"
    SALAD = "Salad"
    SOUP = "Soup"
    SNACK = "Snack"
    BREAKFAST = "Breakfast"
    BEVERAGE = "Beverage"
    OTHER = "Other"


@dataclass
class Recipe:
    name: str
    dish_type: DishType
    ingredients: List[Ingredient]
    prep_time: int
    description: str

    def scaled_portions(self, portions):
        r = copy.deepcopy(self)
        for i in self.ingredients:
            i.amount *= portions
        return r

    def takes_less_than(self, max_prep_time):
        return self.prep_time <= max_prep_time

    def contains_none_of(self, unwanted_ingredients):
        unwanted_names = {i.name for i in unwanted_ingredients}
        return not any(
            i.name in unwanted_names
            for i in self.ingredients
        )

    def all_available(self, pantry):
        pantry_dict = {p.name: p.amount for p in pantry}
        return all(
            pantry_dict.get(i.name, 0) >= i.amount
            for i in self.ingredients
        )

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
