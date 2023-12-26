
import os 
from apikey import apikey, HUGAPIKEY
from distutils.command.install_egg_info import safe_name 
from dotenv import load_dotenv
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from Spreads.Smanipulator import SheetManipulator
from openai import OpenAI
import faiss
import json
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
def get_closest_chunks(user_input):
    """
    Obtém os dois trechos mais próximos de um vetor de consulta.

    Args:
        user_input: O vetor de consulta.
        vectorstore: O vector_store.

    Returns:
        Uma lista dos dois trechos mais próximos.
    """
    # Converte a consulta para um vetor.
    query_vector = st.session_state.embeddings.em

    # Faz uma busca no vector_store.
    distances, indices = st.session_state.vectorstore.search(query_vector, 2)
    # Retorna os dois trechos com os índices mais altos.
    return [st.session_state.text_chunks[index] for index in indices]

# def search_reviews(product_description, n=3, pprint=True):
#    embedding = get_embedding(product_description, model='text-embedding-ada-002')
#    st.session_state.vectorstore['similarities'] = st.session_state.vectorstore.ada_embedding.apply(lambda x: cosine_similarity(x, embedding))
#    res = st.session_state.vectorstore.sort_values('similarities', ascending=False).head(n)
#    return res

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=600,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def pesquisarProx(pergunta_do_usuario):
    """
    Searches for the 3 most similar passages in the vectorstore to a given user query.

    Args:
        pergunta_do_usuario (str): The user's query.
        vectorstore (FAISS): The vectorstore containing embedded text chunks.

    Returns:
        list: A list of the 3 most similar passages.
    """

    

    query_vector = get_embedding(pergunta_do_usuario, model="text-embedding-ada-002")  # Get embedding using Hugging Face model

    distances, indices = st.session_state.index.search(query_vector, 8)

    most_similar_passages = [st.session_state.vectorstore.texts[idx] for idx in indices[0]]

    return most_similar_passages
def get_vectorstore(text_chunks):
    embedding = OpenAIEmbeddings()
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    # vectorstore = []
    # for tx in text_chunks:
    #     vectorstore.append(get_embedding(tx, model='text-embedding-ada-002')) 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=st.session_state.embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    st.session_state.opcao = None
    memory = ConversationBufferMemory(
    memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# def output(user_question):
#     instruction = st.session_state.vectorstore.similarity_search_with_score(user_question)
    
#     if st.session_state.opcao == "Sheets":
#         json = handle_sheets_output(user_question, instruction)
#         link = st.session_state.sheetMani.create_or_edit_sheet_with_json(json)
#         st.write("your google shets: \n")
#         st.subheader("Output")
#         st.write(f"Your Google Sheets: {link}")
#         return ""
#     else:
#         return handle_text_output(user_question, instruction)
def output(user_question):
    instruction = st.session_state.vectorstore.similarity_search_with_score(user_question)

    if st.session_state.opcao == "Sheets":
        print("Selected Sheets option")
        json_data = handle_sheets_output(user_question, instruction)
        link = st.session_state.sheetMani.create_or_edit_sheet_with_json(json_data)
        st.write("your google sheets: \n")
        st.subheader("Output")
        st.write(f"Your Google Sheets: {link}")
        return ""
    else:
        print("Selected Text option")
        return handle_text_output(user_question, instruction)
# def handle_sheets_output(user_question):
#     instruction = """
#     Write the response in JSON format, always in JSON [[]] format, as I will use it to create a table. This JSON must represent a table. Then answer any question in JSON{
# """
#     return handle_userinput(instruction + user_question + "}")

def handle_sheets_output(user_question, instruction):
    client = OpenAI()
    model = """
{
  "spreadsheet_name": "Tabela de Preços",
  "sheet_name": "Preços",
  "data": [
    {"Produto": "Item A", "Preço": 10, "Quantidade": 5},
    {"Produto": "Item B", "Preço": 15, "Quantidade": 3},
    {"Produto": "Item C", "Preço": 20, "Quantidade": 2}
  ],
  "colorizers": [
    {"range_name": "A1:C1", "color": {"red": 0.8, "green": 0.8, "blue": 0.4}},
    {"range_name": "A2:C4", "color": {"red": 0.4, "green": 0.7, "blue": 0.4}},
    {"range_name": "D2:D4", "color": {"red": 0.4, "green": 0.4, "blue": 0.8}},
    {"range_name": "E2:E4", "color": {"red": 0.8, "green": 0.4, "blue": 0.8}},
    {"range_name": "F2:F4", "color": {"red": 0.8, "green": 0.8, "blue": 0.8}}
  ]
}
"""
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={ "type": "json_object" },
    messages=[
    {"role": "system", "content": f"{instruction}, Your is a table maker(googleSheets), you must color and edit the cells, make the biggest spreadsheet you can. ALWAYS IN THIS JSON MODE: {model}(this is very important) "},
    {"role": "user", "content": f"{user_question}"}
  ]
)
    return response.choices[0].message.content
    #return response.choices[0].message.content

def handle_text_output(user_question, instruction):
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a helpful assistant. {instruction}"},
        {"role": "user", "content": f"{user_question}"},
    ]
    )
    # return response.choices[0].message.content
    return response.choices[0].message.content

def get_embedding(text, model="text-embedding-ada-002"):
   client = OpenAI()
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    return response
    

        
def on_change_callback(valor_antigo, valor_novo):
    # Verifique se o novo valor está na lista de opções aceitas

    if valor_novo in st.session_state.opcao_aceitavel:
        # Atualize o valor da variável `st.session_state.opcao`
        st.session_state.opcao = valor_novo

    return valor_novo

# def main():
#     st.session_state.opcao = None
#     load_dotenv()
#     os.environ['OPENAI_API_KEY'] = apikey
#     st.session_state.embeddings = OpenAIEmbeddings()
#     st.set_page_config(page_title="Chat with multiple PDFs",
#                        page_icon=":books:")
#     st.session_state.sheetMani = SheetManipulator()
#     # Define the acceptable options
#     st.session_state.opcao_aceitavel = ["Text", "Sheets", "excerpts"]
    
    
    
    
#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None

#     st.header("Chat with multiple PDFs, Sheets and Image :books: :sheets:")
#     user_question = st.text_input("Ask a question about your documents:")
#     if user_question:
#         if st.session_state.vectorstore == None:
#             st.write('please add a pdf to the database')
#         else:
#             instruction = st.session_state.vectorstore.similarity_search_with_score(user_question)
#             if(st.session_state.opcao == "Sheets"):
#                 print("this is a option")
#                 st.write("Selected Sheets option")
#                 json_data = handle_sheets_output(user_question, instruction)
#                 link = st.session_state.sheetMani.create_or_edit_sheet_with_json(json_data)
#                 st.write("your google sheets: \n")
#                 st.subheader("Output")
#                 st.write(f"Your Google Sheets: {link}")
#             if(st.session_state.opcao == "Text"):
#                 st.write(handle_text_output(user_question, instruction))
#             if(st.session_state.opcao == "excerpts"):
#                 st.write(instruction)
            

            
#     with st.sidebar:
#         st.session_state.opcao = st.radio("Output Option", ["Text", "Sheets", "excerpts"])
#         st.subheader("Your documents")
#         pdf_docs = st.file_uploader(
#             "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
#         # #os.environ['OPENAI_API_KEY'] = APIKEY
#         os.environ['OPENAI_API_KEY'] = apikey

#         if st.button("Process"):
#             with st.spinner("Processing"):
#                 # get pdf text
#                 raw_text = get_pdf_text(pdf_docs)

#                 # get the text chunks
#                 st.session_state.text_chunks = get_text_chunks(raw_text)

#                 # create vector store
#                 st.session_state.vectorstore = get_vectorstore( st.session_state.text_chunks)

#                 # create conversation chain
#                 # st.session_state.conversation = get_conversation_chain(
#                 #     st.session_state.vectorstore)
#                 #st.session_state.index = faiss.IndexFlatL2(st.session_state.vectorstore)
#                 # st.write(st.session_state.vectorstore)
        

def main():
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = apikey
    st.session_state.embeddings = OpenAIEmbeddings()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.session_state.sheetMani = SheetManipulator()
    # Define the acceptable options
    st.session_state.opcao_aceitavel = ["Text", "Sheets", "excerpts"]

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Chat with multiple PDFs, Sheets and Image :books: :sheets:")
    user_question = st.text_input("Ask a question about your documents:")

    with st.sidebar:
        st.session_state.opcao = st.radio("Output Option", ["Sheets", "Text", "excerpts"])

    if user_question:
        if st.session_state.vectorstore is None:
            st.write('please add a pdf to the database')
        else:
            instruction = st.session_state.vectorstore.similarity_search_with_score(user_question)
            if st.session_state.opcao == "Sheets":
                print("this is a option")
                st.write("Selected Sheets option")
                json_data = handle_sheets_output(user_question, instruction)
                link = st.session_state.sheetMani.create_or_edit_sheet_with_json(json_data)
                st.write("your google sheets: \n")
                st.subheader("Output")
                st.write(f"Your Google Sheets: {link}")
            elif st.session_state.opcao == "Text":
                st.write(handle_text_output(user_question, instruction))
            elif st.session_state.opcao == "excerpts":
                st.write(instruction)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                st.session_state.text_chunks = get_text_chunks(raw_text)

                # create vector store
                st.session_state.vectorstore = get_vectorstore(st.session_state.text_chunks)

if __name__ == '__main__':
    main()














