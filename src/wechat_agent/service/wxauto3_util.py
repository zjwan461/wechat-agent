from typing import Callable

from wxauto import WeChat, Chat
from wxauto.msgs.base import BaseMessage
from wxauto.msgs.friend import FriendTextMessage


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
        print(f"receive from {nickname}`s msg: {content}")
        if isinstance(msg, FriendTextMessage):
            resp = self.msg_handler(nickname, content)
            if resp is not None:
                msg.reply(resp)

    def stop_listening(self):
        return self.wx.StopListening()


if __name__ == '__main__':
    def handler(msg, nickname):
        return "haha"


    service = WeXinAuto3Service(handler)
    service.listen("假洒脱")
    service.wx.KeepRunning()
