from flask import Blueprint, jsonify, request

from wechat_agent.domain.ajax_result import pageResp, success
from wechat_agent.service.db_util import SqliteSqlalchemy, Agent, AiRole, Model

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
        if agent is None:
            return jsonify(success())
        else:
            return jsonify(success(agent.to_dic()))
    finally:
        session.close()


@agent_bp.route("/api/agent/create", methods=["POST"])
def create_agent():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        agent = Agent(name=req["name"], nickname=req.get('nickname'), chat_type=req.get('chat_type'),
                      type=req.get('type'), reply_group=req.get('reply_group'), model_id=req.get('model_id'),
                      ai_role_id=req.get('ai_role_id'))
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
