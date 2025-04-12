from llama_index.core.memory import ChatMemoryBuffer
from prompt.first_aid_template import richprompt, prompttemp
from index_data import load_existing_index
from config_loader import load_config

config = load_config()

def create_chat_engine():
    """Sets up the chat engine with strict first aid guidelines for interactive chat."""
    
    # Load the index
    index = load_existing_index()
    if index is None:
        print("❌ Failed to load index. Ensure it's created before querying.")
        return None

    # Set up memory buffer
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)

    # Create the chat engine
    chat_engine = index.as_chat_engine(
        chat_mode=config['chat_mode'],
        memory=memory,
        context_prompt=richprompt.template_str ,  # Pass the template directly
        verbose=False,
    )
    return chat_engine

def chat_with_engine(chat_engine):
    """Interactive chat loop for live user input."""
    print("Start chatting with the assistant (type 'exit' to end).")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting the chat.")
            break
        
        # Stream the response live
        streaming_response = chat_engine.stream_chat(user_input)
        print("Assistant:", end=" ")
        for token in streaming_response.response_gen:
            print(token, end="")
        print()  # for a new line after the response


if __name__ == "__main__":
    chat_engine = create_chat_engine()
    
    chat_with_engine(chat_engine)
