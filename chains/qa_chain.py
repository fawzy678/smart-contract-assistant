from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vectorstore.store import retrieve

chat_history = []

def is_contract_related(question: str) -> bool:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a classifier. Answer ONLY with 'yes' or 'no'.\n"
         "Is the following question related to smart contracts, blockchain, "
         "Solidity, DeFi, tokens, or code auditing?"
        ),
        ("human", "{question}"),
    ])
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"question": question}).strip().lower()
    return result.startswith("yes")

def answer(question: str, vectorstore) -> str:
    global chat_history

    if not is_contract_related(question):
        return (
            "⚠️ Sorry, I can only answer questions about smart contracts. "
            "Please ask something related to the contract you uploaded."
        )

    context = retrieve(question, vectorstore)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    history_text = "\n".join([
        f"{'User' if i % 2 == 0 else 'Assistant'}: {msg}"
        for i, msg in enumerate(chat_history[-6:])
    ])

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an expert smart contract auditor. "
         "Use the contract excerpts to answer accurately. "
         "If the answer is not in the excerpts, say so clearly.\n\n"
         "Contract excerpts:\n{context}\n\n"
         "Previous conversation:\n{history}"
        ),
        ("human", "{question}"),
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "context": context,
        "question": question,
        "history": history_text,
    })

    chat_history.append(question)
    chat_history.append(response)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    return response

def clear_history():
    global chat_history
    chat_history = []