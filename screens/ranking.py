import customtkinter as ctk
from controllers.database import BancoDeDados

COR_FUNDO_APP = "#0A0D14"       
COR_CARD = "#12151E"            
COR_BORDAS = "#222738"          
COR_TEXTO_PRINCIPAL = "#FFFFFF" 
COR_TEXTO_SECUNDARIO = "#7E849E"

# Cores do Pódio
COR_1_LUGAR = "#FFD700" # Ouro
COR_2_LUGAR = "#C0C0C0" # Prata
COR_3_LUGAR = "#CD7F32" # Bronze

class TelaRanking(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.trocar_tela_callback = trocar_tela_callback

        # --- CABEÇALHO ---
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=40, pady=(30, 10))

        ctk.CTkButton(
            frame_topo, text="←", font=("Arial", 24, "bold"), width=40, height=40,
            fg_color="transparent", hover_color=COR_CARD, command=lambda: trocar_tela_callback("menu")
        ).pack(side="left")
        
        texto_titulo = " ".join("RANKING")
        ctk.CTkLabel(frame_topo, text=texto_titulo, font=("Arial", 28, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(side="left", padx=20)
        ctk.CTkLabel(frame_topo, text="Os melhores jogadores da Batalha Matemática", font=("Arial", 14), text_color=COR_TEXTO_SECUNDARIO).pack(side="left", pady=(8,0))

        # --- ABAS DE FILTRO (Estilo Pills) ---
        self.frame_filtros = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_filtros.pack(pady=10, fill="x", padx=40)

        modos = [
            ("Geral", "🌍 Global"), 
            ("Tabuada", "✖ Tabuada"), 
            ("Frações", "◴ Frações"), 
            ("Porcentagem", "% Porcentagem"), 
            ("Regra de Três", "⚖️ Regra de Três"), 
            ("Equações", "⊞ Equações")
        ]
        self.botoes_filtro = []

        for modo_id, texto_botao in modos:
            btn = ctk.CTkButton(
                self.frame_filtros, text=texto_botao, font=("Arial", 12, "bold"),
                fg_color="transparent", text_color=COR_TEXTO_SECUNDARIO, hover_color=COR_CARD,
                border_color=COR_BORDAS, border_width=1, corner_radius=20, height=35,
                command=lambda m=modo_id: self.carregar_ranking(m)
            )
            btn.pack(side="left", padx=5)
            self.botoes_filtro.append({"id": modo_id, "widget": btn})

        # --- PÓDIO (TOP 3) ---
        self.container_podio = ctk.CTkFrame(self, fg_color="transparent", height=180)
        self.container_podio.pack(pady=20)
        
        # --- TABELA (1º LUGAR EM DIANTE) ---
        self.frame_tabela = ctk.CTkFrame(self, fg_color=COR_CARD, border_color=COR_BORDAS, border_width=1, corner_radius=15)
        self.frame_tabela.pack(padx=40, pady=(0, 20), fill="both", expand=True)
        
        # Cabeçalho da Tabela
        self.cabecalho_tabela = ctk.CTkFrame(self.frame_tabela, fg_color="transparent", height=40)
        self.cabecalho_tabela.pack(fill="x", padx=20, pady=(10, 0))
        self.cabecalho_tabela.pack_propagate(False)
        
        self.lbl_cabecalho_esq = ctk.CTkLabel(self.cabecalho_tabela, text="#        JOGADOR", font=("Arial", 11, "bold"), text_color=COR_TEXTO_SECUNDARIO)
        self.lbl_cabecalho_esq.pack(side="left", padx=15)
        
        self.lbl_cabecalho_dir = ctk.CTkLabel(self.cabecalho_tabela, text="PONTUAÇÃO", font=("Arial", 11, "bold"), text_color=COR_TEXTO_SECUNDARIO)
        self.lbl_cabecalho_dir.pack(side="right", padx=60)

        ctk.CTkFrame(self.frame_tabela, height=1, fg_color=COR_BORDAS).pack(fill="x", padx=20)

        # Lista rolável da tabela
        self.lista_ranking = ctk.CTkScrollableFrame(self.frame_tabela, fg_color="transparent")
        self.lista_ranking.pack(fill="both", expand=True, padx=10, pady=10)

    def atualizar_tela(self):
        self.carregar_ranking("Geral")

    def desenhar_lugar_podio(self, master, dados_jogador, posicao, cor, altura_bloco):
        """Cria uma coluna do pódio para o Top 3 com alinhamento na base"""
        if not dados_jogador:
            ctk.CTkFrame(master, fg_color="transparent", width=120, height=200).pack(side="left", padx=10, anchor="s")
            return

        nome = dados_jogador[0]
        pontos_ou_xp = dados_jogador[1]
        
        frame_coluna = ctk.CTkFrame(master, fg_color="transparent", width=120)
        frame_coluna.pack(side="left", padx=15, anchor="s")

        ctk.CTkLabel(frame_coluna, text=nome.upper(), font=("Arial", 14, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=(0, 2))
        ctk.CTkLabel(frame_coluna, text=f"{pontos_ou_xp}", font=("Arial", 16, "bold"), text_color=cor).pack(pady=(0, 10))

        bloco = ctk.CTkFrame(frame_coluna, fg_color="#1A1D29", border_color=cor, border_width=2, corner_radius=10, width=80, height=altura_bloco)
        bloco.pack()
        bloco.pack_propagate(False)
        ctk.CTkLabel(bloco, text=str(posicao), font=("Arial", 28, "bold"), text_color=cor).place(relx=0.5, rely=0.5, anchor="center")

    def carregar_ranking(self, modo):
        # 1. Atualiza botões (Pills)
        for btn_dict in self.botoes_filtro:
            btn = btn_dict["widget"]
            if btn_dict["id"] == modo:
                btn.configure(fg_color="#1A1D29", text_color=COR_TEXTO_PRINCIPAL, border_color="#3A415A")
            else:
                btn.configure(fg_color="transparent", text_color=COR_TEXTO_SECUNDARIO, border_color=COR_BORDAS)

        # 2. Limpa a tela
        for widget in self.container_podio.winfo_children():
            widget.destroy()
        for widget in self.lista_ranking.winfo_children():
            widget.destroy()

        # 3. Busca Dados
        if modo == "Geral":
            dados_brutos = BancoDeDados.obter_ranking_geral(limite=100)
            self.lbl_cabecalho_dir.configure(text="XP TOTAL           NÍVEL")
        else:
            dados_brutos = BancoDeDados.obter_ranking_modo(modo, limite=100)
            self.lbl_cabecalho_dir.configure(text="PONTOS           TEMPO")

        # 4. Filtro: Manter apenas a melhor pontuação de cada jogador
        dados_unicos = []
        jogadores_vistos = set()
        
        for linha in dados_brutos:
            nome = linha[0]
            if nome not in jogadores_vistos:
                jogadores_vistos.add(nome)
                dados_unicos.append(linha)

        if not dados_unicos:
            ctk.CTkLabel(self.lista_ranking, text="Nenhum jogador registrado ainda.", text_color=COR_TEXTO_SECUNDARIO).pack(pady=40)
            return

        # 5. Desenhar o Pódio
        top3 = dados_unicos[:3]
        while len(top3) < 3:
            top3.append(None) 

        self.desenhar_lugar_podio(self.container_podio, top3[1], 2, COR_2_LUGAR, 70)  
        self.desenhar_lugar_podio(self.container_podio, top3[0], 1, COR_1_LUGAR, 100) 
        self.desenhar_lugar_podio(self.container_podio, top3[2], 3, COR_3_LUGAR, 50)  

        # 6. Preencher a Tabela com TODOS os jogadores
        for i, linha in enumerate(dados_unicos):
            posicao = i + 1
            nome_jogador = linha[0]
            
            row = ctk.CTkFrame(self.lista_ranking, fg_color="transparent", height=45)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            cor_posicao = COR_TEXTO_SECUNDARIO
            if posicao == 1: cor_posicao = COR_1_LUGAR
            elif posicao == 2: cor_posicao = COR_2_LUGAR
            elif posicao == 3: cor_posicao = COR_3_LUGAR

            # Coluna Esquerda (# e Nome)
            ctk.CTkLabel(row, text=str(posicao), font=("Arial", 14, "bold"), text_color=cor_posicao, width=30).pack(side="left", padx=(10, 15))
            ctk.CTkLabel(row, text=nome_jogador.upper(), font=("Arial", 14, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(side="left")

            # Coluna Direita (Pontos e Estatísticas)
            if modo == "Geral":
                xp, nivel = linha[1], linha[2]
                ctk.CTkLabel(row, text=f"Nv. {nivel}", font=("Arial", 12), text_color=COR_TEXTO_SECUNDARIO).pack(side="right", padx=(20, 10))
                ctk.CTkLabel(row, text=f"{xp} XP", font=("Arial", 14, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(side="right", padx=10)
            else:
                pontos, _, tempo = linha[1], linha[2], linha[3]
                ctk.CTkLabel(row, text=f"⏱ {tempo}s", font=("Arial", 12), text_color=COR_TEXTO_SECUNDARIO).pack(side="right", padx=(20, 10))
                ctk.CTkLabel(row, text=f"{pontos} pts", font=("Arial", 14, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(side="right", padx=10)