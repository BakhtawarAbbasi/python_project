import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Get user input
while True:
    user_input = input("\nEnter your question (or 'quit' to exit): ")

    if user_input.lower() == 'quit':
        print("Thanks for chatting! Goodbye!")
        break

    # generate response using user input
    response = model.generate_content(user_input)

    print("\nResponse:", response.text)