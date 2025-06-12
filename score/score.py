import math
from collections import OrderedDict

EXPIRY_BONUS = 20
PANTRY_BONUS = 2
PANTRY_MALUS = 2
EXPIRY_THRESHOLD = 10
PREFERENCE_BONUS = 4
k = 0.3


def compute_score(recipe, pantry, preferred_ingredients):
    score = 0
    pantry_dict = {p.ing.name: p for p in pantry}
    preferred_names = {i.name for i in preferred_ingredients}
    for ingredient in recipe.ingredients:
        pantry_item = pantry_dict.get(ingredient.name)
        if ingredient.name in preferred_names:
            score += PREFERENCE_BONUS
        if pantry_item:
            quantity_ratio = min(pantry_item.ing.amount / ingredient.amount, 1)
            bonus = PANTRY_BONUS * quantity_ratio
            bonus += EXPIRY_BONUS * math.exp(-k * pantry_item.days_to_expiry())
            score += bonus
        else:
            score -= PANTRY_MALUS
    return score


def best_recipes(pantry, recipes, preferred_ingredients, unwanted_ingredients, available_only, portions, max_prep_time):
    # Dictionary to store the score associated with each recipe name
    scores = {}
    for r in recipes:
        # Check if the recipe is valid:
        # - It meets the maximum preparation time constraint
        # - It does not contain unwanted ingredients
        valid = r.takes_less_than(max_prep_time) and r.contains_none_of(unwanted_ingredients)

        # Adjust the recipe quantities based on the number of requested portions
        r_scaled = r.scaled_portions(portions)

        # If the "available_only" flag is set (user doesn't want to buy missing ingredients),
        # filter further to ensure all ingredients are available in the pantry
        if available_only:
            valid = r_scaled.all_available(pantry)

        # If the recipe passed all validation criteria, calculate its final score
        if valid:
            # Compute and store the score
            scores[r_scaled.name] = compute_score(r_scaled, pantry, preferred_ingredients)

    scores_sorted = OrderedDict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
    return scores_sorted


def calc_stats(pantry, recipe):
    ingToBuy = 0
    ingExpiring = 0
    for ingredient in recipe.ingredients:
        pantry_item = next((p for p in pantry if p.ing.name.lower() == ingredient.name.lower()), None)
        if pantry_item is None:
            ingToBuy += 1
        else:
            days = pantry_item.days_to_expiry()
            if days is not None and days <= EXPIRY_THRESHOLD:
                ingExpiring += 1
            if pantry_item.ing.amount < ingredient.amount:
                ingToBuy += 1

    return ingToBuy, ingExpiring
