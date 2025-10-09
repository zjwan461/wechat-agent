import os

token_header = "Authorization"
token_prefix = "Bearer "
token_white_list = [r'^/ui/.*', "/api/auth/login", "/api/auth/register", "/api/base/sys-info",
                    "/api/base/git-repo", "/api/auth/yzm", "/api/auth/refresh-token"]
gitee_url = "https://gitee.com/zjwan461/wechat-agent"
github_url = "https://github.com/zjwan461/wechat-agent"
server_port = os.getenv('wa_port', 8080)
server_host = os.getenv('wa_host', "0.0.0.0")
db_url = "sqlite:///{0}/wechat-agent/db/wxa.db"
sys_info_id = 1
SECRET_KEY = "your-secret-key-keep-it-safe"
token_timeout = 30
running_env = os.getenv('wa_env', 'command')