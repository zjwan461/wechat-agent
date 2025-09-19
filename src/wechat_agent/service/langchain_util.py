from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

chat_model = ChatOpenAI(
    model="qwen-plus-2025-07-28",
    temperature=0.7,
    max_tokens=2048,
    api_key="sk-343c687211834de2857fef9c9d13bc7d",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout=60,
)
# 聊天模型调用（需传入消息列表，区分角色）
messages = [
    SystemMessage(content="你是一个AI助手，用简洁的语言回答问题,不超過100字"),
    HumanMessage(content="LangChain 主要能做什么？")
]
chat_response = chat_model.invoke(messages)
print("聊天模型响应:\n", chat_response)