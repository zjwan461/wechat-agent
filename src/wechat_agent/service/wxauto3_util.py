from typing import Callable

from wxauto import WeChat, Chat
from wxauto.msgs.base import BaseMessage
from wxauto.msgs.friend import FriendTextMessage


class WeXinAuto3Service:

    def __init__(self, msg_handler: Callable):
        self.msg_handler = msg_handler
        self.wx = WeChat()

    def listen(self, nickname: str):
        self.wx.AddListenChat(nickname=nickname, callback=self.on_message)
        self.wx.KeepRunning()

    def on_message(self, msg: BaseMessage, chat: Chat):
        print(f"receive from {chat.ChatInfo()['chat_name']}`s msg: {msg.content}")
        if isinstance(msg, FriendTextMessage):
            resp = self.msg_handler(msg.content)
            msg.reply(resp)

    def stop_listening(self):
        return self.wx.StopListening()


def handler(msg):
    return "haha"


if __name__ == '__main__':
    service = WeXinAuto3Service(handler)
    service.listen("文件传输助手")
    #
