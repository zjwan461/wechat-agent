from flask import request, Blueprint, jsonify

from wechat_agent.service.db_util import SqliteSqlalchemy, Model
from wechat_agent.domain.ajax_result import success, pageResp
from wechat_agent.service.langchain_util import chat_block_open_ai
from wechat_agent.logger_config import get_logger
from wechat_agent.controller.service_error import ApiError

logger = get_logger(__name__)

model_bp = Blueprint('model_bp', __name__)


@model_bp.route("/api/model/list")
def list_model():
    session = SqliteSqlalchemy().session
    try:
        params = request.args
        page = int(params.get("page"))
        page_size = int(params.get("page_size"))
        name = params.get("name")
        offset = (page - 1) * page_size
        query = session.query(Model)
        if name:
            query = query.filter(Model.name.like(f"%{name}%"))
        record = query.limit(page_size).offset(offset).all()
        rows = []
        for item in record:
            rows.append(item.to_dic())
        total = query.count()
        return jsonify(pageResp(rows, total))
    finally:
        session.close()


@model_bp.route("/api/model/<int:id>")
def get_ai_role(id):
    session = SqliteSqlalchemy().session
    try:
        model = session.query(Model).get(id)
        if model is None:
            res = success()
        else:
            res = success(model.to_dic())
    finally:
        session.close()
    return jsonify(res)


@model_bp.route("/api/model/create", methods=["POST"])
def create_ai_role():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        model = Model(name=req.get("name"), provider=req.get('provider'), base_url=req.get('base_url'),
                      api_key=req.get("api_key"), max_tokens=req.get('max_tokens'),
                      temperature=req.get("temperature"), top_k=req.get("top_k"), top_p=req.get("top_p"))
        if not check_llm(model):
            raise ApiError('模型检查失败')
        session.add(model)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@model_bp.route("/api/model/update", methods=["PUT"])
def update_ai_role():
    req = request.get_json()
    session = SqliteSqlalchemy().session
    try:
        model = session.query(Model).get(req["id"])
        if model is not None:
            if not check_llm(model):
                raise ApiError('模型检查失败')
            model.name = req["name"]
            model.provider = req.get("provider")
            model.base_url = req.get("base_url")
            model.max_tokens = req.get("max_tokens")
            model.provider = req.get("provider")
            model.api_key = req.get("api_key")
            model.temperature = req.get("temperature")
            model.top_k = req.get("top_k")
            model.top_p = req.get("top_p")
        session.commit()
    finally:
        session.close()
    return jsonify(success())


@model_bp.route("/api/model/delete/<ids>", methods=["DELETE"])
def delete_ai_role(ids):
    ids = ids.split(",")
    session = SqliteSqlalchemy().session
    try:
        for id in ids:
            model = session.query(Model).get(id)
            if model is not None:
                session.delete(model)
        session.commit()
    finally:
        session.close()
    return jsonify(success())


def check_llm(model: Model):
    try:
        resp = chat_block_open_ai(model=model.name, base_url=model.base_url, api_key=model.api_key,
                                  system_message='你是一个AI助手', human_message='hello')
        logger.info(f'llm测试成功,resp={resp}')
        return True
    except Exception as e:
        logger.error(f"llm测试失败,error={e}")
        return False
