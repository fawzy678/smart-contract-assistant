from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def summarize(contract_text: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert smart contract auditor. Analyze the following Solidity smart contract and provide a clear structured summary including: purpose, key functions, state variables, access controls, and any potential risks."),
        ("human", "Smart Contract:\n\n{contract}"),
    ])
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"contract": contract_text})