from flask import Blueprint, jsonify, request

from wechat_agent.domain.ajax_result import pageResp, success
from wechat_agent.service.db_util import SqliteSqlalchemy, Agent

agent_bp = Blueprint('agent_bp', __name__)


@agent_bp.route("/api/agent/list")
def agent_list():
    session = SqliteSqlalchemy().session
    try:
        params = request.args
        page = int(params.get("page"))
        page_size = int(params.get("page_size"))
        name = params.get("name")
        offset = (page - 1) * page_size
        query = session.query(Agent).filter(Agent.name.like(f"%{name}%"))
        record = query.limit(page_size).offset(offset).all()
        rows = []
        for item in record:
            rows.append(item.to_dic())
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
