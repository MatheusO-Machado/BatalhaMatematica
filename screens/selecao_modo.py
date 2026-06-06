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
        
        # --- CABEÇALHO ---
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=40, pady=(30, 0))
        
        btn_voltar = ctk.CTkButton(frame_topo, text="←", font=("Arial", 24, "bold"), width=40, height=40, fg_color="transparent", hover_color="#1E1E2E", command=lambda: trocar_tela_callback("menu"))
        btn_voltar.pack(side="left")
        
        ctk.CTkLabel(frame_topo, text="Escolha seu Modo", font=("Arial", 28, "bold"), text_color="#FFFFFF").pack(side="left", padx=20)

        # --- CAIXA CENTRALIZADORA ---
        # Tudo que entrar aqui vai ficar perfeitamente no meio da tela
        container_central = ctk.CTkFrame(self, fg_color="transparent")
        container_central.pack(expand=True)

        # --- LINHA 1 (3 Cartões) ---
        linha1 = ctk.CTkFrame(container_central, fg_color="transparent")
        linha1.pack(pady=15)
        
        CardModo(linha1, "Tabuada", "Multiplicação", "#8A2BE2", "✖", "Fácil", "#38B000", lambda: self.iniciar("Tabuada")).pack(side="left", padx=15)
        CardModo(linha1, "Frações", "Partes do todo", "#00BFFF", "◴", "Médio", "#FFBE0B", lambda: self.iniciar("Frações")).pack(side="left", padx=15)
        CardModo(linha1, "Porcentagem", "Descontos", "#38B000", "%", "Médio", "#FFBE0B", lambda: self.iniciar("Porcentagem")).pack(side="left", padx=15)

        # --- LINHA 2 (2 Cartões) ---
        # --- LINHA 2 (3 Cartões) ---
        linha2 = ctk.CTkFrame(container_central, fg_color="transparent")
        linha2.pack(pady=15)
        
        CardModo(linha2, "Regra de Três", "Proporcionalidade", "#FFD700", "⚖️", "Difícil", "#D90429", lambda: self.iniciar("Regra de Três")).pack(side="left", padx=15)
        CardModo(linha2, "Equações", "Valor de X", "#D90429", "⊞", "Difícil", "#D90429", lambda: self.iniciar("Equações")).pack(side="left", padx=15)
        CardModo(linha2, "Desafio Rápido", "Mistura total", "#9D4EDD", "⚡", "Extremo", "#8A2BE2", lambda: self.iniciar("Desafio Rápido")).pack(side="left", padx=15)

    def iniciar(self, modo):
        self.master.telas["jogo"].configurar_modo(modo)
        self.trocar_tela_callback("jogo")