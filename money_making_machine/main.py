import streamlit as st
import random
import time
import requests


# Custom Styling with Modern and Professional Theme
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364); /* Gradient background */
            color: #ffffff; /* White text */
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            background-color: #6a1b9a; /* Dark Purple */
            color: white;
            font-size: 18px;
            padding: 12px 24px;
            border-radius: 8px;
            transition: 0.3s;
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #9c27b0; /* Light Purple */
            transform: scale(1.05);
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #2c5364;
        }
        .stMarkdown h1 {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 20px;
            color: #00d1ff; /* Teal for headings */
        }
        .stMarkdown h2 {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 15px;
            color: #00d1ff; /* Teal for subheadings */
        }
        .stMarkdown h3 {
            text-align: center;
            font-size: 1.5rem;
            margin-bottom: 10px;
            color: #00d1ff; /* Teal for subheadings */
        }
        .stMarkdown p {
            text-align: center;
            font-size: 1.2rem;
            color: #ffffff; /* White text */
        }
        .stSuccess, .stInfo, .stError {
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            text-align: center;
            font-size: 1.2rem;
        }
        .stSuccess {
            background-color: #00c853; /* Green for success */
            color: white;
        }
        .stInfo {
            background-color: #00b0ff; /* Blue for info */
            color: white;
        }
        .stError {
            background-color: #ff1744; /* Red for error */
            color: white;
        }
        .stSpinner>div {
            color: #00d1ff; /* Teal for spinner */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with Emoji
st.title("💰 Money Making Machine ")


# Generate Money
st.subheader("✨ Instant Cash Generator")
if st.button("💵 Generate Money"):
    with st.spinner("🤑 Counting your money..."):
        time.sleep(2)
        amount = random.randint(1, 1000)
        st.success(f"🎉 You made **${amount}**!")

# Fetch Side Hustle Ideas
def fetch_side_hustle():
    try:
        response = requests.get("http://127.0.0.1:8000/side_hustles")
        if response.status_code == 200:
            hustles = response.json()
            return hustles["side_hustle"]
        else:
            return "💼 Freelancing"
    except:
        return "❌ Something went wrong!"

st.subheader("🚀 Side Hustle Ideas")
if st.button("💡 Generate Hustle"):
    idea = fetch_side_hustle()
    st.info(f"🛠 **{idea}**")


# Fetch Money Quotes
def fetch_money_quote():
    try:
        response = requests.get("http://127.0.0.1:8000/money_quotes")
        if response.status_code == 200:
            quotes = response.json()
            return quotes["money_quote"]
        else:
            return "💰 Money is the root of all evil!"
    except:
        return "❌ Something went wrong!"

st.subheader("🌟 Money-Making Motivation")
if st.button("🔥 Get Inspired"):
    quote = fetch_money_quote()
    st.success(f"📢 **{quote}**")