from typing import BinaryIO
import json
import time
import socket
import sys
import os
import select
import pickle
import collections
import math

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

def binary(num, length=8):
    return format(num, '#0{}b'.format(length+2))

# ==================================================================================
# Reliable UDP Server - go-back-N Protocol
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
    def gbn_recv(self):
        print("Hello, I am a server")
        last_seq_no = -1
        while(True):
            bytesAddressPair = self.socket.recvfrom(512)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            
            packet = pickle.loads(message)
            header = packet.getHeader()
            body = packet.getBody()
            seqNo, bodySize, done = header.split(":")
            seqNo = int(seqNo,2)

            if last_seq_no > seqNo:
                resp = f"ACK\n{seqNo}"
                self.socket.sendto(str.encode(resp), address)
                continue
            
            if seqNo == (last_seq_no+1):
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


def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    iface = iface if iface else "0.0.0.0"
    addrInfo = socket.getaddrinfo(iface,port,proto=socket.IPPROTO_UDP)
    addr_host, addr_port = addrInfo[0][4]
    socket_type = socket.SOCK_DGRAM
    ReliableUDPFileTransfer(addr_host,addr_port,socket_type,fp).gbn_recv()

# ==================================================================================
# CLIENT ENTRYPOINT
# ==================================================================================
def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    socket_type = socket.SOCK_DGRAM
    addrInfo = socket.getaddrinfo(host,port,proto=socket.IPPROTO_UDP)
    addr_host, addr_port = addrInfo[0][4]

    with socket.socket(socket.AF_INET, socket_type) as s:
        print("Hello, I am a client")
        s.connect((addr_host, addr_port))

        try:
            gbn_send(s, addr_host, addr_port, fp)
        except Exception as e:
            print("Exception occured",e)
            sys.exit()


# ==================================================================================
# CLIENT - go-back-N Protocol
# ==================================================================================
def gbn_send(socket, addr_host, addr_port, fp):
    socket.setblocking(0)
    timeout_in_seconds = 1/10
    
    buffer = collections.deque([])
    resend = False
    send_done = False
    window_size = 4
    file_read_size = 397
    send_seq_no = 0
    recv_seq_no = 0

    while True:
            buffer_size = len(buffer)
            # READ AND SEND
            while len(buffer) < window_size and not send_done:
                send_seqNo_binary = binary(send_seq_no)
                if (byte := fp.read(file_read_size)):
                    packet = Packet(byte, send_seqNo_binary, len(byte), False)
                else:
                    # FILE COMPLETEY READ
                    packet = Packet(byte, send_seqNo_binary, len(byte), True)
                    send_done = True
                
                # SEND PACKET
                socket.sendto(pickle.dumps(packet), (addr_host, addr_port))
                buffer.append(byte)
                send_seq_no = (send_seq_no + 1) % 256

                if send_done:
                    break

            # WAIT FOR SERVER RESPONSE
            ready = select.select([socket], [], [], timeout_in_seconds)
            if ready[0]:
                bytesAddressPair = socket.recvfrom(512)
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]

                expected_message = f"ACK\n{recv_seq_no}"
                if message == str.encode(expected_message):
                    recv_seq_no = (recv_seq_no + 1) % 256
                    buffer.popleft()
                    window_size += 1
                    window_size = min(window_size,16) # Capping window size at 16
            else:
                # RESET BUFFER POINTER AND RESEND PACKET
                send_done = False
                window_size = max(1,window_size//2)
                send_seq_no = recv_seq_no
                buffer.clear()
                fp.seek(send_seq_no * file_read_size)
            
            if send_done and send_seq_no == recv_seq_no:
                break    
