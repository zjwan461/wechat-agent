import socket
import platform

import GPUtil
import psutil
from src.wechat_agent.service.db_util import SqliteSqlalchemy, SysInfo
from src.wechat_agent.constants import sys_info_id


def get_cpu_info():
    result = {}
    cores = psutil.cpu_count()
    result['cores'] = cores
    use_percent = psutil.cpu_percent(interval=1)
    result['use_percent'] = str(use_percent) + '%'
    result['free_percent'] = str(round(100 - use_percent, 2)) + '%'
    return result


def get_memory_info():
    result = {}
    # 获取系统内存信息
    memory = psutil.virtual_memory()

    # 总内存（以字节为单位）
    total_memory = memory.total
    # 已使用内存（以字节为单位）
    used_memory = memory.used
    # 内存使用率（百分比）
    memory_percent = memory.percent

    result['total_memory'] = f"{total_memory / (1024 * 1024 * 1024):.2f} GB"
    result['used_memory'] = f"{used_memory / (1024 * 1024 * 1024):.2f} GB"
    result['free_memory'] = f"{(total_memory - used_memory) / (1024 * 1024 * 1024):.2f} GB"
    result['memory_percent'] = f"{memory_percent}%"
    return result


def get_os_info():
    result = {'os': platform.system(), 'arch': platform.machine()}
    hostname = socket.gethostname()
    result['hostname'] = hostname
    result['ip'] = socket.gethostbyname(hostname)
    return result


def get_gpu_info():
    result = []
    gpus = GPUtil.getGPUs()
    if len(gpus) > 0:
        for gpu in gpus:
            item = {"name": f"{gpu.name}", "memory": f"{gpu.memoryTotal / 1024:.2f}", "driver": f"{gpu.driver}",
                    "memory_free": f"{gpu.memoryFree}"}
            # 显存使用率
            result.append(item)
    else:
        if platform.system() == 'Windows':
            import wmi
            try:
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    gpu_info = {
                        "name": gpu.Name,
                        "driver": gpu.DriverVersion,
                    }
                    if not gpu.AdapterRAM:
                        continue
                    memory = round(gpu.AdapterRAM / (1024 ** 3), 2)
                    if memory < 0:
                        continue
                    gpu_info["memory"] = memory
                    result.append(gpu_info)

            except Exception as e:
                print(f"获取非NVIDIA GPU信息失败: {e}")
    return result


def is_cuda_available():
    gpus = GPUtil.getGPUs()
    return len(gpus) > 0


def get_sys_info():
    session = SqliteSqlalchemy().session
    sys_info = session.query(SysInfo).get(sys_info_id)
    session.close()
    if sys_info is None:
        return {}
    else:
        return sys_info.to_dic()


if __name__ == '__main__':
    res = get_cpu_info()
    print(res)
    res2 = get_memory_info()
    print(res2)
    res3 = get_os_info()
    print(res3)
    res4 = get_gpu_info()
    print(res4)
