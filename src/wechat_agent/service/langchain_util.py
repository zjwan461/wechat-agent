from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

memory_cache = {}


def get_memory(memory_key: str, memory_size: int = 5) -> ConversationBufferWindowMemory:
    if memory_key in memory_cache:
        return memory_cache[memory_key]
    else:
        memory = ConversationBufferWindowMemory(k=memory_size)
        memory_cache[memory_key] = memory
        return memory


def chat_block_ollama(
        agent_id,
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

    memory = get_memory(str(agent_id) + ":" + model)
    chain = ConversationChain(llm=chat_model, memory=memory)
    return chain.invoke(messages)['response']


def chat_block_open_ai(
        agent_id,
        model,
        base_url,
        api_key,
        system_message,
        human_message,
        temperature=0.7,
        max_tokens=2048,
        top_p=0.9,
        timeout=60):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": human_message}]
    chat_model = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        base_url=base_url,
        top_p=top_p,
        timeout=timeout,
    )
    memory = get_memory(str(agent_id) + ":" + model)
    chain = ConversationChain(llm=chat_model, memory=memory, verbose=True)
    return chain.invoke(messages)['response']


if __name__ == '__main__':
    # content = chat_block_ollama(1,"qwen3:8b", "你叫花花，是一个AI助手。回答保证语言干练，不要超过500个字", "花花，我今天打了篮球")
    # print(content)
    # content = chat_block_ollama(1,"qwen3:8b", "你叫花花，是一个AI助手。回答保证语言干练，不要超过500个字", "@花花")
    # print(content)
    content = chat_block_open_ai(1, "qwen3-8b", "http://10.100.216.70:8000/v1", "test",
                                 "你叫花花，是一个AI助手。回答保证语言干练，不要超过500个字", "花花，我今天打了篮球")
    print(content)

    content = chat_block_open_ai(1, "qwen3-8b", "http://10.100.216.70:8000/v1", "test",
                                 "你叫花花，是一个AI助手。回答保证语言干练，不要超过500个字", "花花，我好累")
    print(content)
