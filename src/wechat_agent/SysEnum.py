from enum import Enum


class AiProvider(Enum):
    Ollama = "Ollama"
    OpenAI = "Open_AI"


class AiType(Enum):
    LLM = "LLM"
    EMBEDDING = "Embedding"
