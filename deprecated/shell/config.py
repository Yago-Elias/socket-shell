import os
from itertools import filterfalse

# ============= COMANDOS BUILT-IN =============
BUILTINS_COMMANDS = set()

# ============= CAMINHOS DO SISTEMA =============
SYSTEM_PATHS = list(
    filterfalse(lambda p: '/mnt' in p or '/home' in p, os.get_exec_path())
)

# ============= VARIÁVEIS GLOBAIS =============
# Cache dos comandos externos (lazy loading)
_external_commands = None

# ============= CONSTANTES DE REDIRECIONAMENTO =============
STDIN = 0
STDOUT = 1
STDERR = 2
PIPE = 3
JOB = 4

# ============= VARIÁVEIS DO HISTÓRICO =============
HISTFILE = os.getenv('HISTFILE')
HISTORY_LENGTH_MAX = 1000
HIST_SIZE_LAST_ADD = 0

# ============= VARIÁVEIS DO COMANDO COMPLETE =============
COMPLETES = dict()

# ============= VARIÁVEIS DO SHELL =============
VARIABLES = dict()

# ============= FUNÇÕES AUXILIARES =============
# def get_external_commands() -> set[str]:
#     """
#     Obtém o conjunto de comandos externos disponíveis no PATH.
    
#     Usa cache para evitar rescans do filesystem.
    
#     Returns:
#         Set com nomes dos comandos externos encontrados
#     """
#     global _external_commands

#     if _external_commands is None:
#         from .utils import get_commands_in_path
#         _external_commands = {
#             cmd for p in SYSTEM_PATHS
#             for cmd in get_commands_in_path(p)
#         }
    
#     return _external_commands


# def get_completions() -> dict[str, list[str]]:
#     with open(COMPLETE_PATH_FILE, 'r') as f:
#         for line in f:
#             if line.strip():
#                 cmd, *comps = line.strip().split(':')
#                 COMPLETES[cmd] = comps
    
#     return COMPLETES


__all__ = [
    'BUILTINS_COMMANDS',
    'SYSTEM_PATHS',
    'STDIN',
    'STDOUT',
    'STDERR',
    'PIPE',
    'HISTORY_LENGTH_MAX',
    'HISTFILE',
    'HIST_SIZE_LAST_ADD',
    'COMPLETES',
    'VARIABLES',
]