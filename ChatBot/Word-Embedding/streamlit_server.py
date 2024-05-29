# import streamlit as st
# from embeddings_retriever import ChatModule

# # Initialize chat module
# chat = ChatModule('dataset.csv')

# st.title('Financial Chatbot')

# user_input = st.text_input("Ask a financial question:")
# if user_input:
#     response = chat.get_answer(user_input)
#     st.text_area("Answer:", value=response, height=200)


import streamlit as st
from embeddings_retriever import ChatModule

# Initialize chat module
chat = ChatModule('./dataset.csv')

# Set page config for wider page and dark theme
st.set_page_config(page_title='Financial Chatbot', layout='wide', initial_sidebar_state='collapsed')
st.markdown("""
<style>
    .css-18e3th9 {
        padding-top: 0rem;
        padding-bottom: 10rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit theme customization for soft dark mode
st.markdown("""
<style>
    body {
        color: #fff;
        background-color: #0e1117;
    }
    .stTextInput>div>div>input {
        color: #d1d1d1;
    }
    .css-2trqyj {
        background-color: #242731;
    }
    .css-hi6a2p {
        max-width: 800px;
        margin: auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        color: #ffffff;
        border: 2px solid #4caf50;
        background-color: #4caf50;
    }
</style>
""", unsafe_allow_html=True)

st.title('Financial Chatbot')
col1, col2 = st.columns([3, 1])
user_input = col1.text_input("Ask a financial question:", key="question")

if col2.button('Send'):
    if user_input:
        response = chat.get_answer(user_input)
        st.text_area("Answer:", value=response, height=150, key="answer")


#streamlit run streamlit_server.py