import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(page_title="Quiz Application", page_icon=":brain:", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stRadio>div {
        flex-direction: column;
        align-items: flex-start;
    }
    .stRadio>label {
        font-size: 18px;
        margin: 5px 0;
    }
    .stSuccess {
        color: #4CAF50;
        font-size: 20px;
        font-weight: bold;
    }
    .stError {
        color: #FF0000;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Quiz Application 🧠")
st.markdown("---")

# Define the questions
questions = [
    {
        "question": "What is the capital of Pakistan?",
        "options": ["Karachi", "Lahore", "Islamabad", "Peshawar"],
        "answer": "Islamabad"
    },
    {
        "question": "What is the national flower of Pakistan?",
        "options": ["Rose", "Jasmine", "Lily", "Sunflower"],
        "answer": "Jasmine"
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1945", "1950", "1965", "1970"],
        "answer": "1945"
    },
    {
        "question": "How many Paras (sections) are there in the Holy Quran?",
        "options": ["20", "25", "30", "35"],
        "answer": "30"
    },
    {
        "question": "What is the height of Mount Everest?",
        "options": ["7,884 meters", "8,848 meters", "9,102 meters", "8,250 meters"],
        "answer": "8,848 meters"
    },
    {
        "question": "Which is the largest dam in Pakistan?",
        "options": ["Tarbela Dam", "Mangla Dam", "Warsak Dam", "Mirani Dam"],
        "answer": "Tarbela Dam"
    },
    {
        "question": "Who invented the first computer?",
        "options": ["Alan Turing", "Charles Babbage", "Bill Gates", "Steve Jobs"],
        "answer": "Charles Babbage"
    },
    {
        "question": "On which date was Pakistan founded?",
        "options": ["23rd March 1940", "14th August 1947", "25th December 1948", "1st January 1950"],
        "answer": "14th August 1947"
    },
    {
        "question": "What is the largest ocean in the world?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
        "answer": "Pacific Ocean"
    },
    {
        "question": "What is the largest organ in the human body?",
        "options": ["Liver", "Brain", "Skin", "Heart"],
        "answer": "Skin"
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
        "answer": "Carbon Dioxide"
    },
    {
        "question": "Who wrote the famous play 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": "William Shakespeare"
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Platinum"],
        "answer": "Diamond"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["China", "Japan", "South Korea", "Thailand"],
        "answer": "Japan"
    },
    {
        "question": "In which Islamic month was the Holy Quran revealed?",
        "options": ["Muharram", "Safar", "Rajab", "Ramadan"],
        "answer": "Ramadan"
    },
    {
        "question": "Which is the smallest continent in the world?",
        "options": ["Europe", "Australia", "Antarctica", "South America"],
        "answer": "Australia"
    },
    {
        "question": "Who was the first person to step on the moon?",
        "options": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"],
        "answer": "Neil Armstrong"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
        "answer": "Tokyo"
    },
    {
        "question": "Which is the longest river in the world?",
        "options": ["Amazon River", "Yangtze River", "Mississippi River", "Nile River"],
        "answer": "Nile River"
    }
]

# Initialize session state
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

question = st.session_state.current_question

# Display the question
st.subheader(question["question"])

# Display the options
selected_option = st.radio("Choose your answer:", question["options"], key="answer")

# Submit button
if st.button("Submit Answer"):
    if selected_option == question["answer"]:
        st.success("Correct! 🎉")
    else:
        st.error(f"Incorrect! 😢 The correct answer is: {question['answer']}")

    time.sleep(2)

    # Move to the next question
    st.session_state.current_question = random.choice(questions)
    st.rerun()