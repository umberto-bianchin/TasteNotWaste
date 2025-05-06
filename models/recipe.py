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
class RecipeIngredient:
    """Pairs an Ingredient with a required quantity for a recipe."""
    def __init__(self, ingredient: Ingredient, quantity: float):
        self.ingredient = ingredient
        self.quantity = quantity

    def __repr__(self):
        return (
            f"Recipe Ingredient:\n"
            f"  - {self.quantity} {self.ingredient.unit} of {self.ingredient.name}"
            f" (Expires: {self.ingredient.expiration_date.isoformat()}"
            + (
                f", Opened on: {self.ingredient.open_date.isoformat()},"
                f" +{self.ingredient.max_days_after_open}d shelf-life"
                if self.ingredient.open_date and self.ingredient.max_days_after_open is not None
                else ""
              )
            + ")"
        )

@dataclass
class Recipe:
    def __init__(
        self,
        name: str,
        ingredients: List[RecipeIngredient],
        preparation_time_minutes: int,
        description: str,
        dish_type: DishType
    ):
        self.name = name
        self.ingredients = ingredients
        self.preparation_time_minutes = preparation_time_minutes
        self.description = description
        self.dish_type = dish_type

    def add_ingredient(self, ingredient: Ingredient, quantity: float):
        """Convenience method to append an ingredient."""
        self.ingredients.append(RecipeIngredient(ingredient, quantity))

    def __repr__(self):
        ing_lines = "\n".join(
            f"  - {ing.quantity} {ing.ingredient.unit} {ing.ingredient.name}" for ing in self.ingredients
        )
        return (
            f"{self.name} ({self.dish_type.value})\n"
            f"Prep time: {self.preparation_time_minutes} minutes\n"
            f"{self.description}\n"
            f"Ingredients:\n{ing_lines}"
        )