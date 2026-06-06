import customtkinter as ctk

COR_FUNDO = "#0B0C10" # Fundo bem escuro
COR_ROXO = "#8A2BE2"
COR_AZUL = "#00BFFF"
COR_AMARELO = "#FFD700"

class TelaMenu(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback

        # Container centralizado
        self.frame_central = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_central.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        self.label_icone = ctk.CTkLabel(self.frame_central, text="⚡ ✨", font=("Arial", 30))
        self.label_icone.pack()

        self.label_titulo = ctk.CTkLabel(self.frame_central, text="Batalha\nMatemática", font=("Arial", 60, "bold"), text_color="#FFFFFF")
        self.label_titulo.pack(pady=(0, 10))

        self.label_sub = ctk.CTkLabel(self.frame_central, text="Aprender nunca foi tão divertido", font=("Arial", 18), text_color="#A0A0A0")
        self.label_sub.pack(pady=(0, 40))

        # Container para os botões ficarem lado a lado
        self.frame_botoes = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botoes.pack()

        self.btn_jogar = ctk.CTkButton(
            self.frame_botoes, text="▷ Jogar", font=("Arial", 18, "bold"),
            fg_color=COR_ROXO, hover_color="#6A1B9A", width=150, height=50,
            command=lambda: self.trocar_tela_callback("selecao_modo")
        )
        self.btn_jogar.pack(side="left", padx=10)

        self.btn_ranking = ctk.CTkButton(
            self.frame_botoes, text="🏆 Ranking", font=("Arial", 18, "bold"),
            fg_color="transparent", border_color=COR_AZUL, border_width=2, hover_color="#1A2B3C", width=150, height=50
        )
        self.btn_ranking.pack(side="left", padx=10)

        self.btn_manual = ctk.CTkButton(
            self.frame_botoes, text="📖 Manual", font=("Arial", 18, "bold"),
            fg_color="transparent", border_color=COR_AMARELO, border_width=2, hover_color="#332B00", width=150, height=50
        )
        self.btn_manual.pack(side="left", padx=10)