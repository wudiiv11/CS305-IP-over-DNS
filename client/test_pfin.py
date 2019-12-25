import time
import queue
import threading
import client_wrapper

from socket import *
from pytun import *

'''
    me = '192.168.77.2'
    he = '192.168.77.10'
    server = 'group-zzd.cs305.fun'
'''

addr = ('120.78.166.34', 53)
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(5)

tun = TunTapDevice(flags=IFF_TUN | IFF_NO_PI)
tun.addr = '192.168.77.2'
tun.netmask = '255.255.255.0'
tun.mtu = 150
tun.up()


def read_tunnel(contents):
    while True:
        data = tun.read(tun.mtu)
        contents.put(data)


def send_packet(s, addr, tun):
    while True:
        # if contents.empty():
        #    data = b'hello'
        #else:
        #    data = contents.get()
        data = tun.read(tun.mtu)
        s.sendto(client_wrapper.client_encrypt(data), addr)
        # time.sleep(2)


def dummy_packet(s, addr):
    while True:
        for _ in range(1):
            data = b'hello'
            s.sendto(client_wrapper.client_encrypt(data), addr)
        time.sleep(0.2)


def receive_packet(s, tun):
    while True:
        data, addr = s.recvfrom(2048)
        data = client_wrapper.client_decrypt(data)
        if data:
            tun.write(data)


if __name__ == '__main__':
    cnt = 0
    packets = queue.Queue()
    contents = queue.Queue(-1)
    addr = ('120.78.166.34', 53)
    s = socket(AF_INET, SOCK_DGRAM)

    recv_thread = threading.Thread(target=receive_packet, args=(s, tun))
    send_thread = threading.Thread(target=send_packet, args=(s, addr, tun))
    dummy_thread = threading.Thread(target=dummy_packet, args=(s, addr))
    # read_thread = threading.Thread(target=read_tunnel, args=(contents,))
    recv_thread.start()
    send_thread.start()
    dummy_thread.start()
    # read_thread.start()
