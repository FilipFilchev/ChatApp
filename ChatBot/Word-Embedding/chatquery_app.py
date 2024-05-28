#Chat with word-embedding system -> Streamlit UI
import streamlit as st
import pandas as pd
import torch
import faiss
import numpy as np
import pickle
from transformers import AutoTokenizer, AutoModel

# Load knowledge base
with open('knowledge_base.pkl', 'rb') as f:
    knowledge_base = pickle.load(f)
questions = knowledge_base['questions']
answers = knowledge_base['answers']
embeddings = knowledge_base['embeddings']

# Init. FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Init tokenizer and model to query embedding
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModel.from_pretrained("microsoft/DialoGPT-medium")
tokenizer.pad_token = tokenizer.eos_token  # eos_token as pad_token

# generate embeddings for queries 
def generate_embeddings(texts, tokenizer, model):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy()

# Retrieve most similar answer in context
def retrieve_similar_dialogue(query, tokenizer, model, index, questions, answers, k=1):
    query_embedding = generate_embeddings([query], tokenizer, model)
    distances, indices = index.search(query_embedding, k)
    results = [(questions[i], answers[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return results

# Streamlit app
st.set_page_config(page_title="Financial Chatbot", page_icon=":robot_face:", layout="wide", initial_sidebar_state="expanded")

# CSS -- soft dark theme
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #e0e0e0;
    }
    .stTextInput > div > input {
        background-color: #333;
        color: #e0e0e0;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
    }
    .css-1d391kg {
        background-color: #333;
        color: #e0e0e0;
    }
    .css-1lcbmhc {
        color: #e0e0e0;
    }
    .css-1adrfps {
        color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Financial Analysis Chatbot / Финансов Асистент")

# Input box for user query
query = st.text_input("Задайте въпрос свързан с финансовия пазар:  ")

# Button to submit the query
if st.button("Изпрати"):
    if query:
        results = retrieve_similar_dialogue(query, tokenizer, model, index, questions, answers, k=1)
        st.subheader("Отговор")
        for result in results:
            st.write(f">>>  {result[0]}")
            #st.write(f"**Answer:** {result[1]}")
            st.write(f"**Ниво на сходство:** {result[2]:.5f}")
    else:
        st.warning("Моля задайте въпрос.")

# To run the app, use: streamlit run chatquery_app.py
