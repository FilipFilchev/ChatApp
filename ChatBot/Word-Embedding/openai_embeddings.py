
import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# import openai

# # Assume you have an API key set in your environment
# openai.api_key = 'your-api-key'

# # Example dataset
# financial_data = {
#   "inflation": "Inflation is the rate at which the general level of prices for goods and services is rising.",
#   "bull market": "A bull market refers to a financial market of a group of securities in which prices are rising or are expected to rise."
# }

# # Create embeddings for your data
# financial_data_embeddings = {key: openai.Embedding.create(input=value)["data"] for key, value in financial_data.items()}

# def get_closest_data(query):
#     query_embedding = openai.Embedding.create(input=query)["data"]
#     # Find the closest embedding in your dataset (this part is simplified)
#     closest = min(financial_data_embeddings.items(), key=lambda x: openai.util.cosine_similarity(query_embedding, x[1]))
#     return financial_data[closest[0]]

# # Example query
# response = get_closest_data("What is a rising market called?")
# print(response)

# ##OR SIMPLY CREATE A CUSTOM GPT in the OPENAI PLATFORM