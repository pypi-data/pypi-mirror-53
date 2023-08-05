#-*- coding:utf-8 -*-
"""
    main

    Copyright (c) 2018 Balus CO., LTD.
    Coder: T. Shinaji 
    
    2018/11/01

"""
from ArtNetRouter import ArtNetRouter
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='ArtNet router')
    parser.add_argument('--debug', '-D', action='store_true',
                        default=False,
                        dest='is_debug',
                        help='Enable debug mode')
    parser.add_argument('--src_port', '-s', type=int,
                        default=6454,
                        dest='src_port',
                        help='source port of ArtNet signals are arrived')
    parser.add_argument('--dst_port', '-d', type=int,
                        default=6454,
                        dest='dst_port',
                        help='destination port of ArtNet signals are sent')
    parser.add_argument(
        '--dst_ip', '-i', type=str,
        required=True,
        dest='dst_ip',
        help='destination port of ArtNet signals are sent')
    parser.add_argument(
        '--buff_size', '-b', type=int,
        default=1024,
        dest='buff_size',
        help='buffer size, the default buffer size is 1024')
    parser.add_argument(
        '--listen_ip', '-l', type=str,
        default="0.0.0.0",
        dest='listen_ip',
        help='listening ip address, the default value is 0.0.0.0'
    )

    args = parser.parse_args()
    is_debug = args.is_debug
    if is_debug:
        print("Debug mode")
    router = ArtNetRouter(
        src_port=args.src_port,
        dst_port=args.dst_port,
        dst_ip=args.dst_ip,
        buff_size=args.buff_size,
        listening_ip=args.listen_ip
    )
    router.start_routing(is_debug)
