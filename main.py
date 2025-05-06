
from datetime import date

from models.ingredient import Ingredient
from models.pantry import PantryIngredient
from models.recipe import Recipe, DishType
from helper.csv_parser import parse_csv

if __name__ == "__main__":
    pantry, recipes = parse_csv()
    for ing in pantry:
        print(ing)
    for rec in recipes:
        print(rec)
