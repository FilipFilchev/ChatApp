from sentence_transformers import SentenceTransformer, util
import pandas as pd

class ChatModule:
    def __init__(self, data_path):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.data = pd.read_csv(data_path)
        self.embeddings = self.model.encode(self.data['Question'], convert_to_tensor=True)

    def get_answer(self, query):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        top_result = scores.argmax()
        return self.data.iloc[top_result]['Answer']


#requirement: pip install torch==2.0
"""or in requirements.txt --> torch==2.0 
pip install -r requirements.txt
pip show torch
"""


# import streamlit as st
# import pandas as pd
# import faiss
# import pickle
# import torch
# from transformers import GPT2Tokenizer, GPT2Model

# # Load precomputed data and models
# @st.cache(allow_output_mutation=True)
# def load_data():
#     with open('/mnt/data/question_embeddings.pkl', 'rb') as f:
#         embeddings = pickle.load(f)
#     index = faiss.read_index('/mnt/data/faiss_index')
#     data = pd.read_csv('/mnt/data/ChatBot_QA.csv')
#     return embeddings, index, data

# embeddings, index, data = load_data()
# questions = data['Question'].tolist()
# answers = data['Answer'].tolist()

# # Initialize tokenizer and model
# tokenizer = GPT2Tokenizer.from_pretrained('microsoft/DialoGPT-medium')
# model = GPT2Model.from_pretrained('microsoft/DialoGPT-medium')
# model.eval()

# # Embedding function for queries
# def embed_query(query):
#     inputs = tokenizer(query, return_tensors='pt', truncation=True, max_length=512)
#     outputs = model(**inputs).last_hidden_state
#     return outputs.mean(dim=1).squeeze().numpy()

# # Function to retrieve the most relevant answer
# def get_answer(query_embedding):
#     D, I = index.search(np.array([query_embedding]), k=1)  # search for the top 1 similar item
#     closest_question_index = I[0][0]
#     return questions[closest_question_index], answers[closest_question_index]

# # Streamlit UI setup
# st.title('Financial Chatbot')
# user_query = st.text_input("Ask a financial question:")

# if st.button('Send'):
#     if user_query:
#         query_embedding = embed_query(user_query)
#         question, response = get_answer(query_embedding)
#         st.write("Question:", question)
#         st.write("Answer:", response)
