from wechat_agent.conf import token_header, token_prefix, token_white_list, SECRET_KEY, server_host, server_port
from flask import Flask, request, jsonify, session, g
from wechat_agent.logger_config import get_logger
import re

from wechat_agent.controller.service_error import ApiError
from wechat_agent.domain.ajax_result import error
from wechat_agent.service.jwt_util import verify_token
from wechat_agent.controller.auth_controller import auth_bp
from wechat_agent.controller.base_controller import base_bp
from wechat_agent.controller.agent_controller import agent_bp
from wechat_agent.controller.ai_role_controller import ai_role_bp
from wechat_agent.controller.reply_controller import reply_bp
from wechat_agent.controller.model_controller import model_bp
from wechat_agent.controller.history_controller import history_bp

app = Flask(__name__, static_url_path='/ui', static_folder='ui')
app.secret_key = SECRET_KEY
app.register_blueprint(auth_bp)
app.register_blueprint(base_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(ai_role_bp)
app.register_blueprint(reply_bp)
app.register_blueprint(model_bp)
app.register_blueprint(history_bp)

logger = get_logger()


@app.before_request
def auth():
    if request.path in token_white_list:
        logger.info(f"{request.path} match token white list, no need auth")
        return None
    for rule in token_white_list:
        if bool(re.fullmatch(rule, request.path)):
            logger.info(f"{request.path} match token white list, no need auth")
            return None
    headers = request.headers
    bearer_token = headers.get(token_header)
    if not bearer_token or not bearer_token.startswith(token_prefix):
        return jsonify(error("invalid token")), 401

    save_user_id = session.get(bearer_token)
    if save_user_id is None:
        session.clear()
        return jsonify(error("invalid token")), 401

    token = bearer_token[len(token_prefix):]
    payload = verify_token(token)
    if not payload["valid"]:
        return jsonify(error(payload["error"])), 401
    g.user_id = payload["payload"]["user_id"]

    return None


@app.after_request
def resp(response):
    global data
    status = response.status
    try:
        data = response.get_json()
    except Exception as e:
        logger.error("cant not get json from response", e)

    if data is not None:
        code = data.get('code')
        if code is None:
            return jsonify(code=code, msg=data.get('msg'), data=data.get('data')), status

    return response


@app.errorhandler(ApiError)
def error_handle(e):
    logger.error(e)
    return jsonify(error(e.message)), 200


@app.errorhandler(Exception)
def unknow_error_handle(e: Exception):
    logger.error(e)
    return jsonify(error("system is too busy")), 500


def main():
    app.run(host=server_host, port=server_port)


if __name__ == "__main__":
    main()
