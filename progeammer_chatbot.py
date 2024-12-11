import streamlit as st
import pandas as pd
from Model_train import find_best_answer
import json
import os

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 

history_file = "chat_history.json"

def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            return json.load(file)
    return []

def save_history(chat_history):
    with open(history_file, "w") as file:
        json.dump(chat_history, file)

st.set_page_config(
    page_title="Python QnA Chatbot",
    layout="wide",
    menu_items={"About": "Python QnA Chatbot UI using Streamlit"}
)

st.sidebar.title("🚀 Navigation")
selected_page = st.sidebar.radio(
    "Go to:", 
    ["🏠 Home", "🤖 Chatbot", "📜 History", "ℹ️ About"]
)

if selected_page == "🏠 Home":
    st.title(" Welcome to the Python QnA Chatbot!")
    st.markdown("""
        This chatbot is designed to assist with Python-related questions.  
        It uses machine learning and natural language processing to provide answers based on a specific dataset.
        """)
    st.image("friendly_robot.png", width=300)

elif selected_page == "🤖 Chatbot":
    st.title("🤖 Programmer Chatbot at Your Service")
    user_input = st.text_input("Ask your Python question:")
    if st.button("Submit"):
        response = find_best_answer(str(user_input))
        st.session_state.chat_history.insert(0,(user_input, response))
        st.session_state.user_input = ""
        save_history(st.session_state.chat_history)

    for user_query, bot_reply in st.session_state.chat_history:
        st.markdown(
            f"""
                <div style="flex: 1; text-align: right; padding: 10px; border-radius: 10px; margin-right: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <strong>You:</strong> {user_query}
                <div style="flex: 1; text-align: left; padding: 10px; border-radius: 10px; margin-left: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <strong>Chatbot:</strong> {bot_reply}
                </div>
            """,
            unsafe_allow_html=True,
        )

elif selected_page == "📜 History":
    st.title("📜 Chat History")
    if(load_history == []):
        for _past_user_query,past_bot_reply in load_history():  
                st.markdown(
                    f"""
                        <div style="flex: 1; text-align: right; padding: 10px; border-radius: 10px; margin-right: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                            <strong>You:</strong> {_past_user_query}
                        <div style="flex: 1; text-align: left; padding: 10px; border-radius: 10px; margin-left: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                            <strong>Chatbot:</strong> {past_bot_reply}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.markdown("No history available yet.")

elif selected_page == "ℹ️ About":
    st.title("ℹ️ About This Chatbot")
    st.markdown("""
    ## Purpose of the Chatbot
    This chatbot was created to assist programmers with Python-specific questions. It is designed to provide accurate and relevant answers based on a predefined dataset, making it a helpful tool for learning Python concepts or troubleshooting programming challenges.

    ## Features
    - **Interactive Q&A**: Users can ask Python-related questions and get instant responses.
    - **Simple Interface**: Designed with Streamlit for ease of use.
    - **Customizable**: You can enhance the chatbot by updating the dataset or improving the logic.

    ## Libraries Used
    Below are the libraries that power this chatbot:

    1. **Pandas**  
       A powerful library for data manipulation and analysis. It is used to structure and preprocess the dataset efficiently.

    2. **scikit-learn**  
       - **TfidfVectorizer**: Converts text data into numerical features using Term Frequency-Inverse Document Frequency (TF-IDF), enabling similarity comparisons.
       - **cosine_similarity**: Computes the similarity between the user query and dataset entries, helping the chatbot select the most relevant response.

    3. **spaCy**  
       A popular NLP library used for text preprocessing, including stop-word removal and tokenization, ensuring better query matching.

    4. **NumPy**  
       Provides numerical computation support, especially for handling arrays and mathematical operations required in text similarity computations.

    5. **Streamlit**  
       A framework for creating interactive web apps. It powers the chatbot's user interface, enabling dynamic user interactions.

    ## How It Works
    1. The user's query is preprocessed using `spaCy` to remove stop words and tokenize text.
    2. The processed query is vectorized using `TfidfVectorizer`.
    3. **Cosine similarity** is calculated between the query vector and dataset vectors.
    4. The most relevant response is selected and displayed to the user.

    ## Limitations
    - The chatbot relies on a static dataset and does not "learn" dynamically.
    - Responses are limited to the scope of the dataset and may not handle complex or unrelated queries well.

    ## Future Improvements
    - Integration with larger datasets for better coverage.
    - Implementation of dynamic learning using advanced NLP models.
    - Adding context-awareness for multi-turn conversations.

    ---
    We hope this chatbot enhances your Python programming journey!
    """)
