from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.rag.retriever import get_retriever
from dotenv import load_dotenv

load_dotenv()

def format_chunks(chunks):
    return "\n\n".join(chunk.page_content for chunk in chunks)

def get_rag_chain():
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful assistant that answers questions 
based only on the provided context. If the answer is not in the context, 
say "I don't have that information in the documents provided."

Context:
{context}

Question: {question}

Answer:"""
    )

    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0
    )

    retriever = get_retriever()

    chain = (
        {"context": retriever | format_chunks, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

def ask_question(question):
    print(f"\nQuestion: {question}")
    chain = get_rag_chain()
    answer = chain.invoke(question)
    print(f"Answer: {answer}")
    return answer