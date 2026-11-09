"""
Lógica da Aplicação Multi-usuário (Mural de Mensagens + Analisador de Frases).
Substitui o exemplo básico .upper() do livro por uma aplicação interativa entre vários clientes.
"""

# Guarda os usuários conectados: chave = (ip, porta), valor = nome do usuário
usuarios = {}

# Guarda as mensagens enviadas no mural compartilhado
mural = []


def registrar_usuario(endereco, protocolo='TCP'):
    if endereco not in usuarios:
        usuarios[endereco] = f'Usuario_{endereco[1]}'
    return usuarios[endereco]


def remover_usuario(endereco):
    return usuarios.pop(endereco, None)


def obter_total_usuarios():
    return len(usuarios)


# --- Funções de cada comando ---

def cmd_ajuda(endereco, argumento):
    return (
        '--- COMANDOS DISPONÍVEIS ---\n'
        '  nome <apelido>   -> Muda seu nome (ex: nome Davi)\n'
        '  usuarios         -> Mostra quem está conectado agora\n'
        '  msg <recado>     -> Posta uma mensagem no mural para todos\n'
        '  mural            -> Lê todas as mensagens do mural\n'
        '  <qualquer frase> -> Inverte a frase e conta palavras, letras e vogais\n'
        '  exit             -> Sai do programa\n'
    )


def cmd_nome(endereco, argumento):
    if not argumento:
        return 'Digite um nome! Exemplo: nome Davi\n'
    usuarios[endereco] = argumento
    return f'Seu nome foi alterado para: {argumento}\n'


def cmd_usuarios(endereco, argumento):
    linhas = [f'--- USUÁRIOS CONECTADOS ({len(usuarios)}) ---']
    for end, nome in usuarios.items():
        linhas.append(f'  * {nome} ({end[0]}:{end[1]})')
    return '\n'.join(linhas) + '\n'


def cmd_msg(endereco, argumento):
    if not argumento:
        return 'Digite uma mensagem! Exemplo: msg Olá pessoal!\n'
    mural.append(f'{usuarios[endereco]}: {argumento}')
    return f'Mensagem postada no mural! (Total: {len(mural)})\n'


def cmd_mural(endereco, argumento):
    if not mural:
        return 'O mural está vazio. Use "msg <texto>" para escrever algo!\n'
    return '--- MURAL DE MENSAGENS ---\n' + '\n'.join(mural) + '\n'


def analisar_frase(frase: str) -> str:
    invertida = frase[::-1]
    palavras = len(frase.split())
    letras = len(frase)
    vogais = sum(1 for c in frase.lower() if c in 'aeiouáéíóúãõâêô')
    return f'Invertido: "{invertida}" | Palavras: {palavras} | Caracteres: {letras} | Vogais: {vogais}\n'


# Dicionário que mapeia o nome do comando direto para sua função (sem precisar de vários elif)
COMANDOS = {
    'ajuda': cmd_ajuda,
    'nome': cmd_nome,
    'usuarios': cmd_usuarios,
    'msg': cmd_msg,
    'mural': cmd_mural,
}


def processar_comando(mensagem: str, endereco, protocolo='TCP') -> str:
    registrar_usuario(endereco, protocolo)

    partes = mensagem.strip().split(' ', 1)
    comando = partes[0].lower()
    argumento = partes[1] if len(partes) > 1 else ''

    # Busca a função no dicionário COMANDOS; se não for um comando fixo, analisa a frase
    funcao = COMANDOS.get(comando)
    if funcao:
        return funcao(endereco, argumento)

    return analisar_frase(mensagem.strip())
