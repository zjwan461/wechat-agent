import os
import sys


def resource_path(relative_path):
    """获取资源的绝对路径，兼容开发和打包模式"""
    try:
        # PyInstaller打包后的临时目录
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境下的当前目录
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



if __name__ == '__main__':
    with open(r"C:\Users\1\AppData\Local\Temp\_MEI112202\nav.json") as f:
        content = f.read()
        print(content)