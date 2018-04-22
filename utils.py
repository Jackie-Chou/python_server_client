import socket
import threading
import msvcrt
import time
from datetime import datetime

class Server():
    """Server process class"""
    def __init__(self, addr_type, serv_type, addr):
        """ addr_type: str, can be 'ipv4' or 'ipv6'
            serv_type: str, can be 'tcp' or 'udp'
            addr: needed only when serv_type == 'tcp'"""
        if addr_type == 'ipv4':
            self.addr_type = socket.AF_INET
        elif addr_type == 'ipv6':
            self.addr_type = socket.AF_INET6
        else:
            raise Exception("invalid addr_type", addr_type, "should be 'ipv4' or 'ipv6'")

        if serv_type == 'tcp':
            self.serv_type = socket.SOCK_STREAM
        elif serv_type == 'udp':
            self.serv_type = socket.SOCK_DGRAM
        else:
            raise Exception("invalid serv_type", serv_type, "should be 'tcp' or 'udp'")

        self.addr = addr
        self.sock = socket.socket(self.addr_type, self.serv_type)
        self.sock.bind(addr)
        # used to lock threads
        self.lock = threading.Lock()
        print("[{}] Server: creates a socket at address: {}".format(datetime.now(), self.addr))

    def start(self, max_queue_num=5, bufsize=4096):
        self.max_queue_num = max_queue_num
        self.bufsize = bufsize
        '''start running of Server process'''
        if self.serv_type == socket.SOCK_STREAM:
            thread = threading.Thread(target=self._tcp_start)
            thread.start()
        else:
            thread = threading.Thread(target=self._udp_start)
            thread.start()
        time.sleep(1.0)
        print("press ~ to end the server")
        while thread.isAlive():
            thread.join(0.1)
            self.lock.acquire()
            #print("heer")
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == "~":
                    thread._Thread__stop()
            self.lock.release()
        self.sock.close()
        print("[{}] Server: socket closed, server exit".format(datetime.now()))

    def _tcp_start(self):
        self.sock.listen(self.max_queue_num)
        print("[{}] Server: listening for connection at address {}...".format(datetime.now(), self.addr))
        server_id = 0
        # iterate to serve
        while 1:
            # accept from client
            (clientsocket, clientaddr) = self.sock.accept()
            server_id += 1
            thread = threading.Thread(target=self._tcp_serv, args=(clientsocket, clientaddr, server_id))
            thread.start()

    def _udp_start(self):
        print("[{}] Server: started at address {}...".format(datetime.now(), self.addr))
        try:
            while 1:
                # receive data and send back
                data, clientaddr = self.sock.recvfrom(self.bufsize)
                print("[{}] Server receive:{}({})".format(datetime.now(), data, clientaddr))
                if data:
                    # just send back
                    self.sock.sendto(data, clientaddr)
                    print("[{}] Server send: {}({})".format(datetime.now(), data, clientaddr))
        except Exception as e:
            print("[{}] Server : error '{}' occured".format(datetime.now(), e))
        '''
        thread = threading.Thread(target=self._udp_serv)
        thread.start()
        while thread.isAlive():
            thread.join(1.0)
        '''

    def _tcp_serv(self, clientsocket, clientaddr, id):
        print("[{}] Server {}: client accepted at {}".format(datetime.now(), id, clientaddr))
        rthread = threading.Thread(target=self._tcp_recv, args=(clientsocket, id))
        sthread = threading.Thread(target=self._tcp_send, args=(clientsocket, id))
        rthread.start()
        sthread.start()
        while 1:
            if not rthread.isAlive():
                sthread._Thread__stop()
                break
            if not sthread.isAlive():
                rthread._Thread__stop()
                break
        # close connection with this client and repeat
        clientsocket.close()
        print("[{}] Server {}: client at address {} disconnected".format(datetime.now(), id, clientaddr))

    def _udp_serv(self):
        try:
            while 1:
                # receive data and send back
                data, clientaddr = self.sock.recvfrom(self.bufsize)
                print("[{}] Server receive:{}({})".format(datetime.now(), data, clientaddr))
                if data:
                    # just send back
                    self.sock.sendto(data, clientaddr)
                    print("[{}] Server send: {}({})".format(datetime.now(), data, clientaddr))
        except Exception as e:
            print("[{}] Server : error '{}' occured".format(datetime.now(), e))

    def _tcp_recv(self, clientsocket, id):
        try:
            # receive data and display
            while 1:
                data = clientsocket.recv(self.bufsize)
                print("[{}] Server {} receive: {}".format(datetime.now(), id, data))
                if data is None:
                    # if None received, means client close the socket
                    break
        except Exception as e:
            pass

    def _tcp_send(self, clientsocket, id):
        #TODO: send to multiple clients in parallel
        try:
            # receive data and send back
            while 1:
                self.lock.acquire()
                msg = raw_input("[{}] Server {} input: \n".format(datetime.now(), id))
                self.lock.release()
                # send back
                clientsocket.sendall(msg)
        except Exception as e:
            print("[{}] Server {} exits".format(datetime.now(), id))



