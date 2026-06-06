import customtkinter as ctk

class CardModo(ctk.CTkFrame):
    def __init__(self, master, titulo, desc, cor, icone, dificuldade, cor_dif, comando):
        # 1. Tamanho FIXO absoluto. O cartão não vai encolher nem esticar.
        super().__init__(master, fg_color="#12131C", border_color="#1A1C29", border_width=2, corner_radius=15, width=240, height=250)
        
        # 2. A TRAVA MÁGICA: Impede que os textos de dentro deformem o cartão de fora
        self.pack_propagate(False) 
        
        # Efeitos visuais de Hover e Clique
        self.bind("<Enter>", lambda e: self.configure(border_color=cor, cursor="hand2"))
        self.bind("<Leave>", lambda e: self.configure(border_color="#1A1C29"))
        self.bind("<Button-1>", lambda e: comando())
        
        # Selo de dificuldade usando 'place' (coordenada absoluta) para não bagunçar o alinhamento do resto
        selo = ctk.CTkLabel(self, text=dificuldade, font=("Arial", 11, "bold"), text_color="white", fg_color=cor_dif, corner_radius=8, width=60, height=26)
        selo.place(x=165, y=15) 
        
        # Ícone centralizado
        lbl_icone = ctk.CTkLabel(self, text=icone, font=("Arial", 50), text_color=cor)
        lbl_icone.pack(pady=(40, 10))
        
        # Textos principais
        lbl_titulo = ctk.CTkLabel(self, text=titulo, font=("Arial", 20, "bold"), text_color="#FFFFFF")
        lbl_titulo.pack()
        
        lbl_desc = ctk.CTkLabel(self, text=desc, font=("Arial", 13), text_color="#A0A0A0")
        lbl_desc.pack(pady=(5, 0))
        
        # Rodapé fixo na base
        lbl_rodape = ctk.CTkLabel(self, text="⭐ 10 questões    ⏱ 30s", font=("Arial", 11), text_color="#5D6275")
        lbl_rodape.pack(side="bottom", pady=20)

        # Garante que clicar no texto também ativa o botão
        for filho in [selo, lbl_icone, lbl_titulo, lbl_desc, lbl_rodape]:
            filho.bind("<Button-1>", lambda e: comando())
            filho.bind("<Enter>", lambda e: self.configure(border_color=cor, cursor="hand2"))
            filho.bind("<Leave>", lambda e: self.configure(border_color="#1A1C29"))

class TelaSelecaoModo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color="#0B0C10")
        self.trocar_tela_callback = trocar_tela_callback
        
        self.dificuldade_atual = "Médio" # Dificuldade Padrão
        
        # --- CABEÇALHO ---
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=40, pady=(30, 0))
        
        btn_voltar = ctk.CTkButton(frame_topo, text="←", font=("Arial", 24, "bold"), width=40, height=40, fg_color="transparent", hover_color="#1E1E2E", command=lambda: trocar_tela_callback("menu"))
        btn_voltar.pack(side="left")
        
        ctk.CTkLabel(frame_topo, text="Escolha seu Modo", font=("Arial", 28, "bold"), text_color="#FFFFFF").pack(side="left", padx=20)

        # --- SELETOR DE DIFICULDADE (O NOVO RECURSO) ---
        self.frame_dificuldade = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_dificuldade.pack(pady=(20, 10))
        
        dificuldades = [("Fácil", "#38B000"), ("Médio", "#FFBE0B"), ("Difícil", "#FF8C00"), ("Extremo", "#D90429")]
        self.botoes_dif = {}
        
        for dif, cor in dificuldades:
            btn = ctk.CTkButton(
                self.frame_dificuldade, text=dif.upper(), font=("Arial", 12, "bold"),
                fg_color=cor if dif == "Médio" else "transparent", 
                text_color="#12131C" if dif == "Médio" else cor,
                border_color=cor, border_width=2, width=120, height=35, corner_radius=20,
                command=lambda d=dif, c=cor: self.mudar_dificuldade(d, c)
            )
            btn.pack(side="left", padx=10)
            self.botoes_dif[dif] = {"widget": btn, "cor": cor}

        # --- CAIXA CENTRALIZADORA E CARTÕES ---
        container_central = ctk.CTkFrame(self, fg_color="transparent")
        container_central.pack(expand=True)

        linha1 = ctk.CTkFrame(container_central, fg_color="transparent")
        linha1.pack(pady=15)
        CardModo(linha1, "Tabuada", "Multiplicação", "#8A2BE2", "✖", "Fácil", "#38B000", lambda: self.iniciar("Tabuada")).pack(side="left", padx=15)
        CardModo(linha1, "Frações", "Partes do todo", "#00BFFF", "◴", "Médio", "#FFBE0B", lambda: self.iniciar("Frações")).pack(side="left", padx=15)
        CardModo(linha1, "Porcentagem", "Descontos", "#38B000", "%", "Médio", "#FFBE0B", lambda: self.iniciar("Porcentagem")).pack(side="left", padx=15)

        linha2 = ctk.CTkFrame(container_central, fg_color="transparent")
        linha2.pack(pady=15)
        CardModo(linha2, "Regra de Três", "Proporcionalidade", "#FFD700", "⚖️", "Difícil", "#D90429", lambda: self.iniciar("Regra de Três")).pack(side="left", padx=15)
        CardModo(linha2, "Equações", "Valor de X", "#D90429", "⊞", "Difícil", "#D90429", lambda: self.iniciar("Equações")).pack(side="left", padx=15)
        CardModo(linha2, "Desafio Rápido", "Mistura total", "#9D4EDD", "⚡", "Extremo", "#8A2BE2", lambda: self.iniciar("Desafio Rápido")).pack(side="left", padx=15)

    def mudar_dificuldade(self, nova_dif, cor_ativa):
        """Atualiza a cor dos botões para mostrar qual dificuldade está selecionada"""
        self.dificuldade_atual = nova_dif
        for dif, dados in self.botoes_dif.items():
            btn = dados["widget"]
            cor_padrao = dados["cor"]
            if dif == nova_dif:
                btn.configure(fg_color=cor_ativa, text_color="#12131C") # Acende
            else:
                btn.configure(fg_color="transparent", text_color=cor_padrao) # Apaga

    def iniciar(self, modo):
        # Passa o modo e a dificuldade escolhida para a tela de jogo
        self.master.telas["jogo"].configurar_modo(modo, self.dificuldade_atual)
        self.trocar_tela_callback("jogo")