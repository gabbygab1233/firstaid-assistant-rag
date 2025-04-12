import os
import sys

# Ensure src directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import logging
import pandas as pd
from extract_text import extract_text_from_pdf
from clean_text import clean_text
from index_data import create_index, get_embedding_dimension
from ingest_data import save_markdown

from config_loader import load_config

# Load configuration
config = load_config()

MD_PATH = config["paths"]["md_path"]
PDF_FILE = config["paths"]["pdf_file"][0]

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline(pdf_file_path: str):
    """Runs the full RAG pipeline."""
    logging.info("🚀 Starting pipeline...")

    # Step 1: Extract text
    extracted_text = extract_text_from_pdf(pdf_file_path)
    if isinstance(extracted_text, list):
        extracted_text = "\n\n".join([doc.text for doc in extracted_text])
    logging.info("✅ Text extraction completed.")

    # Step 2: Clean text
    cleaned_text = clean_text(extracted_text)
    logging.info("🧹 Text cleaned successfully.")

    # Step 3: Save cleaned text (optional step)
    save_markdown(cleaned_text)
    logging.info("📝 Cleaned text saved to markdown.")

    # Step 4: Get embedding dimension
    embedding_dim = get_embedding_dimension()
    if embedding_dim is None:
        logging.error("🚨 Could not determine embedding dimension. Exiting.")
        exit(1)

    # Step 5: Create index
    index = create_index(embedding_dim)
    if index:
        logging.info("🎉 Index is ready for use.")
    else:
        logging.error("🚨 Index creation failed. Exiting.")
        exit(1)


if __name__ == "__main__":
    run_pipeline(PDF_FILE)
