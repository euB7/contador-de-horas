import os
import time
import logging
from datetime import datetime

# Diretórios Base
BASE_DIR = r"C:\Contador"
LOGS_DIR = os.path.join(BASE_DIR, "Logs")
ARQUIVOS_DIR = os.path.join(BASE_DIR, "Arquivos")

def inicializar_estrutura():
    """Garante a existência das pastas C:\Contador\Logs e C:\Contador\Arquivos."""
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(ARQUIVOS_DIR, exist_ok=True)
    except Exception as e:
        print(f"Erro ao criar estrutura de diretórios: {e}")

# Inicializa pastas e configura logs
inicializar_estrutura()

log_filename = os.path.join(LOGS_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logging.info("==========================================")
logging.info("Aplicação inicializada.")

class GerenciadorContador:
    def __init__(self):
        self.tempo_inicio = None
        self.tempo_decorrido_acumulado = 0
        self.rodando = False

    def iniciar_cronometro(self):
        if not self.rodando:
            self.tempo_inicio = time.time() - self.tempo_decorrido_acumulado
            self.rodando = True
            logging.info("Cronômetro iniciado.")

    def pausar_cronometro(self):
        if self.rodando:
            self.rodando = False
            logging.info("Cronômetro pausado.")

    def resetar(self):
        """Zera o estado do cronômetro para um novo apontamento."""
        self.tempo_inicio = None
        self.tempo_decorrido_acumulado = 0
        self.rodando = False
        logging.info("Cronômetro resetado.")

    def obter_tempo_formatado(self):
        if self.rodando:
            self.tempo_decorrido_acumulado = int(time.time() - self.tempo_inicio)
        
        horas, resto = divmod(self.tempo_decorrido_acumulado, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def salvar_relatorio(self, titulo, atividades):
        """
        Recebe o título e uma lista de tuplas (marcado: bool, texto: str)
        e gera o arquivo .txt em C:\Contador\Arquivos
        """
        try:
            logging.info("Iniciando processo de salvamento de relatório...")
            inicializar_estrutura()

            data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            tempo_total = self.obter_tempo_formatado()

            linhas = [
                f"==================== {titulo or 'Apontamento de Horas'} ====================",
                f"Data/Hora do Registro: {data_hora_atual}",
                f"Tempo Total Decorrido: {tempo_total}",
                "--------------------------------------------------",
                "Atividades Realizadas:"
            ]

            atividades_validas = 0
            for concluido, texto in atividades:
                texto_limpo = texto.strip()
                if texto_limpo:
                    atividades_validas += 1
                    status = "[X]" if concluido else "[ ]"
                    linhas.append(f"  {status} {texto_limpo}")

            if atividades_validas == 0:
                linhas.append("  (Nenhuma atividade descrita)")

            linhas.append("==================================================")

            timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"Apontamento_{timestamp_file}.txt"
            caminho_final = os.path.join(ARQUIVOS_DIR, nome_arquivo)

            with open(caminho_final, "w", encoding="utf-8") as f:
                f.write("\n".join(linhas))

            logging.info(f"Relatório gerado com sucesso em: {caminho_final}")
            return caminho_final

        except Exception as e:
            logging.error(f"Erro grave ao salvar relatório: {e}", exc_info=True)
            raise e