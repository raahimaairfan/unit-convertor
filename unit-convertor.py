import streamlit as st
import re

def convert_units(value, from_unit, to_unit):
    conversions = {
        "Length": {"km": {"m": 1000, "miles": 0.621371}, "m": {"km": 0.001, "cm": 100}, "miles": {"km": 1.60934, "feet": 5280}},
        "Weight": {"kg": {"g": 1000, "lbs": 2.20462}, "g": {"kg": 0.001, "mg": 1000}, "lbs": {"kg": 0.453592, "g": 453.592}},
        "Volume": {"liters": {"ml": 1000, "gallons": 0.264172}, "ml": {"liters": 0.001}, "gallons": {"liters": 3.78541}}
    }
    
    for category, units in conversions.items():
        if from_unit in units and to_unit in units[from_unit]:
            return round(value * units[from_unit][to_unit], 4)
    return None

def ai_mode(query):
    match = re.match(r"(\d+)\s*(\w+)\s*to\s*(\w+)", query.lower())
    if match:
        value, from_unit, to_unit = match.groups()
        result = convert_units(float(value), from_unit, to_unit)
        if result is not None:
            return f"{value} {from_unit} = {result} {to_unit}"
        return "❌ Conversion not supported. Try another query."
    return "❌ Invalid input. Use format like '5 km to miles'"

st.set_page_config(page_title="Unit Converter", layout="wide")

with st.sidebar:
    st.title("ℹ️ How to Use")
    st.write("**Manual Mode:** Select units and input values manually.")
    st.write("**AI Mode:** Type queries like '5 km to miles' and let AI convert it.")
    
    st.markdown("---")
    st.subheader("⚠️ Common Mistakes")
    st.write("❌ `5km to miles` (No space between number and unit)")
    st.write("❌ `convert 5 km to miles` (Too much text)")
    
    st.subheader("✅ Correct Format")
    st.write("✔️ `5 km to miles`")
    st.write("✔️ `10 kg to lbs`")

st.markdown("""
    <style>
        body {background: linear-gradient(to right, #1e3c72, #2a5298); color: white; font-family: Arial, sans-serif;}
        .title {font-size: 32px; font-weight: bold; text-align: center; padding: 15px; border-radius: 10px; background: rgba(0, 0, 0, 0.2); margin-bottom: 20px;}
        .container {text-align: center; padding: 30px; border-radius: 10px; background: rgba(255, 255, 255, 0.1); width: 50%; margin: auto;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🔢 Unit Converter with AI Mode</div>", unsafe_allow_html=True)
st.markdown("<div class='container'>", unsafe_allow_html=True)

option = st.radio("Select Mode:", ["Manual Mode", "AI Mode"])

if option == "Manual Mode":
    category = st.selectbox("Select Category:", ["Length", "Weight", "Volume"])
    
    unit_options = {
        "Length": ["km", "m", "miles", "cm", "feet"],
        "Weight": ["kg", "g", "lbs", "mg"],
        "Volume": ["liters", "ml", "gallons"]
    }
    
    value = st.number_input("Enter value:", min_value=0.0, step=0.1)
    from_unit = st.selectbox("From Unit:", unit_options[category])
    to_unit = st.selectbox("To Unit:", unit_options[category])
    
    if st.button("Convert"):
        result = convert_units(value, from_unit, to_unit)
        if result is not None:
            st.success(f"{value} {from_unit} = {result} {to_unit}")
        else:
            st.error("Conversion not supported.")

elif option == "AI Mode":
    query = st.text_input("Ask AI (e.g., '5 km to miles'):")
    if st.button("Convert with AI"):
        st.info(ai_mode(query))

st.markdown("</div>", unsafe_allow_html=True)