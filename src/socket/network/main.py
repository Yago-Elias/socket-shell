"""
Ponto de entrada unificado para iniciar Servidor ou Cliente (TCP ou UDP).

Você pode executar cada arquivo individualmente em terminais separados:
  - python TCPServer.py
  - python TCPClient.py
  - python UDPServer.py
  - python UDPClient.py

Ou executar este menu interativo:
  - python main.py
"""

import time
from threading import Thread

import TCPClient
import TCPServer
import UDPClient
import UDPServer


def run() -> None:
    print('==================================================')
    print('   APLICAÇÃO DE SOCKETS MULTI-USUÁRIO (TCP/UDP)   ')
    print('==================================================')
    print('  1 - Iniciar Servidor TCP (Multi-usuário)')
    print('  2 - Iniciar Cliente TCP')
    print('  3 - Iniciar Servidor UDP (Multi-usuário)')
    print('  4 - Iniciar Cliente UDP')
    print('  5 - Modo Rápido: Servidor + Cliente TCP juntos')
    print('  6 - Modo Rápido: Servidor + Cliente UDP juntos')
    print('  0 - Sair')
    print('==================================================')

    try:
        opcao = input('Escolha uma opção: ').strip()
    except (EOFError, KeyboardInterrupt):
        print('\nSaindo...')
        return

    match opcao:
        case '1':
            TCPServer.iniciar_servidor()
        case '2':
            TCPClient.iniciar_cliente()
        case '3':
            UDPServer.iniciar_servidor()
        case '4':
            UDPClient.iniciar_cliente()
        case '5':
            t = Thread(target=TCPServer.iniciar_servidor, daemon=True)
            t.start()
            time.sleep(0.3)
            TCPClient.iniciar_cliente()
        case '6':
            t = Thread(target=UDPServer.iniciar_servidor, daemon=True)
            t.start()
            time.sleep(0.3)
            UDPClient.iniciar_cliente()
        case '0':
            print('Até logo!')
        case _:
            print('Opção inválida.')


if __name__ == '__main__':
    run()
