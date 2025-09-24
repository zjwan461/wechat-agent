import time

from wxauto import WeChat


wx = WeChat()

# wx.Show()

time.sleep(1)

wx.SendMsg("haha","文件传输助手")
