from typing import Callable

from wxauto4 import WeChat
from wxauto4.msgs import Message, FriendMessage
from wxauto4.msgs.friend import FriendTextMessage
from wxauto4.wx import Chat


class WeXinAuto4Service:

    def __init__(self, msg_handler: Callable):
        self.msg_handler = msg_handler
        self.wx = WeChat()
        self.wx.Show()

    def listen(self, nickname: str):
        self.wx.AddListenChat(nickname=nickname, callback=self.on_message)

    def on_message(self, msg: Message, chat: Chat):
        if isinstance(msg, FriendTextMessage):
            print(msg)
            resp = self.msg_handler(msg.content)
            chat.SendMsg(resp)

    def get_wx(self):
        return self.wx


def handler(msg):
    return "haha"


if __name__ == '__main__':
    service = WeXinAuto4Service(handler)
    service.listen("女王")
    service.wx.KeepRunning()
