from enum import Enum


class AiProvider(Enum):
    Ollama = "Ollama"
    OpenAI = "Open_AI"


class AiType(Enum):
    LLM = "LLM"
    EMBEDDING = "Embedding"


class AgentType(Enum):
    SIMPLE = "SIMPLE"
    AI = "AI"

class AgentStatus(Enum):
    STARTED = "运行中"
    STOPPED = "已停止"

class ChatType(Enum):
    PRIVATE = '私聊'
    GROUP = '群聊'