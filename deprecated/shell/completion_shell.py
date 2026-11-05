import subprocess
import os, readline, sys

from .builtins_shell import get_builtins_commands
from .utils import parser, get_external_commands, log
from .config import COMPLETES


def _list_path(path: str) -> tuple[str, list[str], str]:
    """
    Extrai informações sobre um caminho de arquivo.
    
    Args:
        path: Caminho para processar
        
    Returns:
        Tupla (diretório, lista_de_arquivos, nome_procurado)
    """
    head, tail = os.path.split(path)
    if os.path.exists(head) == False:
        return ('', [], '')
    
    files = os.listdir(head)
    return head, files, tail


def completer(text: str, state: int):
    """
    Função de completar chamada pelo readline.
    
    Args:
        text: Texto a completar
        state: Estado da completação (0, 1, 2, ...)
        
    Returns:
        Próxima sugestão de completação ou None
    """
    search = text
    matches = []
    path = ''
    buffer = parser(readline.get_line_buffer())

    # tenta completar com as especificações de completação personalizadas
    if len(buffer) > 1:
        script = COMPLETES.get(buffer[0], [None, None])[1]
        if script:
            os.environ['COMP_LINE'] = ' '.join(buffer)
            os.environ['COMP_POINT'] = str(len(os.environ['COMP_LINE']))

            # para evitar que o script de completação entre em loop infinito, limita a quantidade de argumentos passados para o script de completação a 3 (o comando + os 2 últimos argumentos)
            cmd = [script] + ([buffer[0], buffer[-1], buffer[-2]] if len(buffer) > 2 else buffer[:] + [buffer[0]])
            
            stdout = subprocess.run(cmd, capture_output=True).stdout
            matches = stdout.decode('utf-8').splitlines()
        os.environ.pop('COMP_LINE', None)
        os.environ.pop('COMP_POINT', None)
    
    # se não encontrar especificações personalizadas, tenta completar com os comandos internos
    if not matches and len(buffer) == 1:
        matches = [cmd for cmd in get_builtins_commands() if cmd.startswith(text)]
    
    # se não encontrar comandos internos, tenta completar com comandos externos
    if not matches and len(buffer) == 1:
        external_commands = get_external_commands()
        matches = [cmd for cmd in external_commands if cmd.startswith(text)]
    
    # se ainda não encontrar, tenta completar com arquivos do sistema
    if not matches:
        if len(buffer) > 1:
            search = text
            if text.find('/') == -1:
                files = os.listdir()
            else:
                # resgata o último argumento da linha de comando
                path, files, search = _list_path(buffer[-1])
            
            matches = [file for file in files if file.startswith(search)] if search else files

    try:
        path_name = os.path.join(path, matches[state])
        if os.path.isdir(path_name):
            return  path_name + '/'
        return path_name + ' '
    except IndexError:
        return None


def list_commands_match(substituition, matches, longest) -> None:
    """
    Exibe sugestões de completação de forma customizada.
    
    Args:
        substitution: Texto a substituir
        matches: Lista de correspondências
        longest: Maior comprimento de correspondência
    """
    buffer = readline.get_line_buffer()
    print()
    # remove a barra (/) se houver
    basenames = list(map(lambda bn: bn[:-1] if bn[-1] == '/' else bn, matches))
    # separa o dirtório do arquivo ou último nível do diretório
    basenames = list(map(os.path.split, basenames))
    # adiciona a barra (/) se for um diretório
    basenames = list(
        map(
            lambda bn: bn[1] + '/' if os.path.isdir(os.path.join(*bn)) else bn[1],
            basenames
            )
        )
    
    # exibe as sugestões de completação
    print(' '.join(basenames), flush=True)
    sys.stdout.write('\033[K')
    sys.stdout.write(f'$ {buffer}')
    sys.stdout.flush()
    readline.redisplay()


def configure_readline() -> None:
    """Configura a biblioteca readline com as funções customizadas."""
    readline.set_completer(completer)
    readline.set_completion_display_matches_hook(list_commands_match)
    readline.set_completer_delims(' \t')
    readline.parse_and_bind('tab: complete')


__all__ = [
    'configure_readline',
    'completer',
    'list_commands_match',
]
