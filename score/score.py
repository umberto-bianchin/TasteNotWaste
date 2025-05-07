import math

EXPIRY_BONUS = 20
PANTRY_BONUS = 2
PANTRY_MALUS = 2
EXPIRY_THRESHOLD = 10
PREFERENCE_BONUS = 4
k = 0.3

def score_recipe(recipe, pantry, preferred_ingredients):
    score = 0
    for ingredient in recipe.ingredients:
        pantry_item = pantry.get(ingredient.name)
        if ingredient.name in preferred_ingredients:
            score += PREFERENCE_BONUS
        if pantry_item:
            quantity_ratio = min(pantry_item.quantity / ingredient.required_quantity, 1)
            bonus = PANTRY_BONUS * quantity_ratio
            if pantry_item.days_to_expiry <= EXPIRY_THRESHOLD:
                bonus += EXPIRY_BONUS * math.exp(-k * pantry_item.days_to_expiry)
            score += bonus
        else:
            score -= PANTRY_MALUS
    return score
