import customtkinter as ctk

COR_FUNDO = "#0B0C10"

class TelaSelecaoModo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback

        # Cabeçalho
        self.frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_topo.pack(fill="x", padx=40, pady=(30, 20))

        self.btn_voltar = ctk.CTkButton(
            self.frame_topo,
            text="←",
            font=("Arial", 24, "bold"),
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#1E1E2E",
            command=lambda: self.trocar_tela_callback("menu")
        )
        self.btn_voltar.pack(side="left")

        self.label_titulo = ctk.CTkLabel(
            self.frame_topo,
            text="Escolha seu Modo",
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        )
        self.label_titulo.pack(side="left", padx=20)

        # Grid de Cartões
        self.frame_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_grid.pack(pady=10)

        # Criando os 6 cartões (Linha, Coluna, Título, Descrição, Cor, Dificuldade)
        self.criar_card(0, 0, "Tabuada", "Domine a multiplicação", "#8A2BE2", "Fácil", "#38B000", "jogo")
        self.criar_card(0, 1, "Frações", "Trabalhe com partes", "#00BFFF", "Médio", "#FFBE0B", "jogo_fracoes")
        self.criar_card(0, 2, "Porcentagem", "Calcule descontos", "#38B000", "Médio", "#FFBE0B", "jogo_porcentagem")

        self.criar_card(1, 0, "Regra de Três", "Proporcionalidade", "#FFD700", "Difícil", "#D90429", "jogo_regra")
        self.criar_card(1, 1, "Equações", "Encontre o X", "#D90429", "Difícil", "#D90429", "jogo_equacoes")
        self.criar_card(1, 2, "Desafio Rápido", "Mistura de tudo", "#9D4EDD", "Extremo", "#8A2BE2", "jogo_misturado")

    def criar_card(self, linha, coluna, titulo, desc, cor_borda, dif_texto, dif_cor, tela_alvo):
        # O Cartão
        card = ctk.CTkFrame(
            self.frame_grid,
            fg_color="#12131C",
            border_color=cor_borda,
            border_width=1,
            corner_radius=15,
            width=260,
            height=180
        )
        card.grid(row=linha, column=coluna, padx=15, pady=15)
        card.pack_propagate(False)

        # Selo de Dificuldade
        selo = ctk.CTkLabel(
            card,
            text=dif_texto,
            font=("Arial", 12, "bold"),
            text_color="#12131C",
            fg_color=dif_cor,
            corner_radius=10,
            width=60,
            height=25
        )
        selo.pack(anchor="ne", padx=10, pady=10)

        # Textos
        lbl_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 20, "bold"),
            text_color=cor_borda
        )
        lbl_titulo.pack(anchor="w", padx=20, pady=(10, 0))

        lbl_desc = ctk.CTkLabel(
            card,
            text=desc,
            font=("Arial", 12),
            text_color="#A0A0A0"
        )
        lbl_desc.pack(anchor="w", padx=20)

        # Botão invisível que cobre o cartão todo
        btn_clique = ctk.CTkButton(
            card,
            text="10 questões  ⏱ 30s",
            font=("Arial", 12),
            text_color="#A0A0A0",
            fg_color="transparent",
            hover_color="#1A1C29",

            # Passa o nome do título do cartão (ex: "Equações", "Frações")
            command=lambda m=titulo: self.iniciar_modo(m)
        )
        btn_clique.pack(side="bottom", fill="x", pady=15)

    def iniciar_modo(self, modo_escolhido):
        # Acessa a tela de jogo, configura o modo escolhido e faz a troca
        tela_jogo = self.master.telas["jogo"]

        tela_jogo.configurar_modo(modo_escolhido)

        self.trocar_tela_callback("jogo")