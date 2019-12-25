import base64

from dnslib import DNSRecord


def client_encrypt(data):
    domain = 'group-zzd.cs305.fun'
    data = bytes.decode(base64.b64encode(data))
    i, num, seg = 0, len(data), 50
    while i * seg < num:
        domain = data[i * seg:(i + 1) * seg] + '.' + domain
        i += 1
    query = DNSRecord.question(domain, "TXT")
    return query.pack()


def client_decrypt(data):
    response = DNSRecord.parse(data)
    if len(response.rr) == 0:
        return
    return base64.b64decode(response.rr[0].rdata.data[0])
