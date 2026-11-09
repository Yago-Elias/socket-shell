"""
Cliente TCP (Seção 2.7.2 - Programação de Sockets com TCP).

Conceitos importantes (Kurose & Ross):
1. O cliente cria um socket TCP com socket(AF_INET, SOCK_STREAM).
   Não precisamos escolher uma porta para o cliente manualmente: o próprio
   Sistema Operacional designa uma porta livre automaticamente.
2. Antes de enviar dados, o cliente chama connect((IP, PORT)), que realiza a
   apresentação de três vias (Three-Way Handshake) com o servidor.
3. Com a conexão estabelecida, os dados fluem pelo canal confiável usando nosso
   protocolo de cabeçalho de 4 bytes (protocol.send e protocol.receive).
"""

import socket
import protocol

IP = '127.0.0.1'
PORT = 10000


def iniciar_cliente(ip: str = IP, port: int = PORT) -> None:
    """Conecta ao servidor TCP e inicia o loop interativo de envio de comandos."""
    # Cria o socket TCP (IPv4, orientado à conexão)
    skt_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Inicia o Three-Way Handshake e estabelece a conexão com o servidor
        skt_client.connect((ip, port))
    except ConnectionRefusedError:
        print(f'Não foi possível conectar ao servidor TCP em {ip}:{port}. Verifique se o TCPServer está rodando.')
        return

    print(f'Conectado ao servidor TCP em {ip}:{port}!')
    print('Digite "ajuda" para ver os comandos disponíveis ou "exit" para sair.\n')

    try:
        while True:
            try:
                comando = input(f'[TCP] {ip}:{port} $ ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\nEncerrando cliente TCP...')
                break

            if not comando:
                continue

            # Envia o comando codificado em bytes usando o protocolo de aplicação
            protocol.send(skt_client, comando.encode('utf-8'))

            # Aguarda a resposta processada pelo servidor
            resposta = protocol.receive(skt_client)

            if resposta is None:
                print('Servidor encerrou a conexão.')
                break

            print(resposta.decode('utf-8', errors='replace'), end='')

            if comando.lower() in ('exit', 'sair'):
                break
    finally:
        # Fecha o socket e encerra a conexão TCP com o servidor
        skt_client.close()


if __name__ == '__main__':
    iniciar_cliente()
