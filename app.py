import os
import sys
import chainlit as cl

# Add src/ to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Local imports
from config_loader import load_config
from index_data import load_existing_index
from prompt.first_aid_template import richprompt

# LlamaIndex components
from llama_index.core import Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.callbacks import CallbackManager

# Global query_engine so it's accessible across events
query_engine = None

# Load configuration
config = load_config()

@cl.on_chat_start
async def on_chat_start():
    global query_engine

    index = load_existing_index()
    if index is None:
        await cl.Message(content="❌ Failed to load index. Please build it first.").send()
        return



    # Setup retriever and response synthesizer
    storage_context = index.storage_context
    base_retriever = index.as_retriever(similarity_top_k=config['similarity_k'])
    retriever = AutoMergingRetriever(base_retriever, storage_context)

    response_synthesizer = get_response_synthesizer(response_mode=config['response_mode'])

    # Create the query engine
    # Create synthesizer and query engine
    response_synthesizer = get_response_synthesizer(response_mode=config['response_mode'])
    query_engine = index.as_query_engine(
        prompt_template=richprompt,
        response_synthesizer=response_synthesizer
    )

    # Greet the user
    await cl.Message(content="👋 Hello! I'm your First Aid Assistant. Ask me anything related to first aid!").send()

@cl.on_message
async def on_message(message: cl.Message):
    if query_engine is None:
        await cl.Message(content="⚠️ The query engine is not initialized. Please restart the chat.").send()
        return

    response = await cl.make_async(query_engine.query)(message.content)
    await cl.Message(content=str(response)).send()