class Client():
    """Client process class"""
    def __init__(self, addr_type, serv_type, name, addr):
        """ addr_type: str, can be 'ipv4' or 'ipv6'
            serv_type: str, can be 'tcp' or 'udp'
            addr: needed only when serv_type == 'tcp'"""
        if addr_type == 'ipv4':
            self.addr_type = socket.AF_INET
        elif addr_type == 'ipv6':
            self.addr_type = socket.AF_INET6
        else:
            raise Exception("invalid addr_type", addr_type, "should be 'ipv4' or 'ipv6'")

        if serv_type == 'tcp':
            self.serv_type = socket.SOCK_STREAM
        elif serv_type == 'udp':
            self.serv_type = socket.SOCK_DGRAM
        else:
            raise Exception("invalid serv_type", serv_type, "should be 'tcp' or 'udp'")

        self.addr = addr
        self.name = name
        self.sock = socket.socket(self.addr_type, self.serv_type)
        self.sock.bind(addr)
        print("[{}] Client {}: creates a socket at address: {}".format(datetime.now(), self.name, self.addr))

    def start(self, server_addr, bufsize=2048):
        '''start running of Client process'''
        self.server_addr = server_addr
        self.bufsize = bufsize
        if self.serv_type == socket.SOCK_STREAM:
            thread = threading.Thread(target=self._tcp_start)
            thread.start()
        else:
            thread = threading.Thread(target=self._udp_start)
            thread.start()
        thread.join()
        self.sock.close()
        print("[{}] Client {}: socket closed, client exit".format(datetime.now(), self.name))

    def _tcp_start(self):
        self.sock.connect(self.server_addr)
        print("[{}] Client {}; connected to server at {}".format(datetime.now(), self.name, self.server_addr))
        rthread = threading.Thread(target = self._tcp_recv)
        sthread = threading.Thread(target = self._tcp_send)
        rthread.start()
        sthread.start()
        sthread.join()
        # NOTE: rthread won't stop normally
        rthread._Thread__stop()

    def _udp_start(self):
        print("[{}] Client {}; ready to send to server at {}".format(datetime.now(), self.name, self.server_addr))
        rthread = threading.Thread(target = self._udp_recv)
        sthread = threading.Thread(target = self._udp_send)
        rthread.start()
        sthread.start()
        sthread.join()
        # NOTE: rthread won't stop normally
        rthread._Thread__stop()

    def _tcp_send(self):
        # NOTE: error can occur when sending and receiving
        try:
            while 1:
                # send a small chunk of data
                msg = raw_input("input: \n")
                if msg == '':
                    break
                self.sock.sendall(msg)
                print("[{}] Client {} send: {}".format(datetime.now(), self.name, msg))
        except Exception as e:
            print("[{}] Client {}: disconnected with server({})".format(datetime.now(), self.name, e))

    def _tcp_recv(self):
        # NOTE: error can occur when sending and receiving
        try:
            while 1:
                recv_msg = self.sock.recv(self.bufsize)
                print("[{}] Client {} receive: {}".format(datetime.now(), self.name, recv_msg))
        except Exception as e:
            print("[{}] Client {}: disconnected with server({})".format(datetime.now(), self.name, e))

    def _udp_send(self):
        try:
            while 1:
                # send a small chunk of data
                msg = raw_input("input: \n")
                if msg == '':
                    break
                self.sock.sendto(msg, self.server_addr)
                print("[{}] Client {} send: {}".format(datetime.now(), self.name, msg))
        except Exception as e:
            print("[{}] Client {}: disconnected with server({})".format(datetime.now(), self.name, e))

    def _udp_recv(self):
        try:
            while 1:
                # receive it
                recv_msg, addr = self.sock.recvfrom(self.bufsize)
                print("[{}] Client {} receive: {}({})".format(datetime.now(), self.name, recv_msg, addr))
        except Exception as e:
            print("[{}] Client {}: disconnected with server({})".format(datetime.now(), self.name, e))



