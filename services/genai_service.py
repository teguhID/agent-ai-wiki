from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import os
from dotenv import load_dotenv

load_dotenv()

# Set your Google API Key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Setup LangChain model and prompt
llm = ChatGoogleGenerativeAI(model=os.getenv("GOOLE_MODEL"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "Anda adalah agen pencari informasi wiki."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Combine prompt and model into a chain
chain = prompt | llm

# Store session-wise message histories
session_histories = {}

# Function to return (or create) ChatMessageHistory for a session
def get_session_history(session_id):
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]

# Wrap chain with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: get_session_history(session_id),
    input_messages_key="input",
    history_messages_key="chat_history"
)

