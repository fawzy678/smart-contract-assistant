import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import gradio as gr
from dotenv import load_dotenv

load_dotenv(os.path.join(BASE_DIR, ".env"))

if not os.getenv("GROQ_API_KEY"):
    print("ERROR: GROQ_API_KEY not found in .env file")
    sys.exit(1)

print("API Key loaded")

from utils.loader import load_contract_from_string, load_contract_from_file
from vectorstore.store import build_vectorstore
from chains.summary_chain import summarize
from chains.qa_chain import answer, clear_history

_vectorstore = None

def handle_file_upload(file):
    if file is None:
        return ""
    try:
        return load_contract_from_file(file.name)
    except Exception as e:
        return f"Error reading file: {str(e)}"

def handle_summarize(contract_text):
    global _vectorstore
    if not contract_text.strip():
        return "Please paste or upload a smart contract first.", ""
    try:
        text = load_contract_from_string(contract_text)
        _vectorstore = build_vectorstore(text)
        summary = summarize(text)
        return summary, "✅ Contract loaded successfully."
    except Exception as e:
        return f"Error: {str(e)}", ""

def handle_qa(question):
    global _vectorstore
    if _vectorstore is None:
        return "Please load a contract first in the Summary tab."
    if not question.strip():
        return "Please type a question."
    try:
        return answer(question, _vectorstore)
    except Exception as e:
        return f"Error: {str(e)}"

def handle_clear():
    clear_history()
    return ""

with gr.Blocks(title="Smart Contract Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔐 Smart Contract Summary & Q&A Assistant")

    with gr.Row():
        with gr.Column(scale=2):
            contract_input = gr.Textbox(
                label="📋 Smart Contract",
                lines=14,
                placeholder="pragma solidity ^0.8.0;\n\ncontract MyContract { ... }"
            )
        with gr.Column(scale=1):
            gr.Markdown("### 📁 Upload Contract File")
            gr.Markdown("Supports: `.sol` `.txt` `.pdf` `.docx`")
            file_upload = gr.File(
                label="Upload File",
                file_types=[".sol", ".txt", ".pdf", ".docx"],
            )
            upload_btn = gr.Button("📥 Load File", variant="secondary")
            upload_btn.click(
                fn=handle_file_upload,
                inputs=[file_upload],
                outputs=[contract_input]
            )

    with gr.Tab("📄 Summarize"):
        summarize_btn = gr.Button("🔍 Generate Summary", variant="primary")
        summary_output = gr.Textbox(label="📝 Summary", lines=12, interactive=False)
        status_output = gr.Textbox(label="Status", lines=1, interactive=False)
        summarize_btn.click(
            fn=handle_summarize,
            inputs=[contract_input],
            outputs=[summary_output, status_output]
        )

    with gr.Tab("💬 Q&A"):
        gr.Markdown("*Load a contract first in the Summary tab.*")
        question_input = gr.Textbox(label="❓ Your Question", lines=2,
                                    placeholder="Who is the owner? What are the risks?")
        with gr.Row():
            qa_btn = gr.Button("💡 Get Answer", variant="primary")
            clear_btn = gr.Button("🗑️ Clear History", variant="secondary")
        qa_output = gr.Textbox(label="🤖 Answer", lines=8, interactive=False)
        qa_btn.click(fn=handle_qa, inputs=[question_input], outputs=[qa_output])
        clear_btn.click(fn=handle_clear, outputs=[qa_output])

demo.launch(show_error=True)