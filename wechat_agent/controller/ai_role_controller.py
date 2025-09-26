from flask import Blueprint, jsonify, request

from wechat_agent.domain.ajax_result import pageResp, success
from wechat_agent.service.db_util import SqliteSqlalchemy, AiRole

ai_role_bp = Blueprint("ai_role_bp", __name__)


@ai_role_bp.route("/api/aiRole/list")
def list_ai_role():
    session = SqliteSqlalchemy().session
    try:
        params = request.args
        page = int(params.get("page"))
        page_size = int(params.get("page_size"))
        name = params.get("name")
        offset = (page - 1) * page_size
        query = session.query(AiRole)
        if name:
            query = query.filter(AiRole.name.like(f"%{name}%"))
        record = query.limit(page_size).offset(offset).all()
        rows = []
        for item in record:
            rows.append(item.to_dic())
        total = query.count()
        return jsonify(pageResp(rows, total))
    finally:
        session.close()


@ai_role_bp.route("/api/aiRole/<int:id>")
def get_ai_role(id):
    session = SqliteSqlalchemy().session
    try:
        ai_role = session.query(AiRole).get(id)
        if ai_role is None:
            return jsonify(success())
        else:
            return jsonify(success(ai_role.to_dic()))
    finally:
        session.close()


@ai_role_bp.route("/api/aiRole/create", methods=["POST"])
def create_ai_role():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        ai_role = AiRole(name=req["name"], prompt=req["prompt"])
        session.add(ai_role)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@ai_role_bp.route("/api/aiRole/update", methods=["PUT"])
def update_ai_role():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        ai_role = session.query(AiRole).get(req["id"])
        if ai_role is not None:
            ai_role.name = req["name"]
            ai_role.prompt = req["prompt"]
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@ai_role_bp.route("/api/aiRole/delete/<ids>", methods=["DELETE"])
def delete_ai_role(ids):
    ids = ids.split(",")
    session = SqliteSqlalchemy().session
    try:
        for id in ids:
            ai_role = session.query(AiRole).get(id)
            if ai_role is not None:
                session.delete(ai_role)
        session.commit()
    finally:
        session.close()
    return jsonify(success())
