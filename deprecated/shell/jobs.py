"""
Implementação do comando jobs.
"""

from subprocess import Popen
from collections import namedtuple

from .builtins_shell import InputShell, OutputShell
from .utils import log

Process = namedtuple('Process', ['job_number', 'pid', 'command', 'status', 'proccess'], defaults=[0, 0, '', 'Running', None])

JOBS_NUMBER = 0 # Contador de jobs em execução
process: dict[int, Process] = {} # Dicionário de processos em execução, chave é o PID


def run_bg_job(input: InputShell) -> OutputShell:
    """Executa um comando em background."""

    command = [input.command] + input.args
    proc = Popen(command)

    if proc.stderr:
        return OutputShell(stderr=proc.stderr.read())
    global JOBS_NUMBER
    JOBS_NUMBER += 1
    process[proc.pid] = Process(JOBS_NUMBER, proc.pid, ' '.join(command), proccess=proc)

    return OutputShell(bytes(f'[{JOBS_NUMBER}] {proc.pid}', encoding='utf-8'))


def _check_job(pid: int) -> str:
    recent = ' '
    proc = process[pid]
    if proc.job_number == process[max(process)].job_number:
        recent = '+'
    elif len(process) > 1 and proc.job_number == list(process.values())[-2].job_number:
        recent = '-'
    
    return f'[{proc.job_number}]{recent}  {proc.status:<24}{proc.command}\n'


def jobs(input: InputShell | None) -> OutputShell:
    """Lista os jobs em execução."""

    list_remove_pid = []
    for p in [proc for proc in process.values()]:
        if p.status == 'Done':
            list_remove_pid.append(p.pid)
            continue
        process[p.pid] = p._replace(status='Done' if p.proccess.poll() is not None else 'Running')

    global JOBS_NUMBER
    for pid in list_remove_pid:
        JOBS_NUMBER -= 1
        del process[pid]
    
    list_jobs = []
    list_process = list(process.values())
    for proc in list_process:
        list_jobs.append(_check_job(proc.pid))

    return OutputShell(bytes(''.join(list_jobs), encoding='utf-8'))


def check_bg_jobs() -> OutputShell:
    """Verifica o status dos jobs em background e exibe mensagens de conclusão."""

    list_remove_pid = []
    list_jobs = []
    for p in [proc for proc in process.values()]:
        if p.status == 'Running' and p.proccess.poll() is not None:
            process[p.pid] = p._replace(status='Done')
            list_remove_pid.append(p.pid)
            list_jobs.append(_check_job(p.pid))
    
    global JOBS_NUMBER
    for pid in list_remove_pid:
        JOBS_NUMBER -= 1
        del process[pid]

    return OutputShell(bytes(''.join(list_jobs), encoding='utf-8'))


__all__ = ['jobs', 'run_bg_job', 'check_bg_jobs']