def success(data=None):
    return {"code": 0, "msg": "success", "data": data}


def error(msg="system is too busy"):
    return {"code": 1, "msg": msg, "data": None}


def build(code, msg, data):
    return {"code": code, "msg": msg, "data": data}
