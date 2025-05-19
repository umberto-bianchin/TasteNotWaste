import streamlit as st
from helper.csv_parser import parse_csv

st.set_page_config(page_title="Pantry", page_icon="📦")
st.title("📦 Your Pantry")

# Upload CSV
try:
    pantry, _ = parse_csv()
    st.session_state["pantry"] = pantry
    st.success(f"✅ {len(pantry)} ingredients in your pantry.")
except Exception as e:
    st.error(f"❌ Error loading pantry: {e}")
    pantry = []

if pantry:
    for item in pantry:
        ing = item.ing
        days_left = item.days_to_expiry() if hasattr(item, "days_to_expiry") else "-"
        opened_str = f"Opened on: {item.opened_date.strftime('%Y-%m-%d')}" if item.opened_date else ""
        with st.expander(label=f"""**{ing.name} ({ing.amount} {ing.unit})**""", expanded=False):
            st.markdown(f"""
                ⚖️ Quantity: **{ing.amount} {ing.unit}**  
                {'⚠️ ️EXPIRED!' if days_left == 0 else f"""⌛ Expires in **{days_left}** days"""}  
                🗓️ Expiry: {item.expiration_date}  
                {'🔓 Opened on: ' + item.opened_date.strftime('%Y-%m-%d') if item.opened_date else ''}                         
                """)
else:
    st.info("There are no ingredients in your pantry.")
