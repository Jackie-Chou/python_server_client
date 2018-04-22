import argparse
import time
import signal
import sys

def handler(signum, frame):
    print("\n\n")
    sys.exit(0)
signal.signal(signal.SIGINT, handler)

parser = argparse.ArgumentParser(description="program to automatic send messages to server, NOTE this program only generates output to stdout, \
                                              a client process should be running together")
parser.add_argument("-i", "--ipproto", default="ipv4", type=str, help="ipvX proto(default: ipv4)")
parser.add_argument("-p", "--proto", default="tcp", type=str, help="transport protocol tcp/udp(default: tcp)")
parser.add_argument("-n", "--name", required=True, type=str, help="name of the client")
parser.add_argument("--ip1", required=True, type=str, help="ip address of client")
parser.add_argument("--port1", required=True, type=int, help="port of client")
parser.add_argument("--ip2", required=True, type=str, help="ip address of client")
parser.add_argument("--port2", required=True, type=int, help="port of client")
parser.add_argument("-l", "--length", default=1024, type=int, help="length of each msg in Bytes(default: 1024)")
parser.add_argument("--interval", default=0.1, type=float, help="interval of sending consecutive msgs in secs(default: 0.1)")
parser.add_argument("--max_num", default=0, type=int, help="maximum num of sending msgs, 0 means infinity(default: 0)")
args = parser.parse_args()
# client config
print("{}\n{}\n{}\n{}\n{}\n{}\n{}".format(args.ipproto, args.proto, args.name, args.ip1, args.port1, args.ip2, args.port2))
time.sleep(1.0)

msg = "z" * args.length
if args.max_num == 0:
    # begin msg sending
    print("{}".format(msg))
    # sleep
    time.sleep(args.interval)
else:
    for _ in range(args.max_num):
        # begin msg sending
        print("{}".format(msg))
        # sleep
        time.sleep(args.interval)

# end the client
print("\n")
