import random

from flask import Blueprint, jsonify, request

from wechat_agent.SysEnum import AgentType, AgentStatus, ChatType, WechatReplyType, AiProvider
from wechat_agent.controller.service_error import ApiError
from wechat_agent.domain.ajax_result import pageResp, success
from wechat_agent.service.db_util import SqliteSqlalchemy, Agent, AiRole, Model, Reply, SysInfo, ChatHistory
from wechat_agent.service.wx_util import start_wxauto_listening, stop_wxauto_listening
from wechat_agent.conf import sys_info_id
import pythoncom
from wechat_agent.service.langchain_util import chat_block_ollama, chat_block_open_ai, memory_cache
from wechat_agent.SysEnum import from_value

agent_bp = Blueprint('agent_bp', __name__)


def get_id_mapping(entity_class):
    session = SqliteSqlalchemy().session
    try:
        list = session.query(entity_class).all()
        res = {}
        for item in list:
            res[item.id] = item
        return res
    finally:
        session.close()


@agent_bp.route("/api/agent/list")
def agent_list():
    session = SqliteSqlalchemy().session
    try:
        params = request.args
        page = int(params.get("page"))
        page_size = int(params.get("page_size"))
        name = params.get("name")
        nickname = params.get("nickname")
        offset = (page - 1) * page_size
        query = session.query(Agent)
        if name:
            query = query.filter(Agent.name.like(f"%{name}%"))
        if nickname:
            query = query.filter(Agent.nickname.like(f"%{nickname}%"))
        record = query.limit(page_size).offset(offset).all()

        model_mapping = get_id_mapping(Model)
        ai_role_mapping = get_id_mapping(AiRole)
        rows = []
        for item in record:
            tmp = item.to_dic()
            model_id = tmp.get("model_id")
            if model_id is not None:
                tmp["model"] = model_mapping.get(model_id).name
            ai_role_id = tmp.get('ai_role_id')
            if ai_role_id is not None:
                tmp["ai_role"] = ai_role_mapping.get(ai_role_id).name
            rows.append(tmp)
        total = query.count()
        return jsonify(pageResp(rows, total))
    finally:
        session.close()


@agent_bp.route("/api/agent/<int:id>")
def get_agent(id):
    session = SqliteSqlalchemy().session
    try:
        agent = session.query(Agent).get(id)
    finally:
        session.close()

    if agent is None:
        return jsonify(success())
    else:
        return jsonify(success(agent.to_dic()))


@agent_bp.route("/api/agent/create", methods=["POST"])
def create_agent():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        agent = Agent(name=req["name"], nickname=req.get('nickname'), chat_type=req.get('chat_type'),
                      type=req.get('type'), reply_group=req.get('reply_group'), model_id=req.get('model_id'),
                      ai_role_id=req.get('ai_role_id'), memory_size=req.get('memory_size'))
        session.add(agent)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@agent_bp.route("/api/agent/update", methods=["PUT"])
def update_agent():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        agent = session.query(Agent).get(req["id"])
        if agent is not None:
            agent.name = req["name"]
            agent.nickname = req.get('nickname')
            agent.chat_type = req.get('chat_type')
            agent.type = req.get('type')
            agent.reply_group = req.get('reply_group')
            agent.model_id = req.get('model_id')
            agent.ai_role_id = req.get('ai_role_id')
            agent.memory_size = req.get('memory_size')
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@agent_bp.route("/api/agent/delete/<ids>", methods=["DELETE"])
def delete_agent(ids):
    ids = ids.split(",")
    session = SqliteSqlalchemy().session
    try:
        for id in ids:
            agent = session.query(Agent).get(id)
            if agent is not None:
                session.delete(agent)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@agent_bp.route('/api/agent/stop/<id>', methods=["POST"])
def stop_agent(id: int):
    session = SqliteSqlalchemy().session
    try:
        agent = session.query(Agent).get(id)
        if agent is None:
            raise ApiError(f"找不到id={id}的智慧助手")

        if agent.status == AgentStatus.STOPPED.value:
            raise ApiError('当前智慧助手不在运行状态')

        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        stop_wxauto_listening(nickname=agent.nickname)

        if agent.type == AgentType.AI.value:
            model = session.query(Model).get(agent.model_id)
            key = str(agent.id) + ":" + model.name
            if key in memory_cache:
                memory_cache.pop(key)
        agent.status = AgentStatus.STOPPED.value
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@agent_bp.route('/api/agent/start/<id>', methods=["POST"])
def start_agent(id: int):
    session = SqliteSqlalchemy().session
    try:
        agent = session.query(Agent).get(id)
        if agent is None:
            raise ApiError(f"找不到id={id}的智慧助手")

        if agent.status == AgentStatus.STARTED.value:
            raise ApiError('当前智慧助手运行中')

        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)

        sys_info = session.query(SysInfo).get(sys_info_id)
        wechat_version = sys_info.wechat_version
        my_wechat_names = sys_info.my_wechat_names
        if agent.type == AgentType.SIMPLE.value:
            groups = agent.reply_group.split(',')
            reply_list = session.query(Reply).filter(Reply.group.in_(groups)).all()
            reply_contents = []
            for reply in reply_list:
                reply_contents.append(reply.content)
            simple_chat(wechat_version, my_wechat_names, agent.nickname, reply_contents, agent.chat_type)
        elif agent.type == AgentType.AI.value:
            model = session.query(Model).get(agent.model_id)
            ai_role = session.query(AiRole).get(agent.ai_role_id)
            ai_chat(wechat_version, my_wechat_names, agent.nickname, model.to_dic(), agent.to_dic(), ai_role.to_dic())
        else:
            raise ApiError(f"不支持的智慧助手类型:{agent.type}")

        agent.status = AgentStatus.STARTED.value
        session.commit()
    finally:
        session.close()

    return jsonify(success())


def simple_chat(wechat_version, my_wechat_names, nickname, reply_list: list[str], agent: Agent):
    if agent.chat_type == ChatType.PRIVATE.value:
        def chat_private(nickname, sender, content):
            save_chat_msg(nickname, content, sender, agent.to_dic())
            resp = random.choice(reply_list)
            save_chat_msg(nickname, resp, AgentType.SIMPLE.value, agent.to_dic())
            return resp, WechatReplyType.REPLY

        start_wxauto_listening(wechat_version, nickname, chat_private)
    elif agent.chat_type == ChatType.GROUP.value:
        def chat_group(nickname: str, sender: str, content: str):
            at_me = False
            for wechat_name in my_wechat_names.split(','):
                if content.startswith(f'@{wechat_name}'):
                    at_me = True
                    break
            if at_me:
                save_chat_msg(nickname, content, sender, agent.to_dic())
                resp = random.choice(reply_list)
                save_chat_msg(nickname, resp, AgentType.SIMPLE.value, agent.to_dic())
            else:
                resp = None
            return resp, WechatReplyType.QUOTE

        start_wxauto_listening(wechat_version, nickname, chat_group)
    else:
        raise ApiError(f'不支持的聊天类型：{agent.chat_type}')


def ai_chat(wechat_version, my_wechat_names, nickname, model: dict, agent: dict, ai_role: dict):
    def do_ai_chat(content):
        ai_provider = from_value(AiProvider, model["provider"])
        prompt = ai_role.get("prompt").format(nickname=nickname)
        if ai_provider == AiProvider.Ollama:
            return chat_block_ollama(agent.get("id"), model.get("name"), prompt, content,
                                     model.get("base_url"),
                                     model.get("temperature"),
                                     model.get("top_k"), model.get("top_p"))
        else:
            return chat_block_open_ai(agent.get("id"), model.get("name"), model.get("base_url"), model.get("api_key"),
                                      prompt, content,
                                      model.get("temperature"), model.get("max_tokens"), model.get("top_p"))

    if agent["chat_type"] == ChatType.PRIVATE.value:
        def chat_private(nickname, sender, content):
            save_chat_msg(nickname, content, sender, agent)
            resp = do_ai_chat(content)
            save_chat_msg(nickname, resp, AgentType.AI.value, agent)
            return resp, WechatReplyType.REPLY

        start_wxauto_listening(wechat_version, nickname, chat_private)
    elif agent["chat_type"] == ChatType.GROUP.value:
        def chat_group(nickname: str, sender: str, content: str):
            at_me = False
            for wechat_name in my_wechat_names.split(','):
                if content.startswith(f'@{wechat_name}'):
                    at_me = True
                    break
            if at_me:
                save_chat_msg(nickname, content, sender, agent)
                resp = do_ai_chat(f"{nickname}说: {content}")
                save_chat_msg(nickname, resp, AgentType.AI.value, agent)
            else:
                resp = None

            return resp, WechatReplyType.QUOTE

        start_wxauto_listening(wechat_version, nickname, chat_group)
    else:
        raise ApiError(f'不支持的聊天类型：{agent["chat_type"]}')


def save_chat_msg(nickname: str, content: str, create_by: str, agent: dict):
    session = SqliteSqlalchemy().session
    try:
        chat_history = ChatHistory(agent_id=agent.get("id"), nickname=nickname, chat_type=agent.get("chat_type"),
                                   agent_type=agent.get("type"), content=content, create_by=create_by)

        session.add(chat_history)
        session.commit()
    finally:
        session.close()
