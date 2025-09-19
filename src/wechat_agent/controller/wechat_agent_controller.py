from flask import Flask, session, request, g, jsonify
from src.wechat_agent.constants import SECRET_KEY, sys_info_id, token_header, token_prefix, token_white_list, gitee_url, \
    github_url
from src.wechat_agent.domain.ajax_result import success, error
from src.wechat_agent.service.jwt_util import verify_token, generate_token
import re
from src.wechat_agent.logger_config import get_logger
from src.wechat_agent.service.db_util import SqliteSqlalchemy, SysInfo
from src.wechat_agent.__about__ import __version__ as version
from src.wechat_agent.service.md5_util import calculate_md5
from src.wechat_agent.service.captcha_util import generate_base64_captcha

app = Flask(__name__)
app.secret_key = SECRET_KEY
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
    token = bearer_token[len(token_prefix):]
    payload = verify_token(token)
    if not payload["valid"]:
        return jsonify(error(payload["error"])), 401
    g.user_id = payload["payload"]["user_id"]
    return None


@app.route("/api/base/git-repo")
def git_repo():
    return jsonify(success({"giteeUrl": gitee_url, "githubUrl": github_url}))


@app.errorhandler(500)
def error_handle(e):
    logger.error(e)
    return jsonify(error()), 500


@app.route("/api/login", methods=["POST"])
def login():
    req = request.json
    if session.get('code').upper() != req["yzm"].upper():
        return jsonify(error("验证码错误"))
    sql_session = SqliteSqlalchemy().session
    sys_info = sql_session.query(SysInfo).filter(SysInfo.username == req["username"]).filter(
        SysInfo.password == calculate_md5(req["password"])).one_or_none()
    if sys_info is None:
        return jsonify(error("账号或密码错误"))
    session["sys_info"] = sys_info.to_dic()

    token = token_prefix + generate_token(sys_info.username)
    return jsonify(success(token))


@app.route('/api/base/sys-info')
def sys_info():
    session = SqliteSqlalchemy().session
    result = session.query(SysInfo).get(sys_info_id)
    if result is None:
        return jsonify(success())

    return jsonify(success(result.to_dic()))


@app.route("/api/base/yzm")
def get_yzm():
    base64_image, code = generate_base64_captcha()
    session["code"] = code
    return jsonify(success(base64_image))


@app.route("/api/register", methods=["POST"])
def register():
    req = request.json
    session = SqliteSqlalchemy().session
    sys_info = session.query(SysInfo).get(sys_info_id)
    if sys_info is None:
        sys_info = SysInfo(id=sys_info_id, version=version, username=req["username"],
                           password=calculate_md5(req["password"]), email=req["email"])
        session.add(sys_info)
    else:
        sys_info.username = req["username"]
        sys_info.password = calculate_md5(req["password"])
        sys_info.email = req["email"]
    session.commit()
    return jsonify(success())
