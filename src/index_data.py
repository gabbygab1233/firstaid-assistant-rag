import os
import logging
import faiss
from llama_index.core import Document, StorageContext, VectorStoreIndex, load_index_from_storage, Settings
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from config_loader import load_config


config = load_config()

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Set base directory and file paths
MD_PATH = config["paths"]["md_path"]
PERSIST_DIR = config["paths"]["vector_dir"]


Settings.embed_model = OllamaEmbedding(model_name=config['embed'])
Settings.llm = Ollama(model=config['llm'], request_timeout=360.0)

def get_embedding_dimension():
    """Automatically detects the embedding dimension."""
    try:
        return len(Settings.embed_model.get_text_embedding("Test embedding dimension"))
    except Exception as e:
        logging.error(f"❌ Error detecting embedding dimension: {e}")
        return None

def load_cleaned_text():
    """Loads the cleaned text from the Markdown file."""
    if not os.path.exists(MD_PATH):
        logging.error("❌ Cleaned Markdown file not found! Run ingest_data.py first.")
        return None
    with open(MD_PATH, "r", encoding="utf-8") as file:
        return file.read()

def create_index(embedding_dim):
    """Creates and saves the FAISS index."""
    text = load_cleaned_text()
    if not text:
        logging.error("⚠️ Cannot create index. No valid text found.")
        return None

    documents = [Document(text=text)]


    faiss_index = faiss.IndexFlatL2(embedding_dim)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        embed_model=Settings.embed_model
    )

    index.storage_context.persist(persist_dir=PERSIST_DIR)
    return index

def load_existing_index():
    """Loads the FAISS index from storage if it exists."""
    if not os.path.exists(PERSIST_DIR):
        logging.error("❌ No existing FAISS index found. Create an index first.")
        return None

    try:
        vector_store = FaissVectorStore.from_persist_dir(PERSIST_DIR)
        storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context=storage_context)
    except Exception as e:
        logging.error(f"❌ Failed to load index: {e}")
        return None

if __name__ == "__main__":
    embedding_dim = get_embedding_dimension()
    if embedding_dim is None:
        logging.error("🚨 Could not determine embedding dimension. Exiting.")
        exit(1)

    index = load_existing_index() or create_index(embedding_dim)
    if index:
        logging.info("🎉 Index is ready for use.")
    else:
        logging.error("🚨 Index creation failed. Exiting.")
        exit(1)
