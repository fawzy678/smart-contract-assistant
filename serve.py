# serve.py — LangServe + FastAPI Local Deployment

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

from fastapi import FastAPI
from langserve import add_routes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(
    title="Smart Contract Assistant API",
    description="LangServe API for Smart Contract Summary & Q&A",
    version="1.0.0",
)

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

summary_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert smart contract auditor. "
     "Analyze the Solidity smart contract and provide a structured summary "
     "including: purpose, key functions, state variables, access controls, "
     "and potential risks."
    ),
    ("human", "Smart Contract:\n\n{contract}"),
])

summary_chain = summary_prompt | llm | StrOutputParser()

add_routes(app, summary_chain, path="/summary")

@app.get("/")
def root():
    return {
        "message": "Smart Contract Assistant API",
        "endpoints": {
            "summary": "POST /summary/invoke",
            "docs": "GET /docs",
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)