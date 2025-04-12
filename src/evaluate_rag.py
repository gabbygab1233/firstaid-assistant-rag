from llama_index.core.evaluation import RelevancyEvaluator, FaithfulnessEvaluator
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from pathlib import Path
from llama_index.core import Settings
import pandas as pd
from query_engine import query_index
from config_loader import load_config
import os


config = load_config()

# Set Ollama as the embedding model and LLM
Settings.embed_model = OllamaEmbedding(model_name=config['embed'])
Settings.llm = Ollama(model=config['llm'], request_timeout=360.0)

CSV_PATH = config['paths']['eval_path']
START_FRESH = False  


relevancy_eval = RelevancyEvaluator()
faithfulness_eval = FaithfulnessEvaluator()

eval_questions = [
    "What actions should be taken if a child fell from a height and landed on their head, became momentarily unconscious, and now shows signs of confusion?",
    "What emergency procedures should be performed when someone suddenly begins gasping, clutching their throat, and is unable to speak or breathe during a meal?",
    "What first aid should be provided when a person is found unresponsive after being exposed to extreme heat, with hot, dry skin?",
    "What immediate care is needed when someone burns their hand on a hot pan, causing redness and pain?",
    "What first aid should be provided when a joint appears visibly out of place after a fall, causing intense pain?",
    "What first aid should be administered if a child inhaled a small object and is now struggling to breathe, making unusual sounds?",
    "What first aid should be given when a person is making high-pitched noises and struggling to breathe after eating?",
    "What first aid is needed if a person's knee appears to be out of place after a sports injury, with severe pain and swelling?",
    "What immediate actions should be taken when someone suddenly experiences severe chest pain radiating down their arm, accompanied by shortness of breath?"
]

# Save evaluation results to CSV
def save_eval_to_csv(query: str, response: str, relevancy, faithfulness):
    # Ensure the directory exists
    directory = os.path.dirname(CSV_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist

    file_exists = Path(CSV_PATH).exists()

    df = pd.DataFrame([{
        "Query": query,
        "Response": str(response),
        "Relevancy Score": relevancy.score,
        "Relevancy Pass": relevancy.passing,
        "Relevancy Feedback": relevancy.feedback,
        "Faithfulness Score": faithfulness.score,
        "Faithfulness Pass": faithfulness.passing,
        "Faithfulness Feedback": faithfulness.feedback
    }])

    df.to_csv(CSV_PATH, mode='a', header=not file_exists, index=False)

# Evaluate and save results
def evaluate_and_save(query: str):
    response = query_index(query)
    relevancy = relevancy_eval.evaluate_response(query=query, response=response)
    faithfulness = faithfulness_eval.evaluate_response(query=query, response=response)
    save_eval_to_csv(query, response, relevancy, faithfulness)
    print(f"✅ Evaluated: {query[:60]}...")

# Run evaluations for all questions
for q in eval_questions:
    evaluate_and_save(q)
