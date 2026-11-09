"""
Servidor TCP Multi-usuário (Seção 2.7.2 - Programação de Sockets com TCP).

Conceitos importantes (Kurose & Ross):
1. SOCK_STREAM: Indica que estamos criando um socket TCP (orientado à conexão,
   fluxo confiável e ordenado de bytes).
2. Dois tipos de sockets no Servidor TCP (Figura 2.29 do livro):
   - skt_server (serverSocket): O "socket de entrada" (porta de boas-vindas),
     que fica fixo na porta 10000 aguardando novos clientes baterem à porta.
   - skt_client (connectionSocket): Criado pelo método accept() especificamente
     para cada cliente que completa o handshake de 3 vias.
3. Multiplicidade de Usuários (Threading):
   - Para atender vários clientes simultaneamente sem que um bloqueie o outro,
     cada connectionSocket aceito no accept() é delegado para uma Thread própria.
"""

import socket
from threading import Thread

import app
import protocol
import utils

# Endereço IP e Porta onde o servidor ficará escutando conexões
# '127.0.0.1' permite conexões locais; '' ou '0.0.0.0' aceita conexões da rede local
IP = '127.0.0.1'
PORT = 10000


def atender_cliente(skt_client: socket.socket, client_address: tuple[str, int]) -> None:
    """
    Função executada em uma Thread exclusiva para cada cliente conectado.
    Gerencia todo o ciclo de vida da comunicação com aquele usuário.
    """
    apelido = app.registrar_usuario(client_address, protocolo='TCP')
    total_online = app.obter_total_usuarios()
    utils.log(
        f'Novo cliente conectado: {apelido} ({client_address[0]}:{client_address[1]}) '
        f'| Usuários ativos: {total_online}',
        utils.INFO,
    )

    try:
        while True:
            # Recebe a mensagem completa usando o protocolo de cabeçalho de 4 bytes
            dados = protocol.receive(skt_client)
            if dados is None:
                utils.log(
                    f'Cliente {client_address[0]}:{client_address[1]} fechou a conexão.',
                    utils.WARNING,
                )
                break

            mensagem = dados.decode('utf-8', errors='replace').strip()
            utils.log(
                f'[TCP] Comando de {client_address[0]}:{client_address[1]}: "{mensagem}"',
                utils.DEBUG,
            )

            # Verifica se o cliente solicitou encerramento da sessão
            if mensagem.lower() in ('exit', 'sair'):
                protocol.send(skt_client, 'Sessão encerrada pelo servidor. Até logo!\n'.encode('utf-8'))
                break

            # Processa o comando na camada de aplicação (diferente do modelo .upper() do livro)
            resposta = app.processar_comando(mensagem, client_address, protocolo='TCP')
            protocol.send(skt_client, resposta.encode('utf-8'))

    except (ConnectionResetError, BrokenPipeError, OSError):
        utils.log(
            f'Conexão interrompida abruptamente com {client_address[0]}:{client_address[1]}.',
            utils.ERROR,
        )
    finally:
        # Remove o cliente da lista de usuários ativos e fecha o socket dedicado (connectionSocket)
        nome_removido = app.remover_usuario(client_address)
        skt_client.close()
        utils.log(
            f'Sessão finalizada para {nome_removido or client_address} '
            f'| Usuários restantes: {app.obter_total_usuarios()}',
            utils.INFO,
        )


def iniciar_servidor(ip: str = IP, port: int = PORT) -> None:
    """Inicializa o socket de boas-vindas do servidor TCP e aguarda múltiplos clientes."""
    # AF_INET = IPv4 | SOCK_STREAM = TCP
    skt_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar a porta imediatamente após reiniciar o servidor
    skt_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincula o endereço IP e número de porta ao socket de entrada do servidor
    skt_server.bind((ip, port))

    # Coloca o socket em modo de escuta para conexões de múltiplos clientes
    skt_server.listen()

    # Timeout de 1s no accept() permite capturar Ctrl+C (KeyboardInterrupt) no Windows
    skt_server.settimeout(1.0)

    utils.log(f'Servidor TCP Multi-usuário iniciado em {ip}:{port}', utils.INFO)
    utils.log('Aguardando conexões de clientes (Pressione Ctrl+C para encerrar)...', utils.INFO)

    try:
        while True:
            try:
                # Aguarda um cliente iniciar o Three-Way Handshake
                skt_client, client_address = skt_server.accept()
                # Garante que o socket dedicado ao cliente opere em modo bloqueante normal
                skt_client.settimeout(None)
            except TimeoutError:
                continue

            # Cria e inicia uma Thread dedicada para atender este cliente simultaneamente
            thread_cliente = Thread(
                target=atender_cliente,
                args=(skt_client, client_address),
                daemon=True,
            )
            thread_cliente.start()

    except KeyboardInterrupt:
        utils.log('Servidor TCP interrompido pelo usuário (^C).', utils.ERROR)
    finally:
        skt_server.close()
        utils.log('Socket do servidor TCP fechado.', utils.INFO)


if __name__ == '__main__':
    iniciar_servidor()
