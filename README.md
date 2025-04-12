
# FirstAidRAG: A Smart Emergency Response Assistant Powered by [LlamaIndex](https://docs.llamaindex.ai/en/stable/)


FirstAidRAG is an intelligent first aid assistant that utilizes LlamaIndex and Ollama to process documents, extract relevant first aid information, and provide real-time assistance.

<p align="center">
  <img src="https://github.com/user-attachments/assets/6ba0d93d-7565-4507-9ea1-2c02e5761680">
</p>

---

### Script Overview

Below is a description of the key scripts used in the project:

- **`extract_text.py`**: Extracts structured text from a PDF using LlamaParse API. If LlamaParse fails, it falls back to SimpleDirectoryReader. The script processes the PDF, logs results, and prints a preview of the extracted text.

- **`clean_text.py`**: Cleans and formats extracted text, fixing OCR errors, hyphenation issues, and section headers while removing irrelevant content and preserving important terms.

- **`ingest_data.py`**: Extracts text from a PDF, cleans it, and saves the cleaned content into a Markdown file. The script processes each section of the document, filters relevant content, and handles file saving.

- **`index_data.py`**: Creates or loads a FAISS index for vector-based search using Ollama embeddings. This script processes cleaned text from the Markdown file and stores the index for efficient querying.

- **`evaluate_rag.py`**: Evaluates the first aid responses of the LLM based on relevancy and faithfulness scores. Results are saved to a CSV file for further analysis.

- **`query_engine.py`**: Loads a FAISS index, retrieves relevant documents using AutoMergingRetriever, and generates a response based on the first aid prompt. If no relevant documents are found, it returns a default message.

- **`chat_engine.py`**: Creates a chat engine for interactive first aid assistance using a memory buffer. Streams real-time responses to user input and provides an option to exit the conversation.

---


### Setup

Clone the repository and navigate into the project folder:
```
git clone https://github.com/gabbygab1233/firstaid_assistant.git
cd firstaid_assistant
```

---

### Install all code dependencies

Install the necessary Python packages using `pip`:
```
pip3 install -r requirements.txt
```

---

### Configure LlamaParse API Key

1. Signup for LlamaCloud [here](https://cloud.llamaindex.ai/) to get an API key for LlamaParse.
2. After signing up, create an API key and paste it in the `config.yaml` file as follows:

#### config.yaml
```
LLAMA_CLOUD_API_KEY: put-your-api-key-here
```

---

### Install Ollama

Download Ollama from [this link](https://ollama.com/library/llama3.2). Once downloaded, pull the necessary models:

```
ollama pull llama3.1
ollama pull nomic-embed-text
```



### Running the Application
#### Run Ollama in the Background

Start the Ollama server in the background to serve the models:
```
ollama serve
```

---

### Running the Pipeline

Once Ollama is running, execute the pipeline by running the following command:
```
python3 main.py
```

---

### Running the Application

To launch the application, run the following command:
```
chainlit run app.py -w
```

---


