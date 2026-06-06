import customtkinter as ctk
import random

# Paleta Dark UI Premium
COR_FUNDO_APP = "#0A0D14"       
COR_CARD = "#12151E"            
COR_BORDAS = "#222738"          
COR_TEXTO_PRINCIPAL = "#FFFFFF" 
COR_TEXTO_SECUNDARIO = "#7E849E"

class BotaoDificuldadeAnimado(ctk.CTkFrame):
    def __init__(self, master, texto, cor_neon, is_active, command):
        # A caixa invisível maior que segura o botão
        super().__init__(master, fg_color="transparent", width=140, height=50)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.cor_neon = cor_neon
        self.is_active = is_active
        self.command_callback = command
        self.texto = texto

        # O Botão Real
        self.btn = ctk.CTkButton(
            self, text=texto.upper(), font=("Arial", 12, "bold"),
            fg_color=cor_neon if is_active else "transparent", 
            text_color="#12131C" if is_active else cor_neon,
            border_color=cor_neon, border_width=2, corner_radius=20,
            width=120, height=35, command=self._on_click
        )
        self.btn.place(relx=0.5, rely=0.5, anchor="center")

        # Eventos de Hover
        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        # Animação: O botão cresce levemente
        if not self.is_active:
            self.btn.configure(width=130, height=40, fg_color="#1A1D29")

    def on_leave(self, e):
        # Animação: O botão volta ao normal
        if not self.is_active:
            self.btn.configure(width=120, height=35, fg_color="transparent")

    def _on_click(self):
        self.command_callback(self.texto, self.cor_neon)

    def set_active(self, active):
        """Atualiza a cor quando o botão é selecionado"""
        self.is_active = active
        if active:
            self.btn.configure(width=120, height=35, fg_color=self.cor_neon, text_color="#12131C")
        else:
            self.btn.configure(width=120, height=35, fg_color="transparent", text_color=self.cor_neon)


class CardModoAnimado(ctk.CTkFrame):
    def __init__(self, master, titulo, subtitulo, cor_neon, icone, command):
        # Container invisível (dá espaço para o cartão crescer)
        super().__init__(master, fg_color="transparent", width=250, height=180)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.cor_neon = cor_neon
        self.command = command

        # O Cartão Real
        self.card = ctk.CTkFrame(self, fg_color=COR_CARD, border_color=COR_BORDAS, border_width=2, corner_radius=15, width=220, height=150)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Conteúdo do Cartão
        self.lbl_icone = ctk.CTkLabel(self.card, text=icone, font=("Arial", 38), text_color=cor_neon)
        self.lbl_icone.pack(pady=(25, 5))
        
        self.lbl_titulo = ctk.CTkLabel(self.card, text=titulo, font=("Arial", 16, "bold"), text_color=COR_TEXTO_PRINCIPAL)
        self.lbl_titulo.pack()
        
        self.lbl_subtitulo = ctk.CTkLabel(self.card, text=subtitulo, font=("Arial", 12), text_color=COR_TEXTO_SECUNDARIO)
        self.lbl_subtitulo.pack()

        # Vincula o evento de clique e hover a TUDO dentro do cartão para não bugar
        self._bind_all(self.card)

    def _bind_all(self, widget):
        """Aplica os gatilhos do mouse em todos os elementos do cartão"""
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Button-1>", lambda e: self.command())
        for child in widget.winfo_children():
            self._bind_all(child)

    def on_enter(self, e):
        # Animação: Expande tamanho, brilha a borda e clareia o fundo
        self.card.configure(width=235, height=165, border_color=self.cor_neon, border_width=2, fg_color="#181B26")

    def on_leave(self, e):
        # Animação: Retorna ao tamanho e cor originais
        self.card.configure(width=220, height=150, border_color=COR_BORDAS, border_width=2, fg_color=COR_CARD)


