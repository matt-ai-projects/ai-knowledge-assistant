from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"

def get_retriever():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    return retriever

def retrieve_chunks(query):
    retriever = get_retriever()
    chunks = retriever.invoke(query)
    return chunks