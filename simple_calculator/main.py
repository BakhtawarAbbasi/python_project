import streamlit as st
import time

def main():
    st.markdown(
        """
        <style>
            .stButton > button {
                background-color: #6c5ce7;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
            }
            .stButton > button:hover {
                background-color: #a29bfe;
            }
            .title {
                color: #00cec9;
            }
            .result {
                font-size: 22px;
                font-weight: bold;
                color: #0984e3;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 class='title'>🧮 Interactive Calculator</h1>", unsafe_allow_html=True)
    st.write("### Enter two numbers and choose an operation")

    col1, col2 = st.columns(2)
    
    with col1:
        num1 = st.number_input("Enter first number", value=0.0)
    with col2: 
        num2 = st.number_input("Enter second number", value=0.0)

    operation = st.selectbox("Choose an operation", [
        "➕ Addition",
        "➖ Subtraction",
        "✖️ Multiplication",
        "➗ Division"])

    if st.button("🚀 Calculate"):
        with st.spinner("Calculating..."):
            time.sleep(1)
            try:
                if "Addition" in operation:
                    result = num1 + num2
                    symbol = "➕"
                elif "Subtraction" in operation:
                    result = num1 - num2
                    symbol = "➖"
                elif "Multiplication" in operation:
                    result = num1 * num2
                    symbol = "✖️"
                else:
                    if num2 == 0:
                        st.error("❌ Error: Division by Zero!")
                        return
                    result = num1 / num2
                    symbol = "➗"
                
                st.markdown(f"<p class='result'>{num1} {symbol} {num2} = {result}</p>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()