import streamlit as st
from score.score import best_recipes
from helper.csv_parser import parse_csv

# Retrieve csv data
myPantry, myRecipes = parse_csv()
st.session_state["pantry"] = myPantry
st.session_state["recipes"] = myRecipes

ing_map = {p.ing.name: p.ing for p in myPantry}

# UI
st.set_page_config(page_title="TasteNotWaste", page_icon="🍽️")
st.title("TasteNotWaste")
st.write("Welcome! Use the left menu to explore all functionalities.")

ingredientsName = list(ing_map.keys())

portions = st.slider("Number of portions", 1, 10, 2)
max_time = st.slider("Max prep time (min)", 5, 60, 30)
buyIng = st.checkbox("Buy ingredients")
unwantedIngName = st.multiselect("Allergies", ingredientsName)
preferredIngName = st.multiselect("Favourite Ingredients", ingredientsName)

unwantedIng = [ing_map[n] for n in unwantedIngName]
preferredIng = [ing_map[n] for n in preferredIngName]

if st.button("Suggest recipes"):
    best = best_recipes(myPantry, myRecipes, preferredIng, unwantedIng, not buyIng, portions, max_time)
    for name, score in best.items():
        st.write(f" {name} — Score: {score}")
    if len(best)==0:
        st.success(f"❌ No recipes found with the filters selected.")