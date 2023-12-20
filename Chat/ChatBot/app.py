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
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    style = """
    .user_message {
        background-color: #eee;
        border-radius: 5px;
        padding: 10px;
    }

    .bot_message {
        background-color: #ccc;
        border-radius: 5px;
        padding: 10px;
    }
    """

    st.write(style, unsafe_allow_html=True)

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                f"""
                <div class="user_message">
                    {message.content}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.write(
                f"""
                <div class="bot_message">
                    {message.content}
                </div>
                """, unsafe_allow_html=True)
        


def main():

    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        if st.session_state.conversation == None:
            st.write('please add a pdf to the database')
            
        else:
            handle_userinput(user_question)
        
            
        

            

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        # #os.environ['OPENAI_API_KEY'] = APIKEY
        os.environ['OPENAI_API_KEY'] = apikey

        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
















# import os 
# from apikey import apikey, HUGAPIKEY
# from distutils.command.install_egg_info import safe_name 
# from dotenv import load_dotenv
# import streamlit as st 
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain, SimpleSequentialChain
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.memory import ConversationBufferMemory
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import ConversationalRetrievalChain



# def get_pdf_text(pdfs):
#     text = ""
#     for pdf in pdfs:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

# def get_chunks(allText):
#     textSpliter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size = 1000,
#         chunk_overlap = 200,
#         length_function = len
#     )
#     chunks = textSpliter.split_text(allText)
#     return chunks

# def extractEmbeding(text_chunks):
#     #embeddings = OpenAIEmbeddings()
#     embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     return vectorstore
# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI()
#     # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

#     memory = ConversationBufferMemory(
#         memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain

# def handle_userinput(user_question):
#     response = st.session_state.conversation({'question': user_question})
#     st.session_state.chat_history = response['chat_history']

#     for i, message in enumerate(st.session_state.chat_history):
#         if i % 2 == 0:
#             st.write(message.content)
#         else:
#             st.write(message.content)


# def busca_trecho_resposta(pergunta, vetor_store):
#   """
#   Busca o trecho de resposta mais relevante no vetorstore.

#   Args:
#     pergunta: A pergunta do usuário.
#     vetor_store: O vetorstore com as representações vetoriais dos trechos de texto.

#   Returns:
#     O trecho de resposta mais relevante.
#   """

#   # Cria uma representação vetorial para a pergunta.
#   embedding_pergunta = vetor_store.get_vector(pergunta)

#   # Busca os trechos de resposta mais relevantes.
#   trechos_resposta = vetor_store.get_closest(embedding_pergunta, k=1)

#   # Retorna o primeiro trecho de resposta.
#   return trechos_resposta[0][0]
 
# # def OnPrompt(prompt, template):
# #     if 
# #     textTo = busca_trecho_resposta(prompt, st.session_state.vector_store)
# #     Question = "Based on" + textTo + "reply" + prompt
# #     response = template.run(topic=prompt, input=prompt)
# #     st.write(response)

# def main():
#     st.set_page_config(page_title="charBot with PDFs", page_icon=":books:")
#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = None
    
# #os.environ['OPENAI_API_KEY'] = APIKEY
#     os.environ['OPENAI_API_KEY'] = apikey
#     llm = OpenAI(temperature=0.9)
#     #app framework
#     st.title('Teste')
#     prompt = st.text_input('teste aqui')

#     #set addition of PDFs config
#     load_dotenv()
#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = None
#     with st.sidebar:
#         st.subheader("Your documents")
#         pdf_docs = st.file_uploader(
#             "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
#         if st.button("Process"):
#             with st.spinner("Processing"):
#                 # get pdf text
#                 raw_text = get_pdf_text(pdf_docs)

#                 # get the text chunks
#                 text_chunks = get_chunks(raw_text)

#                 # create vector store
#                 vectorstore = extractEmbeding(text_chunks)

#                 # create conversation chain
#                 st.session_state.conversation = get_conversation_chain(
#                     vectorstore)
            
           
#     #template
#     java_template = PromptTemplate(
#         input_variables = ['topic'],
#         template = "write a Java program for make this: {topic}"
#     )
#     javaScript_template = PromptTemplate(
#         input_variables = ['topic'],
#         template = "write a Java program for make this: {topic}"
#     )

#     pdfSeach_template = PromptTemplate(

#         input_variables = ['topic'],
#         template = "{topic}"
#     )
#     java_chain = LLMChain(llm= llm, prompt=java_template, verbose=True)
#     javaScript_chain = LLMChain(llm= llm, prompt=javaScript_template, verbose=True)
#     sequential_chain = SimpleSequentialChain(chains=[java_chain, javaScript_chain], verbose=True)
#     #sequential_pdf_TextChain = SimpleSequentialChain(chains=[pdfSeach_template], verbose=True)
#     #llms

#     if prompt:
#         handle_userinput(prompt)
        

# if __name__ == '__main__':
#   main()