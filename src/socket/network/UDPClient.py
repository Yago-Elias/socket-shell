"""
Cliente UDP (Seção 2.7.1 - Programação de Sockets com UDP).

Conceitos importantes (Kurose & Ross):
1. O cliente cria um socket UDP com socket(AF_INET, SOCK_DGRAM).
2. Diferente do TCP, NÃO chamamos connect(). Não há apresentação de três vias.
3. A cada envio, usamos sendto(dados, (IP, PORT)), anexando explicitamente o
   endereço de destino (IP do servidor e porta 10000) ao pacote.
4. Em seguida, aguardamos o datagrama de resposta do servidor com recvfrom(2048).
"""

import socket

# IP = socket.gethostbyname(socket.gethostname())
IP = '127.0.0.1'
PORT = 10000
BUFFER_SIZE = 2048


def iniciar_cliente(ip: str = IP, port: int = PORT) -> None:
    """Inicia o cliente UDP para envio contínuo de datagramas ao servidor."""
    # Cria o socket UDP (IPv4, datagramas sem conexão)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define um timeout de 5 segundos para caso o servidor UDP não esteja rodando
    client.settimeout(5.0)

    print(f'Cliente UDP pronto para enviar pacotes para {ip}:{port}!')
    print('Digite "ajuda" para ver os comandos disponíveis ou "exit" para sair.\n')

    try:
        while True:
            try:
                comando = input(f'[UDP] {ip}:{port} $ ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nEncerrando cliente UDP...')
                break

            if not comando:
                continue

            try:
                # Anexa o endereço (ip, port) ao datagrama e envia pelo socket UDP
                client.sendto(comando.encode('utf-8'), (ip, port))

                # Aguarda o datagrama de resposta vindo do servidor
                resposta, _server_address = client.recvfrom(BUFFER_SIZE)
                print(resposta.decode('utf-8', errors='replace'), end='')
            except TimeoutError:
                print(f'Tempo esgotado: Sem resposta do servidor UDP em {ip}:{port}. Verifique se o UDPServer está ativo.')
            except ConnectionResetError:
                print(f'Não foi possível alcançar o servidor UDP em {ip}:{port}. Verifique se o UDPServer está rodando.')

            if comando.lower() in ('exit', 'sair'):
                break
    finally:
        # Fecha o socket UDP do cliente
        client.close()


if __name__ == '__main__':
    iniciar_cliente()
