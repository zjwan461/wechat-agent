import json
from pathlib import Path

from flask import Blueprint, request, jsonify

from wechat_agent.controller.service_error import ApiError
from wechat_agent.domain.ajax_result import success
from wechat_agent.conf import gitee_url, github_url, sys_info_id, server_host, server_port
from wechat_agent.service import systemInfo_util
from wechat_agent.service.db_util import SqliteSqlalchemy, SysInfo
from wechat_agent.service.wx_util import get_wechat_version
from wechat_agent.SysEnum import WechatVersion

base_bp = Blueprint('base_bp', __name__)


@base_bp.route("/api/base/git-repo")
def git_repo():
    return jsonify(success({"giteeUrl": gitee_url, "githubUrl": github_url}))


@base_bp.route('/api/base/sys-info')
def sys_info():
    session = SqliteSqlalchemy().session
    result = session.query(SysInfo).get(sys_info_id)
    if result is None:
        return jsonify(success())

    return jsonify(success(result.to_dic()))


@base_bp.route("/api/base/nav")
def nav():
    nav_path = str(Path(__file__).parent.parent / "nav.json")
    with open(nav_path, "r", encoding="utf-8") as f:
        conf = f.read()
        json_data = json.loads(conf)
        return jsonify(success(json_data))


@base_bp.route("/api/watch/info")
def get_sys_info():
    result = {"cpu": systemInfo_util.get_cpu_info(), "memory": systemInfo_util.get_memory_info(),
              "gpus": systemInfo_util.get_gpu_info(),
              "os": systemInfo_util.get_os_info(), "sysInfo": systemInfo_util.get_sys_info(),
              "base_url": f"http://{server_host}:{server_port}"}
    return jsonify(success(result))


@base_bp.route("/api/setting")
def get_setting():
    session = SqliteSqlalchemy().session
    sys_info = session.query(SysInfo).get(sys_info_id)
    if sys_info is None:
        return jsonify(success())
    else:
        result = sys_info.to_dic()
        return jsonify(success(result))


@base_bp.route("/api/setting", methods=["POST"])
def update_setting():
    req = request.json
    wechat_install_path = req["wechat_install_path"]
    version = req.get('wechat_version')
    my_wechat_names = req.get('my_wechat_names')
    if version is None or len(version) == 0:
        version = get_wechat_version(wechat_install_path)
        if version is None:
            raise ApiError("无法获取微信版本,请手动指定")
        if version.startswith("3"):
            version = WechatVersion.V3.value
        elif version.startswith("4"):
            version = WechatVersion.V4.value
        else:
            raise ApiError("不支持的微信版本")

    session = SqliteSqlalchemy().session
    try:
        sys_info = session.query(SysInfo).get(sys_info_id)
        if sys_info is not None:
            sys_info.model_dir_dir = req.get("model_save_dir")
            sys_info.wechat_install_path = wechat_install_path
            sys_info.wechat_version = version
            sys_info.my_wechat_names = my_wechat_names
            sys_info.proxy_host = req.get("proxy_host")
            sys_info.proxy_port = req.get("proxy_port")
        session.commit()
        return jsonify(success())
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
