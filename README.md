# Socket Multi-usuário (TCP e UDP) em Python

Aplicação cliente-servidor em **TCP** e **UDP** usando `socket`, com suporte a **múltiplos usuários simultâneos**, **mural de mensagens compartilhado** e **análise/inversão de texto** (diferente do exemplo básico `.upper()` do livro *Redes de Computadores e a Internet* — Kurose & Ross).

---

## 📂 Arquivos do Projeto (`src/socket/network/`)

* **[`app.py`](src/socket/network/app.py)**: Lógica da aplicação (guarda os `usuarios` online, o `mural` de mensagens e analisa as frases com `if / elif / else` simples).
* **[`protocol.py`](src/socket/network/protocol.py)**: Protocolo de envio/recebimento do TCP (envia 4 bytes com o tamanho da mensagem antes dos dados).
* **[`TCPServer.py`](src/socket/network/TCPServer.py)**: Servidor TCP multi-usuário (cria uma `Thread` para cada cliente conectado).
* **[`TCPClient.py`](src/socket/network/TCPClient.py)**: Cliente TCP interativo.
* **[`UDPServer.py`](src/socket/network/UDPServer.py)**: Servidor UDP multi-usuário.
* **[`UDPClient.py`](src/socket/network/UDPClient.py)**: Cliente UDP interativo.
* **[`utils.py`](src/socket/network/utils.py)**: Logs coloridos no terminal do servidor.
* **[`main.py`](src/socket/network/main.py)**: Menu rápido para iniciar servidor ou cliente.

---

## 🚀 Como Rodar

Abra 2 ou 3 terminais na pasta `src/socket/network`:
```powershell
cd src/socket/network
```

### Modo TCP:
1. **Terminal 1 (Servidor)**: `python TCPServer.py`
2. **Terminal 2 (Cliente 1)**: `python TCPClient.py`
3. **Terminal 3 (Cliente 2)**: `python TCPClient.py`

### Modo UDP:
1. **Terminal 1 (Servidor)**: `python UDPServer.py`
2. **Terminal 2 (Cliente 1)**: `python UDPClient.py`

---

## 💬 O que digitar no Cliente?

* `ajuda` — Mostra os comandos disponíveis.
* `nome <apelido>` — Muda seu nome no servidor (ex: `nome Davi`).
* `usuarios` — Lista todos os usuários conectados no momento.
* `msg <recado>` — Publica uma mensagem no mural compartilhado (ex: `msg Olá pessoal!`).
* `mural` — Lê todas as mensagens deixadas no mural pelos usuários.
* **Qualquer outra frase** — O servidor inverte a frase e conta quantas palavras, caracteres e vogais ela tem!
* `exit` — Sai do programa.
