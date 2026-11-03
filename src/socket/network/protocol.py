"""
Estabelece um simples protocolo para a troca de dados entre o servidor e cliente TCP/IP
"""
import struct

# Envia o cabeçalho + dados
# Cabeçalho de tamanho fixo de 4 bytes informando o tamanho de dados
# Dados são bytes de informação a ser enviado
def send(sock, data: bytes):
    header = struct.pack('!I', len(data))
    sock.sendall(header + data)

def _receive_exact(sock, n):
    data = []
    recv_total = 0

    while recv_total < n:
        value = sock.recv(n - recv_total)
        if value == b'': return None

        recv_total += len(value)
        data.append(value)

    return b''.join(data)

def receive(sock):
    header = _receive_exact(sock, 4)
    if header is None: return None
    header = struct.unpack('!I', header)[0]
    return _receive_exact(sock, header)

__all__ = ['send', 'receive']
