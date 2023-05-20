from typing import BinaryIO
import json
import time
import socket
import sys
import os
import select
import pickle

# ==================================================================================
# Packet operations
# ==================================================================================
class Packet:
    def __init__(self, body, seq_no=0, body_length=0, done=False):
        self.body = body
        self.delimiter = b"::HEADER_END::"
        self.header = f"{seq_no}:{body_length}:{done}"

    def getHeader(self):
        return self.header

    def getBody(self):
        return self.body

    def getPacket(self):
        return encode(self.header) + self.delimiter + self.body

# ==================================================================================
# Global functions
# ==================================================================================
def encode(data):
    return json.dumps(data).encode('utf-8')

def decode(data):
    return json.loads(data.decode('utf-8'))

# ==================================================================================
# Reliable UDP Server
# ==================================================================================
class ReliableUDPFileTransfer:
    def __init__(self, host, port, socket_type, fp):
        self.host = host
        self.port = port
        self.socket_type = socket_type
        self.socket = socket.socket(socket.AF_INET, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.fp = fp

    # UDP Listner
    def rdt_recv(self):
        print("Hello, I am a server")
        last_seq_no = 999
        while(True):
            bytesAddressPair = self.socket.recvfrom(256)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            
            packet = pickle.loads(message)
            header = packet.getHeader()
            body = packet.getBody()
            seqNo, bodySize, done = header.split(":")
            
            if seqNo != last_seq_no:
                last_seq_no = seqNo
                if done == "True":
                    self.fp.close()
                    resp = f"ACK\n{last_seq_no}"
                    self.socket.sendto(str.encode(resp), address)
                    break

                self.fp.write(body)

            # SEND ACK BACK
            resp = f"ACK\n{last_seq_no}"
            self.socket.sendto(str.encode(resp), address)

        # Closing socket
        self.socket_close()

    def socket_close(self):
        # Closing socket
        self.socket.close()
        os._exit(0)
    
    def __del__(self):
        # Closing socket
        self.socket.close()

# ==================================================================================
# SERVER ENTRYPOINT
# ==================================================================================
def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    iface = iface if iface else "0.0.0.0"
    addrInfo = socket.getaddrinfo(iface,port,proto=socket.IPPROTO_UDP)
    addr_host, addr_port = addrInfo[0][4]
    socket_type = socket.SOCK_DGRAM
    ReliableUDPFileTransfer(addr_host,addr_port,socket_type,fp).rdt_recv()

# ==================================================================================
# CLIENT ENTRYPOINT
# ==================================================================================
def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    socket_type = socket.SOCK_DGRAM
    addrInfo = socket.getaddrinfo(host,port,proto=socket.IPPROTO_UDP)
    addr_host, addr_port = addrInfo[0][4]

    with socket.socket(socket.AF_INET, socket_type) as s:
        print("Hello, I am a client")
        s.connect((addr_host, addr_port))

        try:
            rdt_send(s, addr_host, addr_port, fp)
        except Exception as e:
            print("Exception occured",e)
            sys.exit()


# ==================================================================================
# CLIENT - RELIABLE DATA TRANSFER
# ==================================================================================
def rdt_send(socket, addr_host, addr_port, fp):
    socket.setblocking(0)
    timeout_in_seconds = 1/10
    seq_no = 0
    while True:
        bytes_read = fp.read(149)
        packet = Packet(bytes_read, seq_no, len(bytes_read), False)

        # FILE COMPLETEY READ
        if not bytes_read:
            packet = Packet(bytes_read, seq_no, len(bytes_read), True)
        
        # SEND PACKET
        socket.sendto(pickle.dumps(packet), (addr_host, addr_port))

        while True:
            ready = select.select([socket], [], [], timeout_in_seconds)
            if ready[0]:
                # WAIT FOR SERVER RESPONSE
                bytesAddressPair = socket.recvfrom(256)
                message = bytesAddressPair[0]
                address = bytesAddressPair[1] 

                expected_message = f"ACK\n{seq_no}"
                if message == str.encode(expected_message):
                    seq_no = (seq_no + 1) % 2
                    break
                else:
                    # IGNORE IF DUPLICATE ACK
                    continue
            else:
                # RESEND PACKET
                socket.sendto(pickle.dumps(packet), (addr_host, addr_port))
            
        if not bytes_read:
            break