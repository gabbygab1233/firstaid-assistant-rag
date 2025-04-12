import re
import unicodedata
from config_loader import load_config
from extract_text import extract_text_from_pdf

config = load_config()

# Fix hyphenation issue from OCR
HYPHEN_FIX_PATTERN = re.compile(r"(\w+)-\s*\n(\w+)")

# Fix multiple consecutive hashes to preserve formatting
HASH_CLEANUP_PATTERN = re.compile(r"(#+)\s*(?=\w)")

# Ensure section headers are properly formatted
SECTION_HEADER_PATTERN = re.compile(r"(?m)^([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\s*$")

def clean_text(text: str) -> str:
    """Cleans extracted text while preserving structure and formatting."""
    
    # Normalize Unicode characters
    text = unicodedata.normalize("NFKD", text)

    # Replace common OCR errors
    replacements = {
        "∞": "a",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "’": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "--"
    }
    
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    # Fix misplaced bullet points
    text = re.sub(r"(?m)^\s*h\s+", "- ", text)  
    text = re.sub(r"(?<=\n)\s*h\s+", "- ", text)  

    # Fix broken hyphenation (e.g., "deat-\n h" -> "death")
    text = HYPHEN_FIX_PATTERN.sub(r"\1\2", text)
    
    # Fix multiple consecutive hashes to ensure proper formatting
    text = HASH_CLEANUP_PATTERN.sub(r"\1 ", text)
    
    # Ensure proper line breaks and spacing
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text) 
    
    # Add ## to section headers
    text = SECTION_HEADER_PATTERN.sub(r"## \1", text)
    
    return text.strip()

def is_relevant_section(content: str) -> bool:
    """Filters out unwanted text while preserving useful data."""
    
    lower_content = content.lower().strip()

    if len(lower_content) < 30:  
        return False

    STRICT_EXCLUDE = [
        "copyright", "isbn", "logo", "acknowledgments", "contact",
        "phone:", "email:", "state disaster management authority",
        "meghalaya", "shillong", "printed by", "terms of use"
    ]
    
    if any(keyword in lower_content for keyword in STRICT_EXCLUDE) and len(lower_content.split()) < 10:
        return False  

    IMPORTANT_TERMS = ["first aid", "injury", "wound", "emergency", "burn", "fracture", "cpr"]
    
    if any(term in lower_content for term in IMPORTANT_TERMS):
        return True  

    return False

if __name__ == "__main__":

    config = load_config()

    pdf_path= config['paths']['pdf_file'][0]

    raw_documents = extract_text_from_pdf(pdf_path)

    if isinstance(raw_documents, list):
        raw_text = "\n\n".join([doc.text if hasattr(doc, 'text') else str(doc) for doc in raw_documents])
    else:
        raw_text = str(raw_documents) 

    cleaned_text = clean_text(raw_text)  

    print("Raw Text Sample:", raw_text[:300])  
    print("\nCleaned Text Sample:", cleaned_text[:300]) 
