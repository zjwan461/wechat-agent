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


class WechatVersion(Enum):
    V3 = "V3"
    V4 = "V4"


def from_value(enum_cls, value):
    """根据value获取对应的枚举成员"""
    for member in enum_cls.__members__.values():
        if member.value == value:
            return member
    return None
