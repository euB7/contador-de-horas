import sys
import logging
import tkinter as tk
from tkinter import ttk, messagebox

# Importa a lógica do arquivo logica.py
from logica import GerenciadorContador, LOGS_DIR

class InterfaceContador:
    def __init__(self, root):
        self.root = root
        self.root.title("Contador de Horas")
        self.root.geometry("550x650")
        self.root.minsize(450, 500)

        # Instância da Lógica
        self.gerenciador = GerenciadorContador()
        self.itens_atividades = []
        self.modo_compacto = False
        self.modo_escuro = False  # Estado do tema

        self.setup_styles()
        self.setup_ui()
        self.aplicar_tema()
        
        # Intercepta o clique no botão X da janela para tratar o fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar_janela)

    def setup_styles(self):
        """Configura os estilos base do TTK."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def setup_ui(self):
        # ---------------------------------------------------------
        # Frame Principal (Tela Completa)
        # ---------------------------------------------------------
        self.frame_completo = ttk.Frame(self.root)
        self.frame_completo.pack(fill="both", expand=True)

        # Barra Superior / Header com Botões de Modo Mini e Tema
        frame_top_bar = ttk.Frame(self.frame_completo, padding=(10, 10, 10, 0))
        frame_top_bar.pack(fill="x")

        self.lbl_titulo_header = ttk.Label(frame_top_bar, text="Título do Chamado / Apontamento:", font=("Segoe UI", 10, "bold"))
        self.lbl_titulo_header.pack(side="left")
        
        frame_botoes_top = ttk.Frame(frame_top_bar)
        frame_botoes_top.pack(side="right")

        self.btn_tema = ttk.Button(frame_botoes_top, text="🌙 Escuro", width=9, command=self.alternar_tema)
        self.btn_tema.pack(side="left", padx=(0, 5))

        self.btn_mini = ttk.Button(frame_botoes_top, text="🗖 Mini", width=8, command=self.alternar_modo_compacto)
        self.btn_mini.pack(side="left")

        self.entry_titulo = tk.Entry(self.frame_completo, font=("Segoe UI", 10), relief="solid", bd=1)
        self.entry_titulo.pack(fill="x", padx=10, pady=(5, 10))

        # Seção do Timer (Tela Completa)
        self.frame_timer = ttk.Frame(self.frame_completo, padding=10)
        self.frame_timer.pack(fill="x")

        self.label_timer = ttk.Label(self.frame_timer, text="00:00:00", font=("Segoe UI", 32, "bold"))
        self.label_timer.pack()

        frame_botoes = ttk.Frame(self.frame_timer)
        frame_botoes.pack(pady=5)

        self.btn_iniciar = tk.Button(
            frame_botoes, text=" ▶ Iniciar", font=("Segoe UI", 10, "bold"),
            bg="#2e7d32", fg="white", activebackground="#1b5e20", activeforeground="white",
            relief="flat", padx=12, pady=5, command=self.iniciar
        )
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_pausar = tk.Button(
            frame_botoes, text=" ❚❚ Pausar", font=("Segoe UI", 10, "bold"),
            bg="#d32f2f", fg="white", activebackground="#b71c1c", activeforeground="white",
            relief="flat", padx=12, pady=5, state="disabled", command=self.pausar
        )
        self.btn_pausar.pack(side="left", padx=5)

        # Área de Scroll de Atividades
        frame_label = ttk.Frame(self.frame_completo, padding=(10, 10, 10, 0))
        frame_label.pack(fill="x")
        self.lbl_atividades_header = ttk.Label(frame_label, text="Atividades (Pressione ENTER para adicionar a próxima):", font=("Segoe UI", 10, "bold"))
        self.lbl_atividades_header.pack(anchor="w")

        canvas_container = ttk.Frame(self.frame_completo, padding=10)
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', self._redimensionar_canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Adiciona a primeira linha de atividade
        self.adicionar_campo_atividade()

        # Rodapé - Botão Salvar
        frame_footer = ttk.Frame(self.frame_completo, padding=10)
        frame_footer.pack(fill="x")

        self.btn_salvar = ttk.Button(frame_footer, text="Salvar", command=self.salvar_e_resetar)
        self.btn_salvar.pack(fill="x", ipady=5)

        # ---------------------------------------------------------
        # Frame do Modo Compacto (Mini Widget)
        # ---------------------------------------------------------
        self.frame_mini = ttk.Frame(self.root, padding=10)

        self.label_timer_mini = ttk.Label(self.frame_mini, text="00:00:00", font=("Segoe UI", 22, "bold"))
        self.label_timer_mini.pack(pady=(0, 2))

        frame_botoes_mini = ttk.Frame(self.frame_mini)
        frame_botoes_mini.pack(pady=2)

        self.btn_iniciar_mini = tk.Button(
            frame_botoes_mini, text=" ▶", font=("Segoe UI", 9, "bold"),
            bg="#2e7d32", fg="white", activebackground="#1b5e20", activeforeground="white",
            relief="flat", padx=8, pady=3, command=self.iniciar
        )
        self.btn_iniciar_mini.pack(side="left", padx=3)

        self.btn_pausar_mini = tk.Button(
            frame_botoes_mini, text=" ❚❚", font=("Segoe UI", 9, "bold"),
            bg="#d32f2f", fg="white", activebackground="#b71c1c", activeforeground="white",
            relief="flat", padx=8, pady=3, state="disabled", command=self.pausar
        )
        self.btn_pausar_mini.pack(side="left", padx=3)

        self.btn_expandir = ttk.Button(self.frame_mini, text="🗖 Expandir", command=self.alternar_modo_compacto)
        self.btn_expandir.pack(pady=(5, 0))

    def _redimensionar_canvas(self, event):
        """Ajusta a largura do frame interno para ocupar 100% da área útil do canvas."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def alternar_tema(self):
        """Alterna entre Modo Claro e Modo Escuro."""
        self.modo_escuro = not self.modo_escuro
        self.btn_tema.config(text="🌙" if self.modo_escuro else "☀️")
        self.aplicar_tema()

    def aplicar_tema(self):
        """Aplica as cores do tema ativo a todos os componentes da interface."""
        if self.modo_escuro:
            bg_main = "#1e1e1e"
            bg_card = "#252526"
            fg_text = "#ffffff"
            entry_bg = "#3c3c3c"
            entry_fg = "#ffffff"
            entry_border = "#555555"
        else:
            bg_main = "#f3f3f3"
            bg_card = "#ffffff"
            fg_text = "#000000"
            entry_bg = "#ffffff"
            entry_fg = "#000000"
            entry_border = "#cccccc"

        # Janela e Canvas
        self.root.configure(bg=bg_main)
        self.canvas.configure(bg=bg_main)

        # Estilos TTK
        self.style.configure("TFrame", background=bg_main)
        self.style.configure("TLabel", background=bg_main, foreground=fg_text)
        self.style.configure("TCheckbutton", background=bg_main, foreground=fg_text)
        self.style.configure("TButton", font=("Segoe UI", 9))

        # Entradas Nativas Tkinter
        self.entry_titulo.configure(
            bg=entry_bg, fg=entry_fg, insertbackground=fg_text,
            highlightbackground=entry_border, highlightcolor=entry_border
        )

        for item in self.itens_atividades:
            item['entry'].configure(
                bg=entry_bg, fg=entry_fg, insertbackground=fg_text,
                highlightbackground=entry_border, highlightcolor=entry_border
            )

    def alternar_modo_compacto(self):
        """Alterna entre a janela completa e o mini widget compacto."""
        if not self.modo_compacto:
            self.modo_compacto = True
            self.frame_completo.pack_forget()

            self.root.minsize(180, 130)
            self.root.geometry("220x140")
            self.root.resizable(False, False)
            self.root.wm_attributes("-topmost", True)

            self.frame_mini.pack(fill="both", expand=True)
        else:
            self.modo_compacto = False
            self.frame_mini.pack_forget()

            self.root.minsize(450, 500)
            self.root.geometry("550x650")
            self.root.resizable(True, True)
            self.root.wm_attributes("-topmost", False)

            self.frame_completo.pack(fill="both", expand=True)

    def iniciar(self):
        self.gerenciador.iniciar_cronometro()
        
        self.btn_iniciar.config(state="disabled", bg="#81c784")
        self.btn_pausar.config(state="normal", bg="#d32f2f")
        
        self.btn_iniciar_mini.config(state="disabled", bg="#81c784")
        self.btn_pausar_mini.config(state="normal", bg="#d32f2f")
        
        self.atualizar_interface_timer()

    def pausar(self):
        self.gerenciador.pausar_cronometro()
        
        self.btn_iniciar.config(state="normal", bg="#2e7d32")
        self.btn_pausar.config(state="disabled", bg="#e57373")
        
        self.btn_iniciar_mini.config(state="normal", bg="#2e7d32")
        self.btn_pausar_mini.config(state="disabled", bg="#e57373")

    def atualizar_interface_timer(self):
        if self.gerenciador.rodando:
            tempo_str = self.gerenciador.obter_tempo_formatado()
            self.label_timer.config(text=tempo_str)
            self.label_timer_mini.config(text=tempo_str)
            self.root.after(1000, self.atualizar_interface_timer)

    def adicionar_campo_atividade(self, event=None):
        row_frame = ttk.Frame(self.scrollable_frame)
        row_frame.pack(fill="x", expand=True, pady=3)

        var_check = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(row_frame, variable=var_check)
        chk.pack(side="left", padx=(0, 5))

        # Aplica cores baseadas no tema ativo
        if self.modo_escuro:
            entry_bg, entry_fg, entry_border = "#3c3c3c", "#ffffff", "#555555"
        else:
            entry_bg, entry_fg, entry_border = "#ffffff", "#000000", "#cccccc"

        entry = tk.Entry(
            row_frame, font=("Segoe UI", 10), bg=entry_bg, fg=entry_fg,
            insertbackground=entry_fg, relief="solid", bd=1,
            highlightbackground=entry_border, highlightcolor=entry_border
        )
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", self.adicionar_campo_atividade)

        self.itens_atividades.append({'var': var_check, 'entry': entry, 'frame': row_frame})

        entry.focus_set()
        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def tem_dados_pendentes(self):
        if self.gerenciador.rodando or self.gerenciador.tempo_decorrido_acumulado > 0:
            return True
        if self.entry_titulo.get().strip():
            return True
        for item in self.itens_atividades:
            if item['entry'].get().strip():
                return True
        return False

    def salvar_e_resetar(self):
        try:
            titulo = self.entry_titulo.get()
            atividades = [(item['var'].get(), item['entry'].get()) for item in self.itens_atividades]

            caminho_arquivo = self.gerenciador.salvar_relatorio(titulo, atividades)

            messagebox.showinfo("Sucesso", f"Apontamento salvo com sucesso!\n\nArquivo: {caminho_arquivo}")
            self.resetar_interface()

        except Exception as e:
            messagebox.showerror(
                "Erro ao Salvar",
                f"Ocorreu um erro ao salvar o arquivo:\n{e}\n\nDetalhes registrados em {LOGS_DIR}."
            )

    def resetar_interface(self):
        self.gerenciador.resetar()
        
        self.label_timer.config(text="00:00:00")
        self.label_timer_mini.config(text="00:00:00")
        
        self.btn_iniciar.config(state="normal", bg="#2e7d32")
        self.btn_pausar.config(state="disabled", bg="#e57373")
        
        self.btn_iniciar_mini.config(state="normal", bg="#2e7d32")
        self.btn_pausar_mini.config(state="disabled", bg="#e57373")

        self.entry_titulo.delete(0, tk.END)

        for item in self.itens_atividades:
            item['frame'].destroy()
        self.itens_atividades.clear()

        self.adicionar_campo_atividade()

    def ao_fechar_janela(self):
        if self.tem_dados_pendentes():
            resposta = messagebox.askyesno(
                "Confirmar Saída",
                "Você realmente quer sair? Os dados não salvos serão perdidos.",
                icon='warning'
            )
            if not resposta:
                return

        logging.info("Aplicação encerrada pelo usuário.")
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = InterfaceContador(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Erro não tratado: {e}", exc_info=True)