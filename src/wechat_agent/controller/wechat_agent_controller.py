import json
from pathlib import Path

from flask import Flask, session, request, g, jsonify, current_app
from src.wechat_agent.constants import SECRET_KEY, sys_info_id, token_header, token_prefix, token_white_list, gitee_url, \
    github_url, server_host, server_port, setting_id
from src.wechat_agent.domain.ajax_result import success, error, build
from src.wechat_agent.service.jwt_util import verify_token, generate_token
import re
from src.wechat_agent.logger_config import get_logger
from src.wechat_agent.service.db_util import SqliteSqlalchemy, SysInfo, Setting
from src.wechat_agent.__about__ import __version__ as version
from src.wechat_agent.service.md5_util import calculate_md5
from src.wechat_agent.service.captcha_util import generate_base64_captcha
import src.wechat_agent.service.systemInfo_util as systemInfo_util
from src.wechat_agent.controller.service_error import ApiError

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
        session.clear()
        return jsonify(error(payload["error"])), 401
    with app.app_context():
        login_token = current_app.config.get("token", {})
        if payload["payload"]["user_id"] not in login_token or login_token[
            payload["payload"]["user_id"]] != bearer_token:
            return jsonify(error("token已过期")), 401
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


@app.route("/api/base/git-repo")
def git_repo():
    return jsonify(success({"giteeUrl": gitee_url, "githubUrl": github_url}))


@app.errorhandler(ApiError)
def error_handle(e: ApiError):
    logger.error(e)
    return jsonify(error(e.message)), 200


@app.errorhandler(500)
def unknow_error_handle(e: Exception):
    logger.error(e)
    return jsonify(error("system is too busy")), 500


@app.route("/api/login", methods=["POST"])
def login():
    req = request.json
    if session.get('code').upper() != req["yzm"].upper():
        raise ApiError("验证码错误")
    sql_session = SqliteSqlalchemy().session
    sys_info = sql_session.query(SysInfo).filter(SysInfo.username == req["username"]).filter(
        SysInfo.password == calculate_md5(req["password"])).one_or_none()
    if sys_info is None:
        raise ApiError("用户名或密码错误")
    session["sys_info"] = sys_info.to_dic()

    token = token_prefix + generate_token(sys_info.username)
    with app.app_context():
        login_token = current_app.config.get("token", {})
        login_token[sys_info.username] = token
        current_app.config["token"] = login_token
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
    try:
        sys_info = session.query(SysInfo).get(sys_info_id)
        os_info = systemInfo_util.get_os_info()
        gpu_platform = "cuda" if systemInfo_util.is_cuda_available() else "cpu"
        if sys_info is None:
            sys_info = SysInfo(id=sys_info_id, os_arch=os_info['arch'], platform=os_info['os'],
                               gpu_platform=gpu_platform,
                               version=version, username=req["username"],
                               password=calculate_md5(req["password"]), email=req["email"])
            session.add(sys_info)
        else:
            sys_info.os_arch = os_info['arch']
            sys_info.platform = os_info['os']
            sys_info.gpu_platform = gpu_platform
            sys_info.version = version
            sys_info.username = req["username"]
            sys_info.password = calculate_md5(req["password"])
            sys_info.email = req["email"]

        setting = session.query(Setting).get(setting_id)
        if setting is None:
            setting = Setting(id=setting_id, model_save_dir=str(Path(__file__).parent.parent.parent / "models"))
            session.add(setting)
        else:
            setting.model_save_dir = str(Path(__file__).parent.parent.parent / "models")
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
    finally:
        session.close()
    return jsonify(success())


@app.route("/api/base/nav")
def nav():
    nav_path = str(Path(__file__).parent.parent / "nav.json")
    with open(nav_path, "r", encoding="utf-8") as f:
        conf = f.read()
        json_data = json.loads(conf)
        return jsonify(success(json_data))


@app.route("/api/logout")
def logout():
    session.clear()
    username = g.user_id
    with app.app_context():
        login_token = current_app.config.get("token", {})
        login_token.pop(username, None)
        current_app.config["token"] = login_token
    return jsonify(success())


@app.route("/api/watch/info")
def get_sys_info():
    result = {"cpu": systemInfo_util.get_cpu_info(), "memory": systemInfo_util.get_memory_info(),
              "gpus": systemInfo_util.get_gpu_info(),
              "os": systemInfo_util.get_os_info(), "sysInfo": systemInfo_util.get_sys_info(),
              "base_url": f"http://{server_host}:{server_port}"}
    return jsonify(success(result))


@app.route("/api/setting")
def get_setting():
    session = SqliteSqlalchemy().session
    setting = session.query(Setting).get(setting_id)
    if setting is None:
        return jsonify(success())
    else:
        result = setting.to_dic()
        return jsonify(success(result))


@app.route("/api/setting", methods=["POST"])
def update_setting():
    req = request.json
    session = SqliteSqlalchemy().session
    try:
        setting = session.query(Setting).get(setting_id)
        if setting is None:
            setting = Setting(id=setting_id, model_save_dir=req["model_save_dir"], proxy_host=req["proxy_host"],
                              proxy_port=req["proxy_port"])
            session.add(setting)
        else:
            setting.model_dir_dir = req["model_save_dir"]
            setting.proxy_host = req["proxy_host"]
            setting.proxy_port = req["proxy_port"]
        session.commit()
        return jsonify(success())
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
