import socket
import sys
import time
import struct
from collections import OrderedDict


class Banner:
    def __init__(self):
        self.__banner = OrderedDict(
            [('version', 0),
             ('length', 0),
             ('pid', 0),
             ('realWidth', 0),
             ('realHeight', 0),
             ('virtualWidth', 0),
             ('virtualHeight', 0),
             ('orientation', 0),
             ('quirks', 0)
             ])

    def __setitem__(self, key, value):
        self.__banner[key] = value

    def __getitem__(self, key):
        return self.__banner[key]

    def keys(self):
        return self.__banner.keys()

    def __str__(self):
        return str(self.__banner)


class Minicap:
    def __init__(self, host, port, banner):
        self.buffer_size = 4096
        self.host = host
        self.port = port
        self.banner = banner
        self.capture_complete = False  # 用于控制截图是否完成的标志

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except (socket.error) as e:
            print(e)
            sys.exit(1)
        self.__socket.connect((self.host, self.port))

    def on_image_transfered(self, data):
        #file_name = str(time.time()) + '.jpg'
        file_name = 'screenshot.jpg'
        with open(file_name, 'wb') as f:
            for b in data:
                f.write((b).to_bytes(1, 'big'))
        self.capture_complete = True  # 设置截图完成标志为True

    def consume(self):
        readBannerBytes = 0
        bannerLength = 24
        readFrameBytes = 0
        frameBodyLength = 0
        data = []
        while not self.capture_complete:  # 当截图完成标志为True时退出循环
            try:
                chunk = self.__socket.recv(self.buffer_size)
            except (socket.error) as e:
                print(e)
                sys.exit(1)
            cursor = 0
            buf_len = len(chunk)
            while cursor < buf_len:
                if readBannerBytes < bannerLength:
                    map(lambda i, val: self.banner.__setitem__(self.banner.keys()[i], val),
                        [i for i in range(len(self.banner.keys()))], struct.unpack("<2b5ibB", chunk))
                    cursor = buf_len
                    readBannerBytes = bannerLength
                    #print(self.banner)
                elif readFrameBytes < 4:
                    #print(struct.unpack('B', (chunk[cursor]).to_bytes(1, 'big')))
                    # frameBodyLength += (struct.unpack('B', chunk[cursor])[0] << (readFrameBytes * 8)) >> 0
                    frameBodyLength += (chunk[cursor] << (readFrameBytes * 8)) >> 0
                    cursor += 1
                    readFrameBytes += 1
                else:
                    #print("frame length:{0} buf_len:{1} cursor:{2}".format(frameBodyLength, buf_len, cursor))
                    # pic end
                    if buf_len - cursor >= frameBodyLength:
                        data.extend(chunk[cursor:cursor + frameBodyLength])
                        self.on_image_transfered(data)
                        cursor += frameBodyLength
                        frameBodyLength = readFrameBytes = 0
                        data = []
                    else:
                        data.extend(chunk[cursor:buf_len])
                        frameBodyLength -= buf_len - cursor
                        readFrameBytes += buf_len - cursor
                        cursor = buf_len


def capture_screen():
    mc = Minicap('localhost', 1717, Banner())
    mc.connect()
    mc.consume()

def screen_shotting():
    screen_shot = 0
    while screen_shot < 200:
      capture_screen()
      screen_shot += 1
      time.sleep(0.5)
