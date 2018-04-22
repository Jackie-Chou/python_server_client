from utils import Client

addr_type = raw_input("input client address type(ipv4/ipv6):\n")
serv_type = raw_input("input client address type(tcp/udp): \n")
name = raw_input("input client name: \n")
ip = raw_input("input client ip address: \n")
port = int(input("input client port: \n"))
sip = raw_input("input server ip address: \n")
sport = int(input("input server port: \n"))
myClient = Client(addr_type, serv_type, name, (ip, port))
myClient.start((sip, sport))
