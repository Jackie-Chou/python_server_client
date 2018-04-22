import threading
import time
from utils import Server

addr_type = raw_input("input server address type(ipv4/ipv6):\n")
serv_type = raw_input("input server address type(tcp/udp): \n")
ip = raw_input("input server ip address: \n")
port = int(input("input server port: \n"))
myServer = Server(addr_type, serv_type, (ip, port))
thread = threading.Thread(target=myServer.start)
thread.start()
while thread.isAlive():
   time.sleep(1.0)
thread._Thread__stop()
print("end")