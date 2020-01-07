# CS305-IP-over-DNS
A VPN service based on DNS query

## Requirements

python version > 3.6
```   
dnslib==0.9.10
python-pytun==2.3.0
```
just need to run on both client side and server side
```shell
pip3 install requirements.txt
```

## How to use
### SSH Connection

Change the parameters in client_settings.properties
```shell
[client]
# start
sudo python setup.sh
# stop
sudo python shutdown.sh
```
### NAT Setting Connection

```shell
[client]
sudo route add -host 120.78.166.34 gw 192.168.139.2
sudo route add default gw 192.168.77.10

[server]
sudo sysctl net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -s 192.168.77.2 -j SNAT --to 172.16.239.253

[test]
http://pv.sohu.com/cityjson

```
