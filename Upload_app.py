import streamlit as st
import os

from Indexer import index_pdf
from search_engine import search_pdf


st.title("📚 Chat With PDF")


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file:

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded")


    collection_name = st.text_input(
        "Collection Name",
        value="my_pdf"
    )

    if st.button("Index PDF"):

        count = index_pdf(
            file_path,
            collection_name
        )

        st.success(
            f"{count} chunks indexed successfully!"
        )


st.divider()


query = st.text_input(
    "Ask a Question"
)


collection_name = st.text_input(
    "Search Collection",
    value="my_pdf"
)


if st.button("Search"):

    results = search_pdf(
        collection_name,
        query
    )

    documents = results["documents"][0]
    metadata = results["metadatas"][0]

    st.subheader("Results")

    for doc, meta in zip(documents, metadata):

        st.write(
            f"📄 Page {meta['page']}"
        )

        st.write(doc)

        st.divider()