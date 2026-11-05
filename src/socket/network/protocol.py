import struct


def send(sock, data: bytes) -> None:
    """
    Envia o cabeçalho de 4 bytes (tamanho da mensagem) seguido dos bytes de dados.
    """
    header = struct.pack('!I', len(data))
    sock.sendall(header + data)


def _receive_exact(sock, n: int) -> bytes | None:
    """
    Função auxiliar que garante a leitura exata de 'n' bytes do socket TCP.
    Retorna None caso a outra ponta tenha fechado a conexão (recv retorna b'').
    """
    data = []
    recv_total = 0

    while recv_total < n:
        value = sock.recv(n - recv_total)
        if value == b'':
            return None

        recv_total += len(value)
        data.append(value)

    return b''.join(data)


def receive(sock) -> bytes | None:
    """
    Recebe uma mensagem completa do socket TCP lendo primeiro o cabeçalho
    de 4 bytes e, em seguida, o corpo completo da mensagem.
    """
    header = _receive_exact(sock, 4)
    if header is None:
        return None
    tamanho_mensagem = struct.unpack('!I', header)[0]
    return _receive_exact(sock, tamanho_mensagem)


__all__ = ['send', 'receive']