class TelaSelecaoModo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.trocar_tela_callback = trocar_tela_callback
        self.dificuldade_atual = "Médio"

        # Fundo Animado
        self.criar_fundo_decorativo()

        # Container Principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # --- CABEÇALHO ---
        frame_topo = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame_topo.pack(fill="x", pady=(0, 20))
        
        btn_voltar = ctk.CTkButton(
            frame_topo, text="← Voltar", font=("Arial", 14, "bold"), width=40, height=40,
            fg_color="transparent", hover_color=COR_CARD, text_color=COR_TEXTO_SECUNDARIO,
            command=lambda: trocar_tela_callback("menu")
        )
        btn_voltar.pack(side="left")

        # --- SELETOR DE DIFICULDADE (Animado) ---
        self.frame_dificuldade = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_dificuldade.pack(pady=(0, 30))
        
        dificuldades = [("Fácil", "#38B000"), ("Médio", "#FFBE0B"), ("Difícil", "#FF8C00"), ("Extremo", "#D90429")]
        self.botoes_dif = {}
        
        for dif, cor in dificuldades:
            btn = BotaoDificuldadeAnimado(
                self.frame_dificuldade, texto=dif, cor_neon=cor, 
                is_active=(dif == "Médio"), command=self.mudar_dificuldade
            )
            btn.pack(side="left", padx=5)
            self.botoes_dif[dif] = btn

        # --- GRADE DE CARTÕES (Animados) ---
        container_cards = ctk.CTkFrame(self.main_container, fg_color="transparent")
        container_cards.pack(expand=True)

        linha1 = ctk.CTkFrame(container_cards, fg_color="transparent")
        linha1.pack(pady=5)
        CardModoAnimado(linha1, "Tabuada", "Multiplicação ágil", "#8A2BE2", "✖", lambda: self.iniciar("Tabuada")).pack(side="left", padx=5)
        CardModoAnimado(linha1, "Frações", "Partes do todo", "#00BFFF", "◴", lambda: self.iniciar("Frações")).pack(side="left", padx=5)
        CardModoAnimado(linha1, "Porcentagem", "Descontos reais", "#38B000", "↗", lambda: self.iniciar("Porcentagem")).pack(side="left", padx=5)

        linha2 = ctk.CTkFrame(container_cards, fg_color="transparent")
        linha2.pack(pady=5)
        CardModoAnimado(linha2, "Regra de Três", "Proporcionalidade", "#FFBE0B", "⚖️", lambda: self.iniciar("Regra de Três")).pack(side="left", padx=5)
        CardModoAnimado(linha2, "Equações", "Descubra o X", "#D90429", "⊞", lambda: self.iniciar("Equações")).pack(side="left", padx=5)
        CardModoAnimado(linha2, "Desafio Rápido", "Mistura insana", "#FF007F", "⚡", lambda: self.iniciar("Desafio Rápido")).pack(side="left", padx=5)

    def criar_fundo_decorativo(self):
        """Partículas matemáticas flutuantes estilo Dark UI"""
        elementos = ["7", "3", "9", "2", "4", "1", "+", "-", "x", "∑", "θ", "√n", "∞", "∫"]
        for _ in range(25): 
            texto = random.choice(elementos)
            tamanho = random.randint(20, 70)
            
            # Deixa o centro mais livre
            pos_x = random.uniform(0.05, 0.95)
            pos_y = random.uniform(0.05, 0.95)
            if 0.2 < pos_x < 0.8 and 0.2 < pos_y < 0.8:
                continue 

            lbl = ctk.CTkLabel(self, text=texto, font=("Arial", tamanho, "bold"), text_color="#141824")
            lbl.place(relx=pos_x, rely=pos_y, anchor="center")

    def mudar_dificuldade(self, nova_dif, cor_ativa):
        """Atualiza a lógica visual dos botões animados"""
        self.dificuldade_atual = nova_dif
        for dif, btn in self.botoes_dif.items():
            btn.set_active(dif == nova_dif)

    def iniciar(self, modo):
        # Manda para a tela de jogo com o modo e dificuldade selecionados!
        self.master.telas["jogo"].configurar_modo(modo, self.dificuldade_atual)
        self.trocar_tela_callback("jogo")