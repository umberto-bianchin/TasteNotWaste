import streamlit as st
from score.score import best_recipes, calc_stats
from helper.csv_parser import parse_csv, update_expiration
from audio.audio import (
    record_audio,
    transcribe_audio,
    extract_filters,
    resolve_ingredient_name
)

def render_recipes(best, recipes, pantry, portions, buyIng):
    rank_emojis = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    if not best:
        st.warning("❌ No recipes found with the selected filters.")
        return

    st.markdown("## Best recipes")
    for idx, (name, score) in enumerate(best.items(), start=1):
        emoji = rank_emojis[idx - 1] if idx <= len(rank_emojis) else f"{idx}."
        recipe = next(r for r in recipes if r.name == name).scaled_portions(portions)
        st.markdown(f"""
        <div style='font-size:20px; font-weight:600; margin-top:1em'>
            {emoji} {recipe.name}
        </div>
        <div style='font-size:14px; color:gray; margin-bottom:0.5em'>
            Score: {score:.3f}
        </div>
        """, unsafe_allow_html=True)

        ingToBuy, ingExpiring = calc_stats(pantry, recipe)
        label = f"**{ingExpiring}** ingredient{'s' if ingExpiring != 1 else ''} about to expire"
        label += f" and **{ingToBuy}** to buy!" if buyIng else "!"

        with st.expander(label):
            st.markdown("📝 ***Ingredients:***")
            for ing in recipe.ingredients:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;• {ing.name}: {ing.amount} {ing.unit}", unsafe_allow_html=True)

            st.markdown(f"""
                ⏰ ***Preparation time:*** **{recipe.prep_time}** min  
                ℹ️ ***Description:***  
                {recipe.description}
            """)

#update_expiration()

# Retrieve csv data
myPantry, myRecipes = parse_csv()
st.session_state["pantry"] = myPantry
st.session_state["recipes"] = myRecipes

ing_map = {p.ing.name.lower(): p.ing for p in myPantry}
for r in myRecipes:
    for ing in r.ingredients:
        if ing.name not in ing_map:
            ing_map[ing.name] = ing


# UI
st.set_page_config(page_title="TasteNotWaste", page_icon="🍽️")
st.title("TasteNotWaste")
st.write("Welcome! Use the left menu to explore all functionalities.")

ingredientsName = list(ing_map.keys())

portions = st.slider("Number of portions", 1, 10, 1)
max_time = st.slider("Max prep time (min)", 5, 60, 30)
buyIng = st.checkbox("Buy ingredients")
unwantedIngName = st.multiselect("Allergies", ingredientsName)
preferredIngName = st.multiselect("Favourite Ingredients", ingredientsName)

rank_emojis = ["🥇", "🥈", "🥉"] + ["🏅"] * 7

if st.button("Suggest recipes"):
    unwantedIng = [ing_map[n] for n in unwantedIngName]
    preferredIng = [ing_map[n] for n in preferredIngName]

    best = best_recipes(myPantry, myRecipes, preferredIng, unwantedIng, not buyIng, portions, max_time)
    render_recipes(best, myRecipes, myPantry, portions, buyIng)
    
if st.button("🎤 Voice Command"):
    try:
        audio = record_audio(duration=10)
        text = transcribe_audio(audio)
        st.success(f"✅ You said: *{text}*")

        filters = extract_filters(text, ingredientsName)
        st.info(f"📌 Using filters: {filters['portions']} portions, {filters['max_time']} minutes, {filters['preferred']} preferred, {filters['unwanted']} unwanted")

        preferredIng = [resolve_ingredient_name(n, ing_map) for n in filters['preferred']]
        unwantedIng = [resolve_ingredient_name(n, ing_map) for n in filters['unwanted']]

        best = best_recipes(myPantry, myRecipes, preferredIng, unwantedIng, buyIng, filters['portions'], filters['max_time'])
        render_recipes(best, myRecipes, myPantry, filters['portions'], buyIng)

    except ValueError as err:
        st.error(f"❌ Unknown ingredient: '{err}'")
    except Exception as e:
        st.error(f"❌ Error during voice transcription: {e}")