import socket
import time

IP_ADDRESS = "127.0.0.1"
PORT_NO = 6789
# IP_ADDRESS = "138.197.63.247"
# PORT_NO = 443

PACKET_SIZE = 1024
BUFFER_SIZE = 500 * 1024 * 1024
msg = b'a'
nr_chunks = BUFFER_SIZE // PACKET_SIZE


def udp(stopwait):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if stopwait:
        sock.settimeout(0.5)
    nrmsg = 0
    nrbytes = 0
    start_time = time.time()
    for i in range(nr_chunks):
        sock.sendto(msg * PACKET_SIZE, (IP_ADDRESS, PORT_NO))
        nrmsg += 1
        nrbytes += len(msg) * PACKET_SIZE
        if stopwait:
            acknowledged = False
            while not acknowledged:
                try:
                    ACK, address = sock.recvfrom(1024)
                    acknowledged = True
                except socket.timeout:
                    print('[UDP] Failed. Resending packet.')
                    nrmsg += 1
                    nrbytes += len(msg) * PACKET_SIZE
                    sock.sendto(msg * PACKET_SIZE, (IP_ADDRESS, PORT_NO))
    elapsed_time = time.time() - start_time
    print('[UDP] Sent %s messages, %s bytes in %.02f seconds' % (nrmsg, nrbytes, elapsed_time))


def tcp(stopwait):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if stopwait:
        sock.settimeout(0.5)
    sock.connect((IP_ADDRESS, PORT_NO))
    start_time = time.time()
    try:
        nrmsg = 0
        nrbytes = 0
        for i in range(nr_chunks):
            # Send data
            sock.send(msg * PACKET_SIZE)
            nrmsg += 1
            nrbytes += len(msg * PACKET_SIZE)
            if stopwait:
                acknowledged = False
                while not acknowledged:
                    try:
                        ACK, address = sock.recvfrom(1024)
                        acknowledged = True
                    except socket.timeout:
                        print('[TCP] Failed. Resending packet.')
                        nrmsg += 1
                        nrbytes += len(msg) * PACKET_SIZE
                        sock.send(msg * PACKET_SIZE)

    finally:
        sock.close()
    elapsed_time = time.time() - start_time
    print('[TCP] Sent %s messages, %s bytes in %.02f seconds' % (nrmsg, nrbytes, elapsed_time))


# udp(False)
# udp(True)
tcp(False)
# tcp(True)
