import customtkinter as ctk
from controllers.database import BancoDeDados

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

class TelaPerfil(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.trocar_tela_callback = trocar_tela_callback

        self.frame_esq = ctk.CTkFrame(self, fg_color=COR_CARD, border_color=COR_BORDAS, border_width=1, corner_radius=15, width=320)
        self.frame_esq.pack(side="left", fill="y", padx=20, pady=20)
        self.frame_esq.pack_propagate(False)

        self.scroll_dir = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_dir.pack(side="left", fill="both", expand=True, pady=20, padx=(0, 20))

    def atualizar_tela(self):
        for widget in self.frame_esq.winfo_children():
            widget.destroy()
        for widget in self.scroll_dir.winfo_children():
            widget.destroy()

        usuario_id = self.master.usuario_logado_id
        
        if not usuario_id:
            self.montar_perfil_convidado()
            return

        dados = BancoDeDados.obter_dados_perfil(usuario_id)
        stats = BancoDeDados.obter_estatisticas_conquistas(usuario_id)
        historico = BancoDeDados.obter_historico_recente(usuario_id, 4)

        username, xp_total, _ = dados
        
        xp_por_nivel = 200
        nivel_atual = (xp_total // xp_por_nivel) + 1
        xp_atual_no_nivel = xp_total % xp_por_nivel
        progresso_xp = xp_atual_no_nivel / xp_por_nivel

        self.montar_coluna_esquerda(username, nivel_atual, xp_total, progresso_xp, stats)
        self.montar_coluna_direita(stats, historico)

    def montar_coluna_esquerda(self, username, nivel, xp_total, progresso_xp, stats):
        ctk.CTkButton(
            self.frame_esq, text="← Voltar ao Menu", font=("Arial", 12, "bold"), text_color=COR_TEXTO_SECUNDARIO,
            fg_color="transparent", hover_color="#1A1D29", anchor="w", command=lambda: self.trocar_tela_callback("menu")
        ).pack(fill="x", padx=20, pady=(20, 10))

        # Avatar Dinâmico
        inicial = username[0].upper() if username else "?"
        
        container_avatar = ctk.CTkFrame(self.frame_esq, fg_color="transparent")
        container_avatar.pack(pady=(15, 10))
        
        avatar_bg = ctk.CTkFrame(container_avatar, fg_color=COR_ROXO, width=85, height=85, corner_radius=50)
        avatar_bg.pack()
        avatar_bg.pack_propagate(False)
        ctk.CTkLabel(avatar_bg, text=inicial, font=("Arial", 38, "bold"), text_color=COR_TEXTO_PRINCIPAL).place(relx=0.5, rely=0.5, anchor="center")

        # Textos de Identidade Limpos
        ctk.CTkLabel(self.frame_esq, text=f"NÍVEL {nivel}", font=("Arial", 11, "bold"), text_color=COR_AMARELO).pack()
        ctk.CTkLabel(self.frame_esq, text=username.upper(), font=("Arial", 22, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=(2, 20))

        # Barra de XP
        frame_xp = ctk.CTkFrame(self.frame_esq, fg_color="transparent")
        frame_xp.pack(fill="x", padx=30, pady=(0, 10))
        
        ctk.CTkLabel(frame_xp, text="XP", font=("Arial", 10, "bold"), text_color=COR_TEXTO_SECUNDARIO).pack(side="left")
        ctk.CTkLabel(frame_xp, text=f"{xp_total} / {((xp_total // 200) + 1) * 200}", font=("Arial", 10, "bold"), text_color=COR_TEXTO_SECUNDARIO).pack(side="right")
        
        barra_xp = ctk.CTkProgressBar(self.frame_esq, height=8, fg_color=COR_BORDAS, progress_color=COR_ROXO)
        barra_xp.pack(fill="x", padx=30)
        barra_xp.set(progresso_xp)

        # Grid de Estatísticas (Caixas Ajustadas)
        grid_stats = ctk.CTkFrame(self.frame_esq, fg_color="transparent")
        grid_stats.pack(fill="x", padx=15, pady=30)
        
        self.criar_mini_stat(grid_stats, "🏆", stats["total_partidas"], "Partidas", 0, 0)
        self.criar_mini_stat(grid_stats, "⭐", stats["maior_pontuacao"], "Maior Pont.", 0, 1)
        self.criar_mini_stat(grid_stats, "⊞", stats["partidas_equacoes"], "Equações", 1, 0)
        self.criar_mini_stat(grid_stats, "🔥", "Ativo", "Status", 1, 1)

        # Botão Sair
        self.btn_sair = ctk.CTkButton(
            self.frame_esq, text="Sair da Conta", font=("Arial", 14, "bold"), text_color=COR_VERMELHO,
            fg_color="transparent", border_color=COR_VERMELHO, border_width=1, hover_color="#2A0808", height=45,
            command=self.fazer_logout
        )
        self.btn_sair.pack(side="bottom", fill="x", padx=30, pady=30)

    def criar_mini_stat(self, master, icone, valor, titulo, linha, coluna):
        # Aumentei a largura para 135 e a altura para 95 para evitar cortes
        frame = ctk.CTkFrame(master, fg_color="#0A0D14", border_color=COR_BORDAS, border_width=1, corner_radius=10, width=135, height=95)
        frame.grid(row=linha, column=coluna, padx=7, pady=7)
        frame.pack_propagate(False)
        
        # O ícone agora tem a cor roxa do tema para dar contraste
        ctk.CTkLabel(frame, text=icone, font=("Arial", 22), text_color=COR_ROXO).pack(pady=(12, 2))
        ctk.CTkLabel(frame, text=f"{valor}", font=("Arial", 16, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=0)
        ctk.CTkLabel(frame, text=titulo, font=("Arial", 10), text_color=COR_TEXTO_SECUNDARIO).pack()

    def montar_coluna_direita(self, stats, historico):
        ctk.CTkLabel(self.scroll_dir, text="Conquistas", font=("Arial", 18, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(0, 10))
        
        frame_conquistas = ctk.CTkFrame(self.scroll_dir, fg_color="transparent")
        frame_conquistas.pack(fill="x", pady=(0, 30))

        lista_conquistas = [
            {"titulo": "Pioneiro", "desc": "1ª partida", "cond": stats["total_partidas"] >= 1, "icone": "🌱"},
            {"titulo": "Veterano", "desc": "10 partidas", "cond": stats["total_partidas"] >= 10, "icone": "⚔️"},
            {"titulo": "Mestre", "desc": "+150 pts", "cond": stats["maior_pontuacao"] >= 150, "icone": "👑"},
            {"titulo": "X-Hunter", "desc": "5 Equações", "cond": stats["partidas_equacoes"] >= 5, "icone": "⊞"}
        ]

        for i, conq in enumerate(lista_conquistas):
            self.criar_card_conquista(frame_conquistas, conq, linha=i//2, coluna=i%2)

        ctk.CTkLabel(self.scroll_dir, text="Partidas Recentes", font=("Arial", 18, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(anchor="w", pady=(0, 10))
        
        if not historico:
            ctk.CTkLabel(self.scroll_dir, text="Nenhuma partida jogada ainda.", text_color=COR_TEXTO_SECUNDARIO).pack(anchor="w", pady=10)
            return

        for partida in historico:
            modo, pontos, acertos, tempo = partida
            taxa_acerto = int((acertos / 10) * 100) 
            
            row = ctk.CTkFrame(self.scroll_dir, fg_color=COR_CARD, border_color=COR_BORDAS, border_width=1, corner_radius=10, height=60)
            row.pack(fill="x", pady=5)
            row.pack_propagate(False)
            
            icone = "🎮"
            if modo == "Tabuada": icone = "✖"
            elif modo == "Frações": icone = "◴"
            elif modo == "Porcentagem": icone = "↗"
            elif modo == "Equações": icone = "⊞"
            
            ctk.CTkLabel(row, text=icone, font=("Arial", 20), text_color=COR_ROXO).pack(side="left", padx=20)
            
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left")
            ctk.CTkLabel(info, text=modo, font=("Arial", 14, "bold"), text_color=COR_TEXTO_PRINCIPAL, anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"⏱ {tempo}s", font=("Arial", 11), text_color=COR_TEXTO_SECUNDARIO, anchor="w").pack(fill="x")

            stats_box = ctk.CTkFrame(row, fg_color="transparent")
            stats_box.pack(side="right", padx=20)
            ctk.CTkLabel(stats_box, text=f"{pontos} pts", font=("Arial", 14, "bold"), text_color=COR_TEXTO_PRINCIPAL, anchor="e").pack(fill="x")
            ctk.CTkLabel(stats_box, text=f"Precisão: {taxa_acerto}%", font=("Arial", 11), text_color=COR_VERDE if taxa_acerto >= 70 else COR_AMARELO, anchor="e").pack(fill="x")

    def criar_card_conquista(self, master, dados, linha, coluna):
        ativo = dados["cond"]
        cor_fundo = COR_CARD if ativo else "#0D0F15"
        cor_borda = COR_ROXO if ativo else COR_BORDAS
        cor_texto = COR_TEXTO_PRINCIPAL if ativo else COR_TEXTO_SECUNDARIO
        
        card = ctk.CTkFrame(master, fg_color=cor_fundo, border_color=cor_borda, border_width=1, corner_radius=10, width=280, height=70)
        card.grid(row=linha, column=coluna, padx=10, pady=10)
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text=dados["icone"], font=("Arial", 24), text_color=COR_AMARELO if ativo else COR_TEXTO_SECUNDARIO).pack(side="left", padx=15)
        
        textos = ctk.CTkFrame(card, fg_color="transparent")
        textos.pack(side="left", fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(textos, text=dados["titulo"], font=("Arial", 13, "bold"), text_color=cor_texto, anchor="w").pack(fill="x")
        ctk.CTkLabel(textos, text=dados["desc"], font=("Arial", 11), text_color=COR_TEXTO_SECUNDARIO, anchor="w").pack(fill="x")

    def fazer_logout(self):
        self.master.usuario_logado_id = None
        self.master.usuario_logado_nome = None
        self.trocar_tela_callback("login")

    def montar_perfil_convidado(self):
        ctk.CTkButton(
            self.frame_esq, text="← Voltar ao Menu", font=("Arial", 12, "bold"), text_color=COR_TEXTO_SECUNDARIO,
            fg_color="transparent", hover_color="#1A1D29", anchor="w", command=lambda: self.trocar_tela_callback("menu")
        ).pack(fill="x", padx=20, pady=(20, 10))

        container_avatar = ctk.CTkFrame(self.frame_esq, fg_color="transparent")
        container_avatar.pack(pady=(20, 10))
        avatar_bg = ctk.CTkFrame(container_avatar, fg_color="#1A1D29", width=85, height=85, corner_radius=50)
        avatar_bg.pack()
        avatar_bg.pack_propagate(False)
        ctk.CTkLabel(avatar_bg, text="👻", font=("Arial", 38)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.frame_esq, text="CONVIDADO", font=("Arial", 22, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=(10, 0))
        ctk.CTkLabel(self.frame_esq, text="Modo Offline", font=("Arial", 12), text_color=COR_TEXTO_SECUNDARIO).pack()

        ctk.CTkLabel(self.scroll_dir, text="Modo Convidado Ativo", font=("Arial", 24, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=(100, 10))
        ctk.CTkLabel(self.scroll_dir, text="Crie uma conta para registrar seu progresso,\nsubir de nível e desbloquear conquistas!", font=("Arial", 14), text_color=COR_TEXTO_SECUNDARIO).pack()

        self.btn_sair = ctk.CTkButton(
            self.frame_esq, text="Sair / Criar Conta", font=("Arial", 14, "bold"), text_color=COR_VERMELHO,
            fg_color="transparent", border_color=COR_VERMELHO, border_width=1, hover_color="#2A0808", height=45,
            command=self.fazer_logout
        )
        self.btn_sair.pack(side="bottom", fill="x", padx=30, pady=30)