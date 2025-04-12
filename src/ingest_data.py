import os
import logging
from extract_text import extract_text_from_pdf
from clean_text import clean_text
from config_loader import load_config


config = load_config()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


MD_PATH = config["paths"]["md_path"]
PDF_FILE= config["paths"]["pdf_file"][0]


def process_and_save_text(pdf_path: str):
    """Processes extracted text and saves it to a Markdown file."""
    raw_documents = extract_text_from_pdf(pdf_path)

    markdown_content = f"## {os.path.basename(pdf_path)}\n\n"

    for doc in raw_documents:
        content = clean_text(doc.text)
        if not is_relevant_section(content):
            continue
        
        title = doc.metadata.get("title", "").strip()
        if not title or title.lower() == "untitled section":
            title = " ".join(content.split()[:6]) + "..."
        
        markdown_content += f"### {title}\n\n{content}\n\n"

    if markdown_content.strip() != f"## {os.path.basename(pdf_path)}":
        save_markdown(markdown_content)
    else:
        logging.error("❌ No relevant text extracted from PDF.")

def save_markdown(content: str):
    """Saves processed text to a Markdown file."""
    try:
        os.makedirs(os.path.dirname(MD_PATH), exist_ok=True) 
        with open(MD_PATH, "w", encoding="utf-8") as md_file:
            md_file.write(content)
        logging.info(f"📂 Extracted text saved: {MD_PATH}")
    except Exception as e:
        logging.error(f"❌ Failed to save Markdown: {e}")

def process_pdf():
    """Processes a single PDF and saves the extracted text."""
    pdf_path = os.path.join(os.path.dirname(__file__), PDF_FILE[0])  
    process_and_save_text(pdf_path)



if __name__ == "__main__":
   
    extracted_text = extract_text_from_pdf(PDF_FILE)
    
    if isinstance(extracted_text, list):
        extracted_text = "\n\n".join([doc.text for doc in extracted_text])

    cleaned_text = clean_text(extracted_text)  

    save_markdown(cleaned_text) 
    print("✅ Data ingestion completed (cleaned and saved).")