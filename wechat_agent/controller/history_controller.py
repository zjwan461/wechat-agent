from flask import request, Blueprint, jsonify

from wechat_agent.domain.ajax_result import success, pageResp
from wechat_agent.logger_config import get_logger
from wechat_agent.service.db_util import SqliteSqlalchemy, ChatHistory, Agent

logger = get_logger(__name__)

history_bp = Blueprint('history_bp', __name__)


@history_bp.route("/api/history/list")
def list_history():
    session = SqliteSqlalchemy().session
    try:
        params = request.args
        page = int(params.get("page"))
        page_size = int(params.get("page_size"))
        agent_id = params.get("agent_id")
        nickname = params.get("nickname")
        offset = (page - 1) * page_size
        query = session.query(ChatHistory)
        if agent_id:
            query = query.filter(ChatHistory.agent_id == agent_id)
        if nickname:
            query = query.filter(ChatHistory.nickname.like(f'%{nickname}%'))

        record = query.limit(page_size).offset(offset).all()
        rows = []

        agent_list = session.query(Agent).all()
        mapping = {}
        for item in agent_list:
            mapping[item.id] = item

        for item in record:
            tmp = item.to_dic()
            agent_id = tmp.get("agent_id")
            if agent_id is not None:
                tmp["agent"] = mapping.get(agent_id).name
            rows.append(tmp)
        total = query.count()
        return jsonify(pageResp(rows, total))
    finally:
        session.close()


@history_bp.route("/api/history/<int:id>")
def get_history(id):
    session = SqliteSqlalchemy().session
    try:
        model = session.query(ChatHistory).get(id)
        if model is None:
            res = success()
        else:
            agent = session.query(Agent).get(model.agent_id)
            tmp = model.to_dic()
            tmp["agent"] = agent.name
            res = success(tmp)
    finally:
        session.close()
    return jsonify(res)


@history_bp.route("/api/history/delete/<ids>", methods=["DELETE"])
def delete_history(ids):
    ids = ids.split(",")
    session = SqliteSqlalchemy().session
    try:
        for id in ids:
            chat_history = session.query(ChatHistory).get(id)
            if chat_history is not None:
                session.delete(chat_history)
        session.commit()
    finally:
        session.close()
    return jsonify(success())
