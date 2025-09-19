import constants
from src.wechat_agent.controller.wechat_agent_controller import app


if __name__ == "__main__":
    app.run(host=constants.server_host, port=constants.server_port)
