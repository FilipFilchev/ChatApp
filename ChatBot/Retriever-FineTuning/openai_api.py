#OR JUST USE THE OPENAI PLATFORM as you can use hugging face as well 
# TO UPLOAD DATASETS and FINETUNE the model

# import os
# from dotenv import load_dotenv
# import streamlit as st
# import openai
# from openai import OpenAI

# # Load environment variables from .env file
# load_dotenv()

# client = OpenAI()

# # Get the OpenAI API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# print(OPENAI_API_KEY)

# # Initialize the OpenAI API client
# openai.api_key = OPENAI_API_KEY

# st.title("GPT-4o Chatbot")

# # Initialize session state history
# if "history" not in st.session_state:
#     st.session_state.history = []

# # Function to generate a response from GPT-4o
# def generate_response(prompt):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  
#         messages = [
#             {"role":"system", "content":"You are AI assistant..."},
#             {"role":"user", "content":prompt}
#         ],
#         max_tokens = 200,
#     )
#     return response.choices[0].text.strip()

# # User input
# user_input = st.text_input("You:", key="input")

# if st.button("Send"):
#     if user_input:
#         bot_response = generate_response(user_input)
#         st.session_state.history.append({"user": user_input, "bot": bot_response})

# # Display chat history
# for chat in st.session_state.history:
#     st.write(f"You: {chat['user']}")
#     st.write(f"Bot: {chat['bot']}")




import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
load_dotenv()
client = OpenAI()

# Get the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(OPENAI_API_KEY)

openai.api_key = OPENAI_API_KEY

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Who won the world series in 2020?"}
  ]
)
print(response.choices[0].message.content)

