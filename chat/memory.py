from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory

MEMORY_KEY = "chat_history"

class SqliteMemory(SQLChatMessageHistory):
    """
    Custom memory class that uses SQLChatMessageHistory to store chat history.
    """

    def __init__(self, session_id: str, db_path: str = "sqlite:///chat_history.db"):
        super().__init__(connection=db_path, session_id=session_id)
        self.history = ConversationBufferMemory(memory_key=MEMORY_KEY, chat_memory=self, return_messages = True)
        