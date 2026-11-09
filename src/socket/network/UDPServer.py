"""
Servidor UDP Multi-usuário (Seção 2.7.1 - Programação de Sockets com UDP).

Conceitos importantes (Kurose & Ross):
1. SOCK_DGRAM: Indica que o socket utiliza o protocolo UDP (orientado a datagramas,
   sem conexão prévia / sem handshake).
2. Como não existe conexão fixa, cada pacote que chega em recvfrom(2048) traz
   junto o endereço de origem do remetente: client_address = (IP, Porta).
3. O servidor usa esse client_address como "endereço de retorno" no método
   sendto(resposta, client_address), permitindo atender múltiplos clientes UDP
   intercaladamente pelo mesmo socket!
"""

import socket

import app
import utils

# IP = socket.gethostbyname(socket.gethostname())
IP = '127.0.0.1'
PORT = 10000
BUFFER_SIZE = 2048


def iniciar_servidor(ip: str = IP, port: int = PORT) -> None:
    """Inicializa o socket UDP na porta especificada e processa datagramas de múltiplos clientes."""
    # AF_INET = IPv4 | SOCK_DGRAM = UDP
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Vincula o número de porta 10000 ao socket do servidor
    server.bind((ip, port))

    # Timeout de 1s permite capturar Ctrl+C (KeyboardInterrupt) imediatamente no Windows
    server.settimeout(1.0)

    utils.log(f'Servidor UDP Multi-usuário iniciado em {ip}:{port}', utils.INFO)
    utils.log('Pronto para receber datagramas (Pressione Ctrl+C para encerrar)...', utils.INFO)

    try:
        while True:
            try:
                # Aguarda um pacote UDP chegar (retorna os bytes e a tupla (IP, Porta) do cliente)
                data, client_address = server.recvfrom(BUFFER_SIZE)
            except TimeoutError:
                continue
            except ConnectionResetError:
                # No Windows, o UDP pode lançar ConnectionResetError (WSAECONNRESET) se um cliente
                # anterior fechou o socket abruptamente; ignoramos para manter o servidor ativo.
                continue

            mensagem = data.decode('utf-8', errors='replace').strip()
            utils.log(
                f'[UDP] Datagrama de {client_address[0]}:{client_address[1]} -> "{mensagem}"',
                utils.DEBUG,
            )

            # Se o cliente UDP enviou "exit", removemos seu registro de sessão e confirmamos saída
            if mensagem.lower() in ('exit', 'sair'):
                nome_removido = app.remover_usuario(client_address)
                despedida = 'Sessão UDP encerrada. Até logo!\n'
                server.sendto(despedida.encode('utf-8'), client_address)
                utils.log(
                    f'Cliente UDP {nome_removido or client_address} saiu '
                    f'| Usuários ativos: {app.obter_total_usuarios()}',
                    utils.INFO,
                )
                continue

            # Processa o comando na camada de aplicação (substituindo o modelo .upper() do livro)
            resposta = app.processar_comando(mensagem, client_address, protocolo='UDP')

            # Anexa o endereço de destino do cliente (client_address) e envia o datagrama de resposta
            server.sendto(resposta.encode('utf-8'), client_address)

    except KeyboardInterrupt:
        utils.log('Servidor UDP interrompido pelo usuário (^C).', utils.ERROR)
    finally:
        server.close()
        utils.log('Socket do servidor UDP fechado.', utils.INFO)


if __name__ == '__main__':
    iniciar_servidor()
