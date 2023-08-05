#-*- coding:utf-8 -*-
"""
    core

    Copyright (c) 2018 Balus CO., LTD.
    Coder: T. Shinaji 
    
    2018/11/01

"""
import socket
import signal
from typing import List
import traceback
import time
import platform

class ArtNetRouter:

    def __init__(
            self,
            dst_ip, dst_port=6454,
            src_port=6454, buff_size=1024,
            listening_ip="0.0.0.0",
            disp_length=20
    ):
        # type: (ArtNetRouter, str, int, int, int, str, int) -> None
        """
        init
        :param dst_ip: destination ip address
        :param dst_port: destination port
        :param src_port: source port
        :param buff_size: buffer size (bytes)
        :param listening_ip: listening ip address
        :param disp_length: display length of ArtNet signal
        """

        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.buff_size = buff_size
        self.listening_ip = listening_ip
        if "Darwin" in platform.platform() and listening_ip == "0.0.0.0":
            self.listening_ip = ""
        self.disp_length = disp_length

    def start_routing(self, is_debug=False, is_test_mode=False):
        # type: (ArtNetRouter, bool) -> None
        """
        start ArtNer transfer
        :param is_debug: if true print console log,
        :param is_test_mode: if true, quit in 5s,
        this script is assuming ArtNet is working with broadcast packets
        """
        try:
            ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if self.dst_ip.split(".")[-1] == "255":
                ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as rs:
                # rs.connect((self.src_ip, self.port))
                rs.bind((self.listening_ip, self.src_port))
                if is_test_mode:
                    rs.settimeout(1.0)
                begin_time = time.time()
                while True:
                    try:
                        if is_test_mode:
                            if time.time() - begin_time > 5:
                                break
                        msg, src_ip_port = rs.recvfrom(self.buff_size)
                        ip, port = src_ip_port
                        if ip.split(".")[0] == self.dst_ip.split(".")[0]:
                            if is_debug:
                                print(f"reject {0}".format(ip))
                            continue
                        if is_debug:
                            print(ip, msg[0:min(self.disp_length, len(msg))])
                            # if port == self.port:
                            # print(f"Send {0}".format(msg))
                        ss.connect((self.dst_ip, self.src_port))
                        ss.send(msg)
                    except KeyboardInterrupt:
                        print("CTRL-C signal has been received.")
                        break
                    except:
                        print(traceback.format_exc())
        except KeyboardInterrupt:
            print("CTRL-C signal has been received.")


