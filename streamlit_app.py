import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime
import pytz
from info import info

# Function to handle default chatbot behavior
def default_chat():
    if 'chat_session' not in st.session_state:
        model = genai.GenerativeModel('gemini-1.5-pro')
        st.session_state.chat_session = model.start_chat()
        st.session_state.chat_history = []

    # Add an input text box for the user to enter a prompt
    prompt = st.text_input("What's on your mind?:", key="input_prompt")

    # Add an Enter button for submitting the input
    enter_button = st.button("Ask ChadGPT")

    # Capture Enter key press event or button click event
    if (prompt and st.session_state.get('last_input', None) != prompt) or (enter_button and prompt):
        st.session_state.last_input = prompt
        response = st.session_state.chat_session.send_message(prompt)
        handle_response(prompt, response)
    elif enter_button and not prompt:
        st.warning("Please enter a message first.")

# Function to handle chat response
def handle_response(prompt, response):
    # Get current time in GMT+8
    ph_time = pytz.timezone('Asia/Manila')
    gmt8_now = datetime.now(pytz.utc).astimezone(ph_time)
    timestamp = gmt8_now.strftime("%B %d, %Y - %I:%M:%S%p")

    # Format user prompt and chatbot response for conversation history
    formatted_entry = f"{timestamp}\n\nYou asked: {prompt}\n\nChadGPT replied:\n{response.text}\n"

    # Add a divider after each conversation entry
    divider = "---------------------------------------------------\n"
    formatted_entry_with_divider = f"{formatted_entry}{divider}"

    # Display only the chatbot response without the prompt and timestamp, left-aligned
    st.write(response.text)  # Use st.write for left-aligned text

    # Append full entry with timestamp to conversation history
    st.session_state.chat_history.append(formatted_entry_with_divider)

# Function to toggle visibility of chat history
def toggle_history_visibility():
    if st.button("Show History"):
        st.session_state.show_history = not st.session_state.get("show_history", False)

# Configure Gemini API with the API key loaded from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the Streamlit app
def main():
    st.set_page_config(page_title="Gemini Chat Demo")
    st.header("🤖ChadGPT: Your Intelligent Chat Assistant")
    st.write("""
    Welcome to **ChadGPT**, your versatile and intelligent chat assistant powered by advanced generative AI technology! 
    ChadGPT is designed to assist you with a wide range of tasks, including answering questions, providing detailed explanations, generating creative content, and helping with various information needs.
""")

    info()

    # Default chatbot behavior
    default_chat()

    # Toggle visibility of chat history
    toggle_history_visibility()

    if st.session_state.get("show_history"):
        st.subheader("Conversation History:")
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            for entry in st.session_state.chat_history:
                st.markdown(f"<p style='text-align: center;'>{entry}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center;'>None</p>", unsafe_allow_html=True)

    if st.button("Reset Conversation"):
        model = genai.GenerativeModel('gemini-1.5-pro')
        st.session_state.chat_session = model.start_chat()
        st.session_state.chat_history = []  # Clear history when resetting

if __name__ == "__main__":
    main()
