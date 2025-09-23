from pathlib import Path

from flask import Blueprint, session, request, jsonify
from wechat_agent.service.db_util import SqliteSqlalchemy, SysInfo
from wechat_agent.controller.service_error import ApiError
from wechat_agent.service.md5_util import calculate_md5
from wechat_agent.service.jwt_util import generate_token
from wechat_agent.conf import token_prefix, sys_info_id
from wechat_agent.domain.ajax_result import success, error
from wechat_agent.service.captcha_util import generate_base64_captcha
import wechat_agent.service.systemInfo_util as systemInfo_util
from wechat_agent.__about__ import __version__ as version
from wechat_agent.logger_config import get_logger
from wechat_agent.service.wx_util import get_wechat_version
from wechat_agent.SysEnum import WechatVersion

logger = get_logger(__name__)

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    req = request.json
    if session.get('code').upper() != req["yzm"].upper():
        raise ApiError("验证码错误")
    sql_session = SqliteSqlalchemy().session
    sys_info = sql_session.query(SysInfo).filter(SysInfo.username == req["username"]).filter(
        SysInfo.password == calculate_md5(req["password"])).one_or_none()
    if sys_info is None:
        raise ApiError("用户名或密码错误")
    token = token_prefix + generate_token(sys_info.username)
    session[token] = sys_info.username
    return jsonify(success(token))


@auth_bp.route("/api/auth/yzm")
def get_yzm():
    base64_image, code = generate_base64_captcha()
    session["code"] = code
    return jsonify(success(base64_image))


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    req = request.json
    session = SqliteSqlalchemy().session
    try:
        sys_info = session.query(SysInfo).get(sys_info_id)
        os_info = systemInfo_util.get_os_info()
        gpu_platform = "cuda" if systemInfo_util.is_cuda_available() else "cpu"
        model_save_dir = str(Path(__file__).parent.parent.parent / "models")
        wechat_install_path = req.get("wechat_install_path")
        wechat_version = req.get('wechat_version')
        if wechat_version is None:
            wechat_version = get_wechat_version(wechat_install_path)
            if wechat_version is not None:
                if wechat_version.startswith("3"):
                    wechat_version = WechatVersion.V3.value
                elif wechat_version.startswith("4"):
                    wechat_version = WechatVersion.V4.value
                else:
                    raise ApiError("不支持的微信版本")
            else:
                raise ApiError("无法获取微信版本,请手动选择")

        if sys_info is None:
            sys_info = SysInfo(id=sys_info_id, os_arch=os_info['arch'], platform=os_info['os'],
                               gpu_platform=gpu_platform,
                               version=version, username=req["username"],
                               password=calculate_md5(req["password"]), email=req["email"],
                               model_save_dir=model_save_dir, wechat_install_path=wechat_install_path,
                               wechat_version=wechat_version)
            session.add(sys_info)
        else:
            sys_info.os_arch = os_info['arch']
            sys_info.platform = os_info['os']
            sys_info.gpu_platform = gpu_platform
            sys_info.version = version
            sys_info.username = req["username"]
            sys_info.password = calculate_md5(req["password"])
            sys_info.email = req["email"]
            sys_info.model_save_dir = model_save_dir
            sys_info.wechat_install_path = wechat_install_path
            sys_info.wechat_version = wechat_version
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise e
    finally:
        session.close()
    return jsonify(success())


@auth_bp.route("/api/auth/logout")
def logout():
    session.clear()
    return jsonify(success())


@auth_bp.route("/api/auth/refresh-token", methods=["POST"])
def refresh_token():
    req = request.get_json()
    refresh_token = req["refreshToken"]
    user_id = session.get(refresh_token)
    if user_id != None:
        new_token = token_prefix + generate_token(user_id)
        session[new_token] = user_id
        return jsonify(success(new_token))
    else:
        return jsonify(error("Token is invalid")), 401
