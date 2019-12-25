import queue
import server_wrapper
import binascii

from socket import *
from pytun import *
from threading import Thread

'''
    me = '192.168.77.10'
    he = '192.168.77.2'
'''
tun = TunTapDevice(flags=IFF_TUN | IFF_NO_PI)
tun.addr = '192.168.77.10'
tun.netmask = '255.255.255.0'
tun.mtu = 150
tun.up()


class Packet:
    def __init__(self, payload, question, query, addr):
        self.payload = payload
        self.question = question
        self.query = query
        self.addr = addr

def read_tunnel(contents):
    while True:
        data = tun.read(tun.mtu)
        contents.put(data)


def send_packet(s, contents, packets):
    while True:
        if contents.empty():
            continue
        p = packets.get()
        data = contents.get()
        s.sendto(server_wrapper.server_encrypt(p.query, data, p.question), p.addr)


def recv_packet(s: socket, packets):
    while True:
        try:
            data, addr = s.recvfrom(2048)
            data, question, query = server_wrapper.server_decrypt(data)
            p = Packet(data, question, query, addr)
            if packets.full():
                p2 = packets.get()
                s.sendto(server_wrapper.server_encrypt(p2.query, b'hi', p2.question), p2.addr)
            packets.put(p)
            if question != 'aGVsbG8=.group-7.cs305.fun' and question:
                tun.write(data)
            else:
                print('receive empty packet')
        except binascii.Error:
            continue


if __name__ == '__main__':
    addr = ('0.0.0.0', 53)
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(addr)
    packets = queue.Queue(1)
    contents = queue.Queue(-1)
    recv_thread = Thread(target=recv_packet, args=(s, packets,))
    send_thread = Thread(target=send_packet, args=(s, contents, packets,))
    read_thread = Thread(target=read_tunnel, args=(contents,))
    recv_thread.start()
    send_thread.start()
    read_thread.start()
