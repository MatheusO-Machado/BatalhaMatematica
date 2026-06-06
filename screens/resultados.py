import customtkinter as ctk

COR_ROXO = "#7B2CBF"
COR_FUNDO = "#0B0C10" 
COR_VERDE = "#38B000"
COR_AMARELO = "#FFBE0B"
COR_AZUL = "#3A86FF"
COR_BRANCO = "#F8F9FA"

class TelaResultados(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback
        
        # Container centralizado para evitar bugs de resolução
        self.container_central = ctk.CTkFrame(self, fg_color="transparent")
        self.container_central.place(relx=0.5, rely=0.5, anchor="center")

    def configurar_resultados(self, dados_partida):
        """Recebe o dicionário com os dados do jogo e constrói a tela"""
        # Limpa resultados anteriores, se houver
        for widget in self.container_central.winfo_children():
            widget.destroy()

        modo = dados_partida["modo"]
        acertos = dados_partida["acertos"]
        max_perguntas = dados_partida["max_perguntas"]
        tempo = dados_partida["tempo"]
        pontos = dados_partida["pontos"]
        
        desempenho_pct = int((acertos / max_perguntas) * 100)
        
        # Sistema de "Tier/Medalha"
        if desempenho_pct == 100:
            medalha = "💎 DIAMANTE"
            cor_destaque = "#00FFFF" 
            frase = "Absoluto! Um verdadeiro gênio da matemática! ✨"
        elif desempenho_pct >= 70:
            medalha = "🥇 OURO"
            cor_destaque = "#FFD700" 
            frase = "Incrível! Seu raciocínio está afiadíssimo! 🚀"
        elif desempenho_pct >= 40:
            medalha = "🥈 PRATA"
            cor_destaque = "#C0C0C0" 
            frase = "Muito bom! Mas você pode ir ainda mais longe! 💪"
        else:
            medalha = "🥉 BRONZE"
            cor_destaque = "#CD7F32" 
            frase = "A prática leva à perfeição. Tente novamente! 🎯"
            
        # Painel central da vitória (tamanho fixo para não bugar)
        painel = ctk.CTkFrame(self.container_central, fg_color="#12131C", border_color=cor_destaque, border_width=2, corner_radius=25, width=700, height=500)
        painel.pack()
        painel.pack_propagate(False) # Impede que o painel amasse os textos
        
        # Truque de espaçamento com o .join()
        texto_modo_espacado = " ".join(f"RESULTADO: {modo.upper()}")
        ctk.CTkLabel(painel, text=texto_modo_espacado, font=("Arial", 16, "bold"), text_color="#A0A0A0").pack(pady=(35, 0))
        ctk.CTkLabel(painel, text=medalha, font=("Arial", 54, "bold"), text_color=cor_destaque).pack(pady=(0, 5))
        ctk.CTkLabel(painel, text=frase, font=("Arial", 18), text_color=COR_BRANCO).pack(pady=(0, 30))
        
        # Container de estatísticas
        frame_cards = ctk.CTkFrame(painel, fg_color="transparent")
        frame_cards.pack(padx=50, pady=10)
        
        self.criar_card_stat(frame_cards, "Acertos", f"{acertos}/{max_perguntas}", COR_VERDE, 0)
        self.criar_card_stat(frame_cards, "Precisão", f"{desempenho_pct}%", COR_AZUL, 1)
        self.criar_card_stat(frame_cards, "Tempo", f"{tempo}s", COR_ROXO, 2)
        self.criar_card_stat(frame_cards, "Pontos", f"{pontos}", COR_AMARELO, 3)

        barra_precisao = ctk.CTkProgressBar(painel, width=500, height=12, fg_color="#1A1C29", progress_color=cor_destaque)
        barra_precisao.pack(pady=30)
        barra_precisao.set(desempenho_pct / 100)

        # Botões de Saída
        frame_botoes = ctk.CTkFrame(painel, fg_color="transparent")
        frame_botoes.pack(pady=(0, 20))

        ctk.CTkButton(
            frame_botoes, text="↻ Jogar Novamente", fg_color=cor_destaque, text_color="#12131C",
            font=("Arial", 16, "bold"), width=220, height=50, corner_radius=12, hover_color=COR_BRANCO,
            command=lambda: self.jogar_novamente(modo)
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            frame_botoes, text="≡ Escolher Modo", fg_color="transparent", text_color=COR_BRANCO,
            border_color="#2A2D3E", border_width=2, font=("Arial", 16, "bold"), width=220, height=50, corner_radius=12, hover_color="#1A1C29",
            command=lambda: self.trocar_tela_callback("selecao_modo")
        ).pack(side="left", padx=15)

    def criar_card_stat(self, master, titulo, valor, cor, coluna):
        card = ctk.CTkFrame(master, fg_color="#1A1F2E", corner_radius=15, width=120, height=110)
        card.grid(row=0, column=coluna, padx=10)
        card.pack_propagate(False) 
        
        ctk.CTkLabel(card, text=valor, font=("Arial", 26, "bold"), text_color=cor).pack(pady=(25, 5))
        ctk.CTkLabel(card, text=titulo, font=("Arial", 13), text_color="#A0A0A0").pack()

    def jogar_novamente(self, modo):
        tela_jogo = self.master.telas["jogo"]
        tela_jogo.configurar_modo(modo)
        self.trocar_tela_callback("jogo")