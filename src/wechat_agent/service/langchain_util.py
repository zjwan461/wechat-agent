from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.conversation.base import ConversationChain

memory_cache = {}


def get_memory(memory_key: str, memory_size: int = 5) -> ConversationBufferWindowMemory:
    if memory_key in memory_cache:
        return memory_cache[memory_key]
    else:
        memory = ConversationBufferWindowMemory(k=memory_size)
        memory_cache[memory_key] = memory
        return memory


def chat_block_ollama(
        model,
        system_message,
        human_message,
        base_url="http://127.0.0.1:11434",
        temperature=0.7,
        top_k=30,
        top_p=0.9):
    # 聊天模型调用（需传入消息列表，区分角色）
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": human_message}]

    chat_model = ChatOllama(
        model=model,
        base_url=base_url,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        reasoning=False,
    )

    memory = get_memory("ollama:" + model)
    chain = ConversationChain(llm=chat_model, memory=memory)
    return chain.invoke(messages)['response']


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
    memory = get_memory("ollama:" + model)
    chain = ConversationChain(llm=chat_model, memory=memory)
    return chain.invoke(messages)['response']


if __name__ == '__main__':
    content = chat_block_ollama("qwen3:8b", "你是一个AI助手,保证语言干练，不要超过500个字", "langchain是什么")
    print(content)
    content = chat_block_ollama("qwen3:8b", "你是一个AI助手，保证语言干练，不要超过500个字", "介绍一下文本生成")
    print(content)
