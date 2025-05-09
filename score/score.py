import math

EXPIRY_BONUS = 20
PANTRY_BONUS = 2
PANTRY_MALUS = 2
EXPIRY_THRESHOLD = 10
PREFERENCE_BONUS = 4
k = 0.3

def compute_score(recipe, pantry, preferred_ingredients):
    score = 0
    pantry_dict = {p.ing.name: p for p in pantry}
    for ingredient in recipe.ingredients:
        pantry_item = pantry_dict.get(ingredient.name)
        if ingredient.name in preferred_ingredients:
            score += PREFERENCE_BONUS
        if pantry_item:
            quantity_ratio = min(pantry_item.ing.amount / ingredient.amount, 1)
            bonus = PANTRY_BONUS * quantity_ratio
            if EXPIRY_THRESHOLD >= pantry_item.days_to_expiry():
                bonus += EXPIRY_BONUS * math.exp(-k * pantry_item.days_to_expiry())
            score += bonus
        else:
            score -= PANTRY_MALUS
    return f"{score:.3f}"