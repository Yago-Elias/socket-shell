"""
Utilitários de formatação de logs no terminal para os servidores TCP e UDP.
"""

ERROR = 1
DEBUG = 2
WARNING = 3
INFO = 4

COL_ERROR = '\033[0;31m [ ERROR ] \033[m'
COL_DEBUG = '\033[32m [ DEBUG ] \033[m '
COL_WARNING = '\033[0;33m [ WARNING ] \033[m '
COL_INFO = '\033[0;34m [ INFO ] \033[m'

PREFIXOS_LOG = {
    ERROR: COL_ERROR,
    DEBUG: COL_DEBUG,
    WARNING: COL_WARNING,
    INFO: COL_INFO,
}


def log(message_log: str, level: int = INFO) -> None:
    """Exibe mensagens de log coloridas no console do servidor."""
    prefixo = PREFIXOS_LOG.get(level, COL_INFO)
    print(f'{prefixo}{message_log}')


__all__ = [
    'log',
    'ERROR',
    'DEBUG',
    'WARNING',
    'INFO',
    'COL_ERROR',
    'COL_DEBUG',
    'COL_WARNING',
    'COL_INFO',
]
