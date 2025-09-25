from typing import Callable

from wxauto4 import WeChat
from wxauto4.msgs.base import BaseMessage
from wxauto4.msgs.friend import FriendTextMessage
from wxauto4.wx import Chat

from wechat_agent.SysEnum import WechatReplyType
from wechat_agent.logger_config import get_logger

logger = get_logger(__name__)


class WeXinAuto4Service:

    def __init__(self):
        self.msg_handlers = {}
        self.wx = WeChat()

    def listen(self, nickname: str, msg_handler: Callable):
        self.msg_handlers[nickname] = msg_handler
        return self.wx.AddListenChat(nickname=nickname, callback=self.on_message)

    def remove_listen(self, nickname: str):
        self.msg_handlers.pop(nickname)
        return self.wx.RemoveListenChat(nickname=nickname)

    def on_message(self, msg: BaseMessage, chat: Chat):
        nickname = chat.ChatInfo()['chat_name']
        content = msg.content
        logger.info(f"receive from {nickname}`s msg: {content}")
        if isinstance(msg, FriendTextMessage):
            msg_handler = self.msg_handlers[nickname]
            resp, resp_type = msg_handler(nickname, content)
            if resp is not None:
                if resp_type == WechatReplyType.REPLY:
                    chat.SendMsg(resp)
                elif resp_type == WechatReplyType.QUOTE:
                    msg.quote(resp)
                else:
                    logger.warning(f'unknown resp type: {resp_type}, will use reply to handle it')
                    chat.SendMsg(resp)

    def stop_listening(self):
        return self.wx.StopListening()


if __name__ == '__main__':
    def handler(msg, nickname):
        return "haha", WechatReplyType.REPLY


    service = WeXinAuto4Service()
    service.listen("假洒脱", handler)
    service.wx.KeepRunning()
