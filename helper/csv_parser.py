import pandas as pd
from datetime import datetime

from models.ingredient import Ingredient
from models.pantry import PantryIngredient
from models.recipe import Recipe, DishType


def parse_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except:
        return None


def parse_ingredient_string(ingredient_str):
    items = ingredient_str.split("; ")
    result = []
    for item in items:
        if ": " in item:
            name_part, rest = item.split(": ")
            amount_part, unit = rest.split(" ")
            result.append(Ingredient(name=name_part.strip(), amount=int(amount_part), unit=unit.strip()))
    return result


def parse_pantry(p):
    pantry_list = [
        PantryIngredient(
            Ingredient(
                name=row["name"],
                amount=int(row["amount"]),
                unit=row["unit"]
            ),
            expiration_date=parse_date(row.get("expiration_date", "")),
            opened_date=parse_date(row.get("opened_date", "")),
            max_days_after_open=int(row["max_days_after_open"]) if pd.notna(row["max_days_after_open"]) else None
        )
        for _, row in p.iterrows()
    ]
    return pantry_list


def parse_recipes(r):
    recipe_list = [
        Recipe(
            name=row["name"],
            dish_type=DishType(row["dish_type"]),
            ingredients=parse_ingredient_string(row["ingredients"]),
            prep_time=int(row["prep_time_minutes"]),
            description=row["description"]
        )
        for _, row in r.iterrows()
    ]
    return recipe_list


def parse_csv():
    pantry_df = pd.read_csv("data/ingredient_dataset.csv")
    recipe_df = pd.read_csv("data/recipe_dataset.csv")
    return parse_pantry(pantry_df), parse_recipes(recipe_df)
