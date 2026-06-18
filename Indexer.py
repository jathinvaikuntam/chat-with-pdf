import chromadb
from pdf_processor import read_pdf, chunk_text


client = chromadb.PersistentClient(path="./chroma_db")


def create_collection(collection_name):

    collection = client.get_or_create_collection(name=collection_name)

    return collection


def index_pdf(pdf_path, collection_name):

    pages = read_pdf(pdf_path)

    collection = create_collection(collection_name)

    documents = []
    metadatas = []
    ids = []

    chunk_id = 0

    for page in pages:

        chunks = chunk_text(page["text"])

        for chunk in chunks:

            documents.append(chunk)

            metadatas.append({"page": page["page"]})

            ids.append(str(chunk_id))

            chunk_id += 1

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return len(documents)