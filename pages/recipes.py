import streamlit as st
from helper.csv_parser import parse_csv

st.set_page_config(page_title="Recipies", page_icon="🍽️")
st.title("🍽️ Your Recipes")

recipes = st.session_state["recipes"]

if not recipes:
    # Upload CSV
    try:
        _, recipes = parse_csv()
        st.session_state["recipes"] = recipes
    except Exception as e:
        st.error(f"❌ Error loading recipes: {e}")
        recipes = []

if recipes:
    st.success(f"✅ {len(recipes)} recipes in your menu.")
    for recipe in recipes:
        with st.expander(f"**{recipe.name}** ({recipe.dish_type.value})", expanded=False):
            st.markdown(f"**⏱️ Prep time:** {recipe.prep_time} min")
            st.markdown(f"**📝 Description:** {recipe.description}")
            st.markdown("**🍴 Ingredients:**")
            for ing in recipe.ingredients:
                st.markdown(f"""⚪ **{ing.name}**, quantity: **{ing.amount} {ing.unit}**""")
else:
    st.info("There are no recipies in your menu.")
