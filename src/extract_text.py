import os
import logging
from llama_cloud_services import LlamaParse
from config_loader import load_config
from llama_index.core import SimpleDirectoryReader


config = load_config()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts structured text from a PDF file using LlamaParse, with SimpleDirectoryReader as a fallback."""
    api_key = config["LLAMA_CLOUD_API_KEY"]
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    markdown_content = f"## {os.path.basename(pdf_path)}\n\n"

    try:
        # Attempt extraction with LlamaParse
        parser = LlamaParse(api_key=api_key)
        documents = parser.load_data(pdf_path)
        logging.info(f"🔍 LlamaParse extracted {len(documents)} documents.")

    except Exception as llama_error:
        logging.error(f"⚠️ LlamaParse failed: {llama_error}. Switching to SimpleDirectoryReader...")
        try:
            documents = SimpleDirectoryReader("./data").load_data()
        except Exception as reader_error:
            logging.error(f"❌ SimpleDirectoryReader failed: {reader_error}")
            return ""  # Return empty if both methods fail

    return documents  # Return raw extracted documents

if __name__ == "__main__":
    pdf_path = "../data/r41041rgv10-first-aid-reference-guide.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    print("Extracted Text:", extracted_text[:500])  