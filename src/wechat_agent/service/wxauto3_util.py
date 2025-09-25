from typing import Callable

from wxauto import WeChat, Chat
from wxauto.msgs.base import BaseMessage
from wxauto.msgs.friend import FriendTextMessage

from wechat_agent.SysEnum import WechatReplyType
from wechat_agent.logger_config import get_logger

logger = get_logger(__name__)


class WeXinAuto3Service:

    def __init__(self, msg_handler: Callable):
        self.msg_handler = msg_handler
        self.wx = WeChat()

    def listen(self, nickname: str):
        return self.wx.AddListenChat(nickname=nickname, callback=self.on_message)

    def remove_listen(self, nickname: str):
        return self.wx.RemoveListenChat(nickname=nickname)

    def on_message(self, msg: BaseMessage, chat: Chat):
        nickname = chat.ChatInfo()['chat_name']
        content = msg.content
        logger.info(f"receive from {nickname}`s msg: {content}")
        if isinstance(msg, FriendTextMessage):
            resp, resp_type = self.msg_handler(nickname, content)
            if resp is not None:
                if resp_type == WechatReplyType.REPLY:
                    msg.reply(resp)
                elif resp_type == WechatReplyType.QUOTE:
                    msg.quote(resp)
                else:
                    logger.warning(f'unknown resp type: {resp_type}, will use reply to handle it')
                    msg.reply(resp)

    def stop_listening(self):
        return self.wx.StopListening()


if __name__ == '__main__':
    def handler(msg, nickname):
        return "haha"


    service = WeXinAuto3Service(handler)
    service.listen("假洒脱")
    service.wx.KeepRunning()
