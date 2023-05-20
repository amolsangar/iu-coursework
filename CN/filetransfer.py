from typing import BinaryIO
import socket
import sys
import os 
import time
from io import BytesIO

class FileTransferServer:
    def __init__(self, host, port, socket_type, fp):
        self.host = host
        self.port = port
        self.socket_type = socket_type
        self.socket = socket.socket(socket.AF_INET, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.fp = fp

    # =============================================
    # TCP Listner
    def listen_to_tcp_client(self):
        print("Hello, I am a server")
        self.socket.listen()
        while True:
            con, address = self.socket.accept()
            con.settimeout(60)
            with con:
                while True:
                    data = con.recv(256)
                    if not data:
                        self.fp.close()
                        break
                    
                    self.fp.write(data)
            
            # Closing socket
            self.socket_close()

    # =============================================
    # UDP Listner
    def listen_to_udp_client(self):
        print("Hello, I am a server")
        while(True):
            bytesAddressPair = self.socket.recvfrom(256)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            if not message or len(message) == 0:
                self.fp.close()
                break
            
            self.fp.write(message)

        # Closing socket
        self.socket_close()

    # =============================================
    def socket_close(self):
        # Closing socket
        self.socket.close()
        os._exit(0)
    
    # =============================================
    def __del__(self):
        # Closing socket
        self.socket.close()

# ==================================================================================

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    iface = iface if iface else "0.0.0.0"
    if use_udp:
        addrInfo = socket.getaddrinfo(iface,port,proto=socket.IPPROTO_UDP)
        addr_host, addr_port = addrInfo[0][4]
        socket_type = socket.SOCK_DGRAM
        FileTransferServer(addr_host,addr_port,socket_type,fp).listen_to_udp_client()
    else:
        addrInfo = socket.getaddrinfo(iface,port)
        addr_host, addr_port = addrInfo[0][4]
        socket_type = socket.SOCK_STREAM
        FileTransferServer(addr_host,addr_port,socket_type,fp).listen_to_tcp_client()

def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    if use_udp:
        socket_type = socket.SOCK_DGRAM
        addrInfo = socket.getaddrinfo(host,port,proto=socket.IPPROTO_UDP)
        addr_host, addr_port = addrInfo[0][4]
    else:
        socket_type = socket.SOCK_STREAM
        addrInfo = socket.getaddrinfo(host,port)
        addr_host, addr_port = addrInfo[0][4]

    with socket.socket(socket.AF_INET, socket_type) as s:
        print("Hello, I am a client")
        s.connect((addr_host, addr_port))

        try:
            while True:
                bytes_read = fp.read(256)
                # UDP
                if use_udp:
                    if not bytes_read:
                        s.sendto(b"", (addr_host, addr_port))
                        break
                    s.sendto(bytes_read, (addr_host, addr_port))
                # TCP
                else:
                    if not bytes_read:
                        s.send(b"")
                        break
                    s.send(bytes_read)
        except Exception as e:
            # print("Exception occured",e)
            sys.exit()
