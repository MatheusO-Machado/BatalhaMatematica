import customtkinter as ctk
from utils.database import BancoDeDados

# Paleta de Cores
COR_FUNDO = "#0B0C10"
COR_ROXO = "#8A2BE2"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#A0A0A0"
COR_OURO = "#FFD700"
COR_PRATA = "#C0C0C0"
COR_BRONZE = "#CD7F32"

class TelaRanking(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback

        # --- CABEÇALHO ---
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=40, pady=(30, 20))

        ctk.CTkButton(
            frame_topo, text="←", font=("Arial", 24, "bold"), width=40, height=40,
            fg_color="transparent", hover_color="#1E1E2E", command=lambda: trocar_tela_callback("menu")
        ).pack(side="left")
        
        texto_titulo = " ".join("HALL DA FAMA")
        ctk.CTkLabel(frame_topo, text=texto_titulo, font=("Arial", 28, "bold"), text_color=COR_BRANCO).pack(side="left", padx=20)

        # --- ABAS DE FILTRO ---
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=10)

        modos = ["Geral", "Tabuada", "Frações", "Porcentagem", "Regra de Três", "Equações"]
        self.botoes_filtro = []

        for modo in modos:
            btn = ctk.CTkButton(
                self.frame_filtros, text=modo, font=("Arial", 14, "bold"),
                fg_color="transparent", text_color=COR_CINZA, hover_color="#1A1F2E",
                border_color="#2A2D3E", border_width=1, corner_radius=20,
                command=lambda m=modo: self.carregar_ranking(m)
            )
            btn.pack(side="left", padx=5)
            self.botoes_filtro.append(btn)

        # --- CABEÇALHO DA TABELA ---
        self.frame_cabecalho = ctk.CTkFrame(self, fg_color="#12131C", corner_radius=10, height=40)
        self.frame_cabecalho.pack(fill="x", padx=60, pady=(10, 0))
        self.frame_cabecalho.pack_propagate(False)

        self.lbl_cabecalho = ctk.CTkLabel(self.frame_cabecalho, text="", font=("Arial", 12, "bold"), text_color=COR_ROXO)
        self.lbl_cabecalho.pack(side="left", padx=30, pady=10)

        # --- LISTA ROLÁVEL ---
        self.lista_ranking = ctk.CTkScrollableFrame(self, fg_color="transparent", width=800, height=350)
        self.lista_ranking.pack(padx=40, pady=10, fill="both", expand=True)

    def atualizar_tela(self):
        """Método chamado sempre que a tela é aberta para forçar o recarregamento dos dados mais recentes."""
        self.carregar_ranking("Geral")

    def carregar_ranking(self, modo):
        # 1. Destaca visualmente a aba selecionada
        for btn in self.botoes_filtro:
            if btn.cget("text") == modo:
                btn.configure(fg_color=COR_ROXO, text_color=COR_BRANCO, border_width=0)
            else:
                btn.configure(fg_color="transparent", text_color=COR_CINZA, border_width=1)

        # 2. Limpa o ranking anterior da tela
        for widget in self.lista_ranking.winfo_children():
            widget.destroy()

        # 3. Busca os dados no Banco de Dados e ajusta o cabeçalho
        if modo == "Geral":
            dados = BancoDeDados.obter_ranking_geral(limite=50)
            self.lbl_cabecalho.configure(text="POSIÇÃO        JOGADOR                                                                            XP TOTAL          NÍVEL")
        else:
            dados = BancoDeDados.obter_ranking_modo(modo, limite=50)
            self.lbl_cabecalho.configure(text="POSIÇÃO        JOGADOR                                                                            PONTOS            TEMPO")

        # 4. Verifica se o banco está vazio
        if not dados:
            ctk.CTkLabel(self.lista_ranking, text="Nenhuma partida registrada ainda.", font=("Arial", 16), text_color=COR_CINZA).pack(pady=50)
            return

        # 5. Desenha as linhas do Ranking
        for i, linha in enumerate(dados):
            posicao = i + 1
            cor_fundo = "#1A1C29" if i % 2 == 0 else "transparent" # Efeito zebrado (claro/escuro)
            cor_texto = COR_BRANCO

            # Medalhas
            icone = f"{posicao}º"
            if posicao == 1:
                icone = "👑 1º"
                cor_texto = COR_OURO
            elif posicao == 2:
                icone = "🥈 2º"
                cor_texto = COR_PRATA
            elif posicao == 3:
                icone = "🥉 3º"
                cor_texto = COR_BRONZE

            row = ctk.CTkFrame(self.lista_ranking, fg_color=cor_fundo, height=50, corner_radius=8)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            # Coluna 1: Posição
            ctk.CTkLabel(row, text=icone, font=("Arial", 16, "bold"), text_color=cor_texto, width=80, anchor="w").pack(side="left", padx=(20, 10))

            # Coluna 2: Nome do Jogador
            nome_jogador = linha[0]
            ctk.CTkLabel(row, text=nome_jogador.upper(), font=("Arial", 16, "bold"), text_color=cor_texto, width=350, anchor="w").pack(side="left")

            # Colunas 3 e 4 dependem do modo
            if modo == "Geral":
                xp, nivel = linha[1], linha[2]
                ctk.CTkLabel(row, text=f"{xp} XP", font=("Arial", 16, "bold"), text_color=COR_BRANCO, width=100, anchor="e").pack(side="left", padx=20)
                ctk.CTkLabel(row, text=f"Nv. {nivel}", font=("Arial", 14, "bold"), text_color=COR_ROXO).pack(side="left")
            else:
                pontos, _, tempo = linha[1], linha[2], linha[3]
                ctk.CTkLabel(row, text=f"{pontos} pts", font=("Arial", 16, "bold"), text_color=COR_BRANCO, width=100, anchor="e").pack(side="left", padx=20)
                ctk.CTkLabel(row, text=f"⏱ {tempo}s", font=("Arial", 14), text_color=COR_CINZA).pack(side="left")