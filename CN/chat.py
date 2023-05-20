import socket
import threading
import sys
import os 
from threading import current_thread
import time

class ChatServer:
    def __init__(self, host, port, socket_type):
        self.host = host
        self.port = port
        self.socket_type = socket_type
        self.socket = socket.socket(socket.AF_INET, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    # =============================================
    # TCP Listner
    def listen_to_tcp_client(self, threadCount):
        print("Hello, I am a server")
        self.socket.listen(threadCount)
        thread_no = 0
        while True:
            con, address = self.socket.accept()
            con.settimeout(60)
            thread = threading.Thread(name=str(thread_no),target=self.listen_to_client,
                            args=(con, address)).start()
            thread_no += 1

    def listen_to_client(self, conn, address):
        with conn:
            # get the current thread
            thread = current_thread()
            if self.socket_type != socket.SOCK_DGRAM:
                print(f"connection {thread.name} from {address}")

            decoded_data = ""
            while True:
                data = conn.recv(256)
                if not data:
                    break
                
                decoded_data = data.decode()
                print(f"got message from {address}")

                if decoded_data == "hello\n":
                    conn.sendall(b"world\n")
                    continue

                if decoded_data == "goodbye\n":
                    conn.sendall(b"farewell\n")
                    break
                
                if decoded_data == "exit\n":
                    conn.sendall(b"ok\n")
                    break

                # Send data back
                conn.sendall(data)
        
        # print("Closing connection:", conn)
        if decoded_data == "exit\n":
            self.socket_close()

    # =============================================
    # UDP Listner
    def listen_to_udp_client(self):
        # Listen for incoming datagrams
        print("Hello, I am a server")
        while(True):
            bytesAddressPair = self.socket.recvfrom(256)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            decoded_data = message.decode()
            print(f"got message from {address}")

            if decoded_data == "hello\n":
                self.socket.sendto(b"world\n", address)
                continue

            if decoded_data == "goodbye\n":
                self.socket.sendto(b"farewell\n", address)
            
            if decoded_data == "exit\n":
                self.socket.sendto(b"ok\n", address)
                break
            
            # Sending a reply to client
            self.socket.sendto(message, address)

        if decoded_data == "exit\n":
            self.socket_close()

    # =============================================
    def socket_close(self):
        # print("Closing server socket:", self.socket)
        self.socket.close()
        os._exit(0)
    
    # =============================================
    def __del__(self):
        # print("Closing server socket:", self.socket)
        self.socket.close()

# ==================================================================================
# ==================================================================================
# Chat Server
def chat_server(iface:str, port:int, use_udp:bool) -> None:
    if use_udp:
        addrInfo = socket.getaddrinfo(iface,port,family=socket.AF_INET,proto=socket.IPPROTO_UDP)
        addr_host, addr_port = addrInfo[0][4]
        socket_type = socket.SOCK_DGRAM
        ChatServer(addr_host,addr_port,socket_type).listen_to_udp_client()
    else:
        addrInfo = socket.getaddrinfo(iface,port,family=socket.AF_INET,proto=socket.IPPROTO_TCP)
        addr_host, addr_port = addrInfo[0][4]
        socket_type = socket.SOCK_STREAM
        ChatServer(addr_host,addr_port,socket_type).listen_to_tcp_client(5)

# ==================================================================================
# Chat Client
def chat_client(host:str, port:int, use_udp:bool) -> None:
    if use_udp:
        socket_type = socket.SOCK_DGRAM
        addrInfo = socket.getaddrinfo(host,port,family=socket.AF_INET,proto=socket.IPPROTO_UDP)
        addr_host, addr_port = addrInfo[0][4]
    else:
        socket_type = socket.SOCK_STREAM
        addrInfo = socket.getaddrinfo(host,port,family=socket.AF_INET,proto=socket.IPPROTO_TCP)
        addr_host, addr_port = addrInfo[0][4]

    with socket.socket(socket.AF_INET, socket_type) as s:
        print("Hello, I am a client")
        s.connect((addr_host, addr_port))
        c = 0
        user_text = ""
        while True:
            try:
                user_text = input()
                user_text = user_text[0:255] + "\n"
                s.sendall(str.encode(user_text))
                data = s.recv(256)
                data = data.decode()
                print(data[:len(data)-1])
                if user_text == "goodbye\n" or user_text == "exit\n":
                    break
            except Exception as e:
                # print("Exception occured",e)
                sys.exit()