from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
 
load_dotenv()

model = Ollama(
        base_url="http://ollama:11434",
        model="smollm2"  # veya başka bir model
    )

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Only short answer.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model
config = {"configurable": {"session_id": "firstChat"}}
with_message_history = RunnableWithMessageHistory(chain, get_session_history)


if __name__ == "__main__":   
    try:
        while True:
            user_input = input("> ")
            response = with_message_history.invoke(
                [HumanMessage(content=user_input)],
                config=config,
            )
            print(response)
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
