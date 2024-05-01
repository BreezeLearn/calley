from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyDqnLVkETKo7wQgPXN56QON3AGEm4qvTTU"

def gemini_embedding(text):

    llm = GoogleGenerativeAI(model="gemini-pro")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.create_documents([text])
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(texts, embeddings)

    retriever = db.as_retriever()



    tool = create_retriever_tool(
        retriever,
        "search_state_of_union",
        "Searches and returns excerpts from the 2022 State of the Union.",
    )
    
