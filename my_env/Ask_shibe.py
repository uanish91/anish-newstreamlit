# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import langchain
page_config = st.set_page_config(page_title="🦜🔗 Ask the Doc App")
import tiktoken
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA



open_api_key = st.sidebar.text_input('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')

#Define a custom generate_response function
def generate_response(uploaded_file, openai_api_key, query_text):
    if uploaded_file is not None:
        documents = [uploaded_file.read().decode()]

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.create_documents(documents)
    #Select embeddings:
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    #Create a vectorstore from documents
    db = Chroma.from_documents(texts, embeddings)
    #Create retriever interface
    retriever = db.as_retriever()
    #Create QA chain
    qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type = 'stuff', retriever = retriever)
    return qa.run(query_text)

# Page title
st.title('🦜🔗 Ask the Doc App')

#Add input widgets to allow users to upload text files.
uploaded_file = st.file_uploader('Upload an article', type='txt')

#Query text
query_text= st.text_input('Enter your question', placeholder='Please provide a short summary', disabled=not uploaded_file)

# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    openai_api_key = st.text_input('OpenAI API Key', type='password', disabled=not (uploaded_file and query_text))
    submitted = st.form_submit_button('Submit', disabled=not(uploaded_file and query_text))
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(uploaded_file, openai_api_key, query_text)
            result.append(response)
            del openai_api_key

if len(result):
    st.info(response)
