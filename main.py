from models.ingredient import Ingredient
from models.recipe import *
from utils.csv_parser import *
from datetime import date

if __name__ == "__main__":
    # 1) create Ingredient instances
    flour = Ingredient("Flour", expiration_date=date(2025, 6, 1))
    sugar = Ingredient("Sugar", expiration_date=date(2026, 1, 1))
    butter = Ingredient(
        "Butter",
        expiration_date=date(2025, 5, 20),
        open_date=date(2025, 4, 28),
        max_days_after_open=10,
        unit="g"
    )

    # 2) build your recipe
    cake = Recipe(
        name="Simple Butter Cake",
        ingredients=[
            RecipeIngredient(flour, 200),
            RecipeIngredient(sugar, 100),
            RecipeIngredient(butter, 150),
        ],
        preparation_time_minutes=45,
        description="A tender, buttery cake that's easy to make.",
        dish_type=DishType.DESSERT,
    )

    # 3) add more if you like
    cake.add_ingredient(Ingredient("Eggs", expiration_date=date(2025, 5, 15), unit="pcs"), 3)

    #print(RecipeIngredient(flour, 200))
    print(Ingredient("Eggs", expiration_date=date(2025, 5, 5), unit="pcs"))
    #print(cake)