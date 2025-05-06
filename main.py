
from datetime import date

from models.ingredient import Ingredient
from models.pantry import PantryIngredient
from models.recipe import Recipe, DishType

if __name__ == "__main__":
    # 1) create Ingredient instances
    flour = Ingredient("Flour", 400, "g")
    sugar = Ingredient("Sugar", 600, "g")
    butter = Ingredient("Butter", 400, "g")
    flourp = PantryIngredient(flour, expiration_date=date(2025, 6, 1))
    sugarp = PantryIngredient(sugar, expiration_date=date(2026, 1, 1))
    butterp = PantryIngredient(
        butter,
        expiration_date=date(2025, 5, 20),
        opened_date=date(2025, 4, 28),
        max_days_after_open=10,
    )

    # 2) build your recipe
    cake = Recipe(
        name="Simple Butter Cake",
        ingredients=[
            flour,
            sugar,
            butter
        ],
        prep_time=45,
        description="A tender, buttery cake that's easy to make.",
        dish_type=DishType.DESSERT,
    )

    # 3) add more if you like
    # cake.add_ingredient(Ingredient("Eggs", expiration_date=date(2025, 5, 15), unit="pcs"), 3)

    #print(RecipeIngredient(flour, 200))
    #print(Ingredient("Eggs", expiration_date=date(2025, 5, 5), unit="pcs"))
    print(cake)
    print(butterp)
