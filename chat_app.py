import os
import tempfile

import streamlit as st
import chromadb

import google.generativeai as genai

from dotenv import load_dotenv
from Indexer import index_pdf

# --------------------------
# GEMINI SETUP
# --------------------------

load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# --------------------------
# STREAMLIT PAGE
# --------------------------

st.set_page_config(
    page_title="Chat With PDF",
    page_icon="📚"
)

st.title("📚 Chat With PDF")
st.write(
    "Upload a PDF and ask questions."
)

# --------------------------
# SESSION STATE
# --------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------
# SIDEBAR
# --------------------------

with st.sidebar:

    st.header("PDF Upload")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    collection_name = st.text_input(
        "Collection Name",
        value=st.text_input("Enter collection name:",
        
        value = "my_pdf" 
        
        )
        
    )

    if st.button("Index PDF"):

        if uploaded_file:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp:

                tmp.write(
                    uploaded_file.read()
                )

                temp_path = tmp.name

            with st.spinner(
                "Indexing PDF..."
            ):

                total_chunks = index_pdf(
                    temp_path,
                    collection_name
                )

            st.success(
                f"Indexed {total_chunks} chunks"
            )

        else:

            st.warning(
                "Upload a PDF first."
            )

# --------------------------
# CHROMA COLLECTION
# --------------------------

def get_collection(name):

    client = chromadb.PersistentClient(
        path="chroma_db"
    )

    return client.get_collection(name)

# --------------------------
# RAG RETRIEVAL
# --------------------------

def retrieve_chunks(
    question,
    collection_name
):

    collection = get_collection(
        collection_name
    )

    results = collection.query(
        query_texts=[question],
        n_results=5
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas

# --------------------------
# GEMINI ANSWER
# --------------------------

def ask_gemini(
    question,
    documents,
    metadatas
):

    context = ""

    for doc, meta in zip(documents, metadatas):

        context += (
            f"\n[Page {meta['page']}]\n"
            f"{doc}\n"
        )

    prompt = f"""
You are a PDF assistant.

Answer ONLY from the context.

If answer is not present,
say:

"I don't see that in the document."

Context:
{context}

Question:
{question}

Include page numbers when possible.
"""

    response = model.generate_content(
        prompt
    )

    return response.text

# --------------------------
# DISPLAY CHAT
# --------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# --------------------------
# CHAT INPUT
# --------------------------

question = st.chat_input(
    "Ask about the PDF..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    try:

        docs, metas = retrieve_chunks(
            question,
            collection_name
        )

        answer = ask_gemini(
            question,
            docs,
            metas
        )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)

            with st.expander(
                "View Source Chunks"
            ):

                for doc, meta in zip(
                    docs,
                    metas
                ):

                    st.markdown(
                        f"### Page {meta['page']}"
                    )

                    st.write(doc)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception:

        st.error(
            "Please index a PDF first."
        )

# --------------------------
# CLEAR CHAT
# --------------------------

if st.sidebar.button(
    "Clear Chat"
):

    st.session_state.messages = []

    st.rerun()