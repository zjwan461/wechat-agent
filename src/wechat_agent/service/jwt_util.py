import jwt
import datetime
from jwt import exceptions
from src.wechat_agent.constants import SECRET_KEY

# 密钥（实际应用中应妥善保管，不要硬编码）



def generate_token(user_id):
    """生成 JWT Token"""
    # 设置过期时间（例如：2小时后过期）
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    # 构建 payload
    payload = {
        "user_id": user_id,
        "exp": expiration,  # 过期时间（必须是 UTC 时间）
        "iat": datetime.datetime.utcnow()  # 签发时间
    }

    # 生成 Token（使用 HS256 算法）
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    """验证 Token 并返回 payload"""
    try:
        # 验证 Token 并解析 payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "payload": payload, "error": None}
    except exceptions.ExpiredSignatureError:
        # Token 已过期
        return {"valid": False, "payload": None, "error": "Token has expired"}
    except exceptions.InvalidTokenError:
        # Token 无效（格式错误等）
        return {"valid": False, "payload": None, "error": "Invalid token"}
    except exceptions.InvalidSignatureError:
        # 签名验证失败
        return {"valid": False, "payload": None, "error": "Invalid signature"}
