import pandas as pd
from datetime import datetime, timedelta, date

from models.ingredient import Ingredient
from models.pantry import PantryIngredient
from models.recipe import Recipe, DishType


def parse_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except:
        return None


def update_date(expiration_date, update):
    if expiration_date is None:
        return None
    return expiration_date + timedelta(days=update)


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
            dish_type=DishType(row["dish_type"]) if row["dish_type"] in DishType._value2member_map_ else DishType.OTHER,
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


def update_expiration(reference_date: date):
    pantry_df = pd.read_csv("data/ingredient_dataset.csv")

    expiration_dates = pantry_df["expiration_date"].dropna().apply(parse_date)
    oldest_date = min(expiration_dates)
    offset_days = (reference_date - oldest_date).days + 1

    for index, row in pantry_df.iterrows():
        expiration = parse_date(row.get("expiration_date", ""))
        opened = parse_date(row.get("opened_date", ""))
        new_expiration = update_date(expiration, offset_days)
        new_opened = update_date(opened, offset_days)
        if new_opened and new_opened > reference_date:
            new_opened = reference_date

        pantry_df.at[index, "expiration_date"] = new_expiration.strftime("%Y-%m-%d") if new_expiration else ""
        pantry_df.at[index, "opened_date"] = new_opened.strftime("%Y-%m-%d") if new_opened else ""

    pantry_df.to_csv("data/ingredient_dataset.csv", index=False)
