import base64

from dnslib import DNSRecord, RR, TXT, QTYPE


def server_encrypt(dns_packet: DNSRecord, data, question):
    data = base64.b64encode(data)
    dns_packet = dns_packet.reply()
    dns_packet.add_answer(RR(question, rtype=QTYPE.TXT, rdata=TXT(data)))
    return dns_packet.pack()


def server_decrypt(dns_packet: bytes):
    query = DNSRecord.parse(dns_packet)
    labels = query.questions[0].qname.label
    i, question = 0, labels[0]
    for tmp in labels[1:]:
        question += b'.' + tmp
    question = bytes.decode(question)
    labels = labels[::-1]
    i, buf = 3, b''
    while i < len(labels):
        buf += labels[i]
        i += 1
    return base64.b64decode(buf), question, query
