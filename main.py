import streamlit as st
from score.score import best_recipes
from helper.csv_parser import parse_csv

myPantry, myRecipes = parse_csv()

# UI
st.set_page_config(page_title="TasteNotWaste", page_icon="🍽️")
st.title("TasteNotWaste")
st.write("Welcome! Use the left menu to explore all functionalities.")

portions = st.slider("Number of portions", 1, 10, 2)
buyIng = st.checkbox("Buy ingredients")
max_time = st.slider("Max prep time (min)", 5, 60, 30)
unwantedIng = st.multiselect("Allergies", myPantry)

if st.button("Suggest recipes"):
    best = best_recipes(myPantry, myRecipes, [], [], buyIng, portions, max_time)
    st.image("1.jpg")
    for name, score in best.items():
        st.write(f" {name} — Score: {score:.2f}")