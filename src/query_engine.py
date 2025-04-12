
from llama_index.core import get_response_synthesizer
import logging

from llama_index.core.retrievers import AutoMergingRetriever
from prompt.first_aid_template import richprompt, prompttemp
from index_data import load_existing_index
from config_loader import load_config

config = load_config()

def query_index(query):
    """Loads the FAISS index and queries it with AutoMergingRetriever using a strict first aid prompt."""

    print(f"\nUser Query: {query}\n")

    # Load the index
    index = load_existing_index()
    if index is None:
        logging.error("❌ Failed to load index. Ensure it's created before querying.")
        return None

    # Set up retriever
    storage_context = index.storage_context
    base_retriever = index.as_retriever(similarity_top_k=config['similarity_k'])
    retriever = AutoMergingRetriever(base_retriever, storage_context, verbose=True)

    raw_documents = retriever.retrieve(query)

    if not raw_documents:
        logging.warning(f"⚠️ No documents retrieved for query: '{query}'")
        return "No relevant information found."

    # Print retrieved documents for debugging
    # logging.info(f"📄 Retrieved {len(raw_documents)} documents for query: '{query}'")
    # print("📄 Retrieved Documents:")
    # for doc in raw_documents:
    #     print(doc)

    # Create synthesizer and query engine
    response_synthesizer = get_response_synthesizer(response_mode=config['response_mode'])
    query_engine = index.as_query_engine(
        prompt_template=richprompt,
        response_synthesizer=response_synthesizer
    )

    response = query_engine.query(query)
   
    print("\nResponse from query engine:")
    print(response)


    return response

if __name__ == "__main__":
    query = "What first aid should be provided when a person is found unresponsive after being exposed to extreme heat, with hot, dry skin?"
    response = query_index(query)
