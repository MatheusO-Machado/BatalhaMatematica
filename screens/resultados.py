import customtkinter as ctk
import random

# Paleta Dark UI Premium
COR_FUNDO_APP = "#0A0D14"       
COR_CARD = "#12151E"            
COR_BORDAS = "#222738"          
COR_TEXTO_PRINCIPAL = "#FFFFFF" 
COR_TEXTO_SECUNDARIO = "#7E849E"
COR_ROXO = "#8A2BE2"
COR_VERMELHO = "#D90429"
COR_VERDE = "#38B000"
COR_AMARELO = "#FFBE0B"
COR_AZUL = "#00BFFF"

class BotaoAcaoAnimado(ctk.CTkFrame):
    def __init__(self, master, texto, cor_base, cor_texto, cor_borda, command, is_primary=False):
        super().__init__(master, fg_color="transparent", width=240, height=75)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.command = command
        self.cor_base = cor_base
        self.cor_borda = cor_borda

        self.btn = ctk.CTkButton(
            self, text=texto.upper(), font=("Arial", 15, "bold"),
            fg_color=cor_base, hover_color=cor_borda if not is_primary else "#2A145C", 
            text_color=cor_texto, border_color=cor_borda, border_width=2,
            corner_radius=12, width=200, height=50, command=self.command
        )
        self.btn.place(relx=0.5, rely=0.5, anchor="center")

        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.btn.configure(width=215, height=58, border_width=3)

    def on_leave(self, e):
        self.btn.configure(width=200, height=50, border_width=2)


class TelaResultados(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.trocar_tela_callback = trocar_tela_callback

        self.criar_fundo_decorativo()

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

    def criar_fundo_decorativo(self):
        elementos = ["7", "3", "9", "2", "4", "1", "+", "-", "x", "∑", "θ", "√n", "∞", "∫"]
        for _ in range(25): 
            texto = random.choice(elementos)
            tamanho = random.randint(20, 70)
            
            pos_x = random.uniform(0.05, 0.95)
            pos_y = random.uniform(0.05, 0.95)
            if 0.3 < pos_x < 0.7 and 0.2 < pos_y < 0.8:
                continue 

            lbl = ctk.CTkLabel(self, text=texto, font=("Arial", tamanho, "bold"), text_color="#141824")
            lbl.place(relx=pos_x, rely=pos_y, anchor="center")

    def mostrar_resultados(self, pontos, acertos, erros, tempo, max_combo):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        total_questoes = acertos + erros
        taxa_acerto = (acertos / total_questoes * 100) if total_questoes > 0 else 0

        # --- NOVA LÓGICA DE RANKING (EMOJIS) ---
        if taxa_acerto >= 90 and acertos > 5:
            rank, cor_rank, titulo = "👑", COR_AMARELO, "LENDÁRIO!"
        elif taxa_acerto >= 70 and acertos > 2:
            rank, cor_rank, titulo = "🌟", COR_ROXO, "EXCELENTE!"
        elif taxa_acerto >= 50:
            rank, cor_rank, titulo = "🔥", COR_AZUL, "MUITO BOM!"
        else:
            rank, cor_rank, titulo = "📚", COR_TEXTO_SECUNDARIO, "PRECISA PRATICAR..."

        ctk.CTkLabel(self.main_container, text="FIM DE JOGO", font=("Arial", 16, "bold"), text_color=COR_TEXTO_SECUNDARIO).pack(pady=(0, 10))
        
        card = ctk.CTkFrame(self.main_container, fg_color=COR_CARD, border_color=cor_rank, border_width=2, corner_radius=20, width=500)
        card.pack(pady=10)
        
        # Selo do Rank (Aumentei o tamanho do frame e da fonte para o emoji brilhar)
        selo_bg = ctk.CTkFrame(card, fg_color="#1A1D29", corner_radius=35, width=70, height=70)
        selo_bg.pack(pady=(20, 5))
        selo_bg.pack_propagate(False)
        ctk.CTkLabel(selo_bg, text=rank, font=("Arial", 38), text_color=cor_rank).place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(card, text=titulo, font=("Arial", 14, "bold"), text_color=cor_rank).pack(pady=(0, 15))

        ctk.CTkLabel(card, text="PONTUAÇÃO TOTAL", font=("Arial", 12), text_color=COR_TEXTO_SECUNDARIO).pack()
        ctk.CTkLabel(card, text=f"{pontos}", font=("Arial", 64, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=(0, 20))

        ctk.CTkFrame(card, height=1, fg_color=COR_BORDAS).pack(fill="x", padx=40, pady=(0, 20))

        grid_stats = ctk.CTkFrame(card, fg_color="transparent")
        grid_stats.pack(fill="x", padx=30, pady=(0, 30))
        
        self.criar_mini_stat(grid_stats, "🎯", f"{acertos}", "Acertos", COR_VERDE, 0, 0)
        self.criar_mini_stat(grid_stats, "❌", f"{erros}", "Erros", COR_VERMELHO, 0, 1)
        self.criar_mini_stat(grid_stats, "⏱️", f"{tempo}s", "Tempo", COR_AZUL, 1, 0)
        self.criar_mini_stat(grid_stats, "⚡", f"{max_combo}x", "Max Combo", COR_AMARELO, 1, 1)

        frame_botoes = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame_botoes.pack(pady=20)

        BotaoAcaoAnimado(
            frame_botoes, texto="Jogar Novamente", 
            cor_base=COR_ROXO, cor_texto=COR_TEXTO_PRINCIPAL, cor_borda=COR_ROXO, 
            command=lambda: self.trocar_tela_callback("selecao_modo"), is_primary=True
        ).pack(side="left", padx=10)

        BotaoAcaoAnimado(
            frame_botoes, texto="Menu Principal", 
            cor_base="transparent", cor_texto=COR_TEXTO_SECUNDARIO, cor_borda=COR_BORDAS, 
            command=lambda: self.trocar_tela_callback("menu")
        ).pack(side="left", padx=10)

    def criar_mini_stat(self, master, icone, valor, titulo, cor_icone, linha, coluna):
        frame = ctk.CTkFrame(master, fg_color="#0A0D14", border_color=COR_BORDAS, border_width=1, corner_radius=12, width=190, height=70)
        frame.grid(row=linha, column=coluna, padx=10, pady=10)
        frame.pack_propagate(False)
        
        ctk.CTkLabel(frame, text=icone, font=("Arial", 24), text_color=cor_icone).pack(side="left", padx=20)
        
        info = ctk.CTkFrame(frame, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=12)
        ctk.CTkLabel(info, text=f"{valor}", font=("Arial", 18, "bold"), text_color=COR_TEXTO_PRINCIPAL, anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=titulo, font=("Arial", 11), text_color=COR_TEXTO_SECUNDARIO, anchor="w").pack(fill="x")