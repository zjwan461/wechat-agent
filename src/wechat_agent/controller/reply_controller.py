from flask import request, Blueprint, jsonify

from wechat_agent.service.db_util import SqliteSqlalchemy, Reply
from wechat_agent.domain.ajax_result import success, pageResp

reply_bp = Blueprint('reply_bp', __name__)


@reply_bp.route("/api/reply/list")
def list_reply():
    session = SqliteSqlalchemy().session
    try:
        params = request.args
        page = int(params.get("page"))
        page_size = int(params.get("page_size"))
        content = params.get("content")
        offset = (page - 1) * page_size
        query = session.query(Reply)
        if content:
            query = query.filter(Reply.content.like(f"%{content}%"))
        record = query.limit(page_size).offset(offset).all()
        rows = []
        for item in record:
            rows.append(item.to_dic())
        total = query.count()
        return jsonify(pageResp(rows, total))
    finally:
        session.close()


@reply_bp.route("/api/reply/<int:id>")
def get_ai_role(id):
    session = SqliteSqlalchemy().session
    try:
        reply = session.query(Reply).get(id)
        if reply is None:
            res = success()
        else:
            res = success(reply.to_dic())
    finally:
        session.close()
    return jsonify(res)


@reply_bp.route("/api/reply/create", methods=["POST"])
def create_ai_role():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        reply = Reply(content=req["content"], group=req["group"])
        session.add(reply)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@reply_bp.route("/api/reply/update", methods=["PUT"])
def update_ai_role():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        reply = session.query(Reply).get(req["id"])
        if reply is not None:
            reply.content = req["content"]
            reply.group = req["group"]
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@reply_bp.route("/api/reply/delete/<ids>", methods=["DELETE"])
def delete_ai_role(ids):
    ids = ids.split(",")
    session = SqliteSqlalchemy().session
    try:
        for id in ids:
            reply = session.query(Reply).get(id)
            if reply is not None:
                session.delete(reply)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@reply_bp.route('/api/reply/listGroup')
def listGroup():
    session = SqliteSqlalchemy().session
    try:
        list = session.query(Reply).group_by(Reply.group).all()
        list_group = []
        if list and len(list) > 0:
            for item in list:
                list_group.append(item.group)
    finally:
        session.close()
    return jsonify(success(list_group))
