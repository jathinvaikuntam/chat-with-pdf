import chromadb


client = chromadb.PersistentClient(path="./chroma_db")


def search_pdf(collection_name, question):

    collection = client.get_collection(name=collection_name)

    results = collection.query(query_texts=[question], n_results=3)

    return results