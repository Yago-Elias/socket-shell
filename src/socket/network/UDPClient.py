import socket

# obtêm o ip atual do computador
IP = socket.gethostbyname(socket.gethostname())
PORT = 10000

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = input('mensagem >>  ')

while True:
    message, server_address = client.recvfrom(2048)
    if message.decode() == '': break

    print(message.decode())

client.close()
