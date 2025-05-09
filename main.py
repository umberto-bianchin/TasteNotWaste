from datetime import date

from models.ingredient import Ingredient
from models.pantry import PantryIngredient
from models.recipe import Recipe, DishType
from helper.csv_parser import parse_csv
from score.score import compute_score


def best_recipes(pantry, recipes, preferred_ingredients, unwanted_ingredients, available_only, portions, max_prep_time):
    # Dictionary to store the score associated with each recipe name
    scores = {}
    for r in recipes:
        score = 0

        # Check if the recipe is valid:
        # - It meets the maximum preparation time constraint
        # - It does not contain unwanted ingredients
        valid = r.takes_less_than(max_prep_time) and r.contains_none_of(unwanted_ingredients)

        # If the "available_only" flag is set (user doesn't want to buy missing ingredients),
        # filter further to ensure all ingredients are available in the pantry
        if available_only:
            valid = r.all_available(pantry)

        # If the recipe passed all validation criteria, calculate its final score
        if valid:
            # Adjust the recipe quantities based on the number of requested portions
            r = r.scaled_portions(portions)

            # Compute and store the score
            score = compute_score(r, pantry, preferred_ingredients)
            scores[r.name] = score

    #sort_scores(scores)
    return scores


if __name__ == "__main__":
    myPantry, myRecipes = parse_csv()
    for ing in myPantry:
        print(ing)
    for rec in myRecipes:
        print(rec)
    print("Best recipes:\n")
    best = best_recipes(myPantry, myRecipes, [], [], True, 2, 30)
