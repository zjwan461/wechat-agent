from flask import Flask, request, g, jsonify
from src.wechat_agent.constants import token_header, token_prefix, token_white_list, gitee_url, github_url
from src.wechat_agent.domain.ajax_result import success, error
from src.wechat_agent.service.jwt_util import verify_token
import re

app = Flask(__name__)


@app.before_request
def auth():
    if request.path in token_white_list:
        return None
    for rule in token_white_list:
        if bool(re.fullmatch(rule, request.path)):
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


@app.route("/api/login", methods=["POST"])
def hello():
    req = request.json
    print(req)
    return jsonify(success())


@app.route("/api/base/git-repo")
def git_repo():
    return jsonify(success({"giteeUrl": gitee_url, "githubUrl": github_url}))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
