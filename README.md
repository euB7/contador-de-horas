#  Contador de Horas & Apontamento de Atividades

Aplicação desktop desenvolvida em Python para gerenciamento de tempo, cronometragem de chamados e registro dinâmico de atividades com suporte a exportação automática de relatórios.

---

##  Funcionalidades

- **Cronômetro Integrado:** Início, pausa e atualização do tempo decorrido em tempo real.
- ** Inclusão Dinâmica de Atividades:** Adição rápida de novas tarefas com *checkbox* apenas pressionando a tecla `ENTER`.
- ** Modo Mini (Widget):** Janela compacta e fixa no topo da tela (`topmost`), ideal para acompanhar o tempo enquanto trabalha em outras tarefas.
- ** Temas Claro e Escuro:** Alternância de tema visual (`☀️ Claro` / `🌙 Escuro`) com um clique.
- ** Gerenciamento de Diretórios:** Criação e validação automática da estrutura de pastas na máquina local (`C:\Contador\Logs` e `C:\Contador\Arquivos`).
- ** Exportação de Relatórios:** Geração automática de arquivos `.txt` formatados com data, hora, tempo total e status das atividades ao salvar.
- ** Logs de Auditoria:** Registro de inicialização, salvamento e diagnósticos de erros em arquivo de log diário.

---

## Arquitetura do Projeto

O projeto utiliza o padrão de separação de responsabilidades para facilitar a manutenção e evolução do código:

- `layout.py`: Camada de Interface Gráfica (GUI) construída com **Tkinter**.
- `logica.py`: Camada de Regras de Negócio, manipulador de arquivos, timers e gerenciador de logs.

---

## Pré-requisitos

- **Python 3.10+** instalado na máquina.
- Módulos nativos do Python (Tkinter, Logging, OS, Time, Sys).

---

##  Como Executar o Projeto

1. Clone o repositório ou baixe os arquivos fonte:
   ```bash
   git clone [https://github.com/SEU_USUARIO/contador-de-horas.git](https://github.com/SEU_USUARIO/contador-de-horas.git)


Acesse a pasta do projeto:

Bash
cd contador-de-horas
Execute a aplicação a partir do arquivo de interface:

Bash
python layout.py
📦 Como Gerar o Executável (.exe)
Para compilar a aplicação em um único arquivo executável para Windows (sem necessidade do Python na máquina de destino):

Instale o PyInstaller:

Bash
pip install pyinstaller
Compile o projeto a partir do layout.py:

Bash
python -m PyInstaller --onefile --noconsole layout.py
O executável final será gerado dentro da pasta dist/.

Estrutura de Arquivos Gerada no Sistema (C:\Contador)
Após a execução, a aplicação gerencia automaticamente o seguinte diretório:

Plaintext
C:\Contador\
├── Arquivos\
│   └── Apontamento_YYYYMMDD_HHMMSS.txt
└── Logs\
    └── app_YYYYMMDD.log

