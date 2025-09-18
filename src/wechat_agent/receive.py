from wxauto import WeChat
from wxauto.msgs import FriendMessage
import time

wx = WeChat()

# 消息处理函数
def on_message(msg, chat):
    text = f'[{msg.type} {msg.attr}]{chat} - {msg.content}'
    print(text)
    with open('msgs.txt', 'a', encoding='utf-8') as f:
        f.write(text + '\n')

    if msg.type in ('image', 'video'):
        print(msg.download())

    # if isinstance(msg, FriendMessage):
    #     print(msg)
        # time.sleep(len(msg.content))
        # msg.quote('收到')

    ...# 其他处理逻辑，配合Message类的各种方法，可以实现各种功能

# 添加监听，监听到的消息用on_message函数进行处理
wx.AddListenChat(nickname="开发七部招聘需求群", callback=on_message)

# ... 程序运行一段时间后 ...

# 移除监听
# wx.RemoveListenChat(nickname="女王👸")

wx.KeepRunning()