# High level Embedding example storing and reusing a knowledge base.
import pandas as pd
from transformers import AutoModel, AutoTokenizer
import torch
import faiss
import numpy as np
import pickle

# read dataset
df = pd.read_csv('dataset.csv')
print("Columns in dataset:", df.columns)

# # Verify column names
# assert 'questions' in df.columns, "The column 'questions' does not exist in the CSV file."
# assert 'answers' in df.columns, "The column 'answer' does not exist in the CSV file."

# Init
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModel.from_pretrained("microsoft/DialoGPT-medium")
# eos_token as pad_token
tokenizer.pad_token = tokenizer.eos_token

# generate embeddings
def generate_embeddings(texts, tokenizer, model):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Get the mean of the hidden states
    return embeddings.cpu().numpy()

# Gen. embeddings for the questions dataframe
questions = df['questions'].tolist()
question_embeddings = generate_embeddings(questions, tokenizer, model)

# Store embeddings & original data
knowledge_base = {'questions': questions, 'answers': df['answers'].tolist(), 'embeddings': question_embeddings}

# Saving knowledge-base
with open('knowledge_base.pkl', 'wb') as f:
    pickle.dump(knowledge_base, f) #using pickle lib


