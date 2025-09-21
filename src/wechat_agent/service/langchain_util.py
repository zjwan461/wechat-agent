from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def chat_block_open_ai(
        model,
        base_url,
        api_key,
        system_message,
        human_message,
        temperature=0.7,
        max_tokens=2048,
        top_p=0.9,
        timeout=60):
    # 聊天模型调用（需传入消息列表，区分角色）
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=human_message)]

    chat_model = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        base_url=base_url,
        top_p=top_p,
        timeout=timeout,
    )
    chat_response = chat_model.invoke(messages)
    return chat_response.content
