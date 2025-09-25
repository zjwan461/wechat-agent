import os
import subprocess
from typing import Callable

from wechat_agent.logger_config import get_logger
from wechat_agent.service.wxauto3_util import WeXinAuto3Service
from wechat_agent.service.wxauto4_util import WeXinAuto4Service
from wechat_agent.SysEnum import WechatVersion

logger = get_logger(__name__)


def get_wechat_version(wechat_exe_path):
    """从指定路径的微信可执行文件获取版本信息"""
    # 检查路径是否存在
    if not os.path.exists(wechat_exe_path):
        logger.error(f"错误: 未找到文件 - {wechat_exe_path}")
        return None

    # 确保路径是Weixin.exe
    if not wechat_exe_path.endswith("Weixin.exe") and not wechat_exe_path.endswith("WeChat.exe"):
        logger.error("错误: 请提供Weixin.exe/WeChat.exe的完整路径")

    try:
        # 处理路径中的反斜杠，适应wmic命令要求
        formatted_path = wechat_exe_path.replace("\\", "\\\\")

        # 使用wmic命令获取文件版本
        result = subprocess.check_output(
            f'wmic datafile where name="{formatted_path}" get Version /value',
            shell=True,
            encoding='utf-8',
            stderr=subprocess.STDOUT
        )

        # 解析输出结果
        version_line = [line.strip() for line in result.splitlines() if line.strip().startswith("Version=")]
        if version_line:
            version = version_line[0].split("=", 1)[1]
            return version
        else:
            logger.error("无法从文件中获取版本信息")
    except subprocess.CalledProcessError as e:
        logger.error(f"执行命令出错: {e.output}")
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
    return None


wxauto_service_holder = {}


def start_wxauto_listening(version, nickname, msg_handler: Callable):
    wxauto_service = wxauto_service_holder.get("service")
    if wxauto_service is None:
        if version == WechatVersion.V3.value:
            wxauto_service = WeXinAuto3Service(msg_handler)
            wxauto_service_holder["service"] = wxauto_service
        else:
            wxauto_service = WeXinAuto4Service(msg_handler)
            wxauto_service_holder["service"] = wxauto_service
    else:
        wxauto_service.msg_handler = msg_handler

    wxauto_service.listen(nickname)


def stop_wxauto_listening(nickname):
    wxauto_service = wxauto_service_holder.get("service")
    if wxauto_service is None:
        logger.warning("not found wxauto service in wxauto_service_holder")
    else:
        wxauto_service.remove_listen(nickname)


if __name__ == "__main__":
    # 这里替换为你的微信安装路径
    # 示例:
    # wechat_path = r"C:\Program Files\Tencent\WeChat\WeChat.exe"
    # wechat_path = r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"
    # wechat_path = r"C:\Users\你的用户名\AppData\Local\Tencent\WeChat\WeChat.exe"

    wechat_path = r"F:\software\Weixin\Weixin.exe"  # 请修改为实际路径

    print(get_wechat_version(wechat_path))
