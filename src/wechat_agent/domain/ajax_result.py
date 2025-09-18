def success(data=None):
    return {"code": 0, "msg": "success", "data": data}


def error(msg="error"):
    return {"code": 1, "msg": msg, "data": None}
