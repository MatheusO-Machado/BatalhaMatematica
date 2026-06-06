import customtkinter as ctk
import random

# Paleta de Cores Premium (Dark Theme)
COR_FUNDO = "#0B0C10" 
COR_ROXO = "#8A2BE2"
COR_AZUL = "#00BFFF"
COR_AMARELO = "#FFD700"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#A0A0A0"

class BotaoAnimado(ctk.CTkButton):
    """
    Botão com efeito de levitação e mudança de luminosidade.
    """
    def __init__(self, master, cor_base, cor_hover, **kwargs):
        super().__init__(master, fg_color=cor_base, **kwargs)
        self.cor_base = cor_base
        self.cor_hover = cor_hover
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(fg_color=self.cor_hover, cursor="hand2")
        self.pack_configure(pady=(15, 25))

    def on_leave(self, event):
        self.configure(fg_color=self.cor_base)
        self.pack_configure(pady=20)

class TelaMenu(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback

        # 1. ELEMENTOS DE FUNDO AVANÇADOS
        self.criar_fundo_decorativo()

        # 2. CONTAINER PRINCIPAL
        self.frame_central = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_central.place(relx=0.5, rely=0.45, anchor="center")

        # Ícone animado
        self.label_icone = ctk.CTkLabel(self.frame_central, text="⚡ ✨", font=("Arial", 42))
        self.label_icone.pack(pady=(0, 10))

        # Título
        self.label_batalha = ctk.CTkLabel(self.frame_central, text="Batalha", font=("Arial", 72, "bold"), text_color=COR_ROXO)
        self.label_batalha.pack()
        
        self.label_matematica = ctk.CTkLabel(self.frame_central, text="Matemática", font=("Arial", 72, "bold"), text_color=COR_BRANCO)
        self.label_matematica.pack(pady=(0, 20))

        # Linha Neon
        linha_neon = ctk.CTkFrame(self.frame_central, fg_color=COR_ROXO, width=150, height=3, corner_radius=5)
        linha_neon.pack(pady=(0, 20))

        self.label_sub = ctk.CTkLabel(self.frame_central, text="Aprender nunca foi tão divertido", font=("Arial", 20), text_color=COR_CINZA)
        self.label_sub.pack(pady=(0, 50))

        # --- BOTÃO DE PERFIL (Canto Superior Direito) ---
        self.frame_usuario = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_usuario.pack(anchor="ne", padx=40, pady=30)

        # Botão de engrenagem/perfil elegante
        self.btn_perfil = ctk.CTkButton(
            self.frame_usuario, text="👤 Meu Perfil", font=("Arial", 14, "bold"),
            fg_color="#12131C", hover_color=COR_ROXO, text_color=COR_BRANCO,
            border_color="#1A1C29", border_width=1, width=130, height=40, corner_radius=10,
            command=lambda: self.trocar_tela_callback("perfil")
        )
        self.btn_perfil.pack(side="right")

        # 3. ÁREA DOS BOTÕES
        self.frame_botoes = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        self.frame_botoes.pack()

        self.btn_jogar = BotaoAnimado(
            self.frame_botoes, 
            cor_base=COR_ROXO, cor_hover="#A349FF",
            text="▷ Jogar", font=("Arial", 18, "bold"), text_color=COR_BRANCO,
            width=200, height=55, corner_radius=12,
            command=lambda: self.trocar_tela_callback("selecao_modo")
        )
        self.btn_jogar.pack(side="left", padx=15, pady=20)

        self.btn_ranking = BotaoAnimado(
            self.frame_botoes, 
            cor_base="transparent", cor_hover="#1A1F2E",
            text="🏆 Ranking", font=("Arial", 18, "bold"), text_color=COR_AZUL,
            border_color=COR_AZUL, border_width=2, width=200, height=55, corner_radius=12, # <--- OLHA A VÍRGULA AQUI NO FINAL
            command=lambda: self.trocar_tela_callback("ranking")
        )
        self.btn_ranking.pack(side="left", padx=15, pady=20)

        # Botão Como Jogar (Antigo Manual)
        self.btn_como_jogar = BotaoAnimado(
            self.frame_botoes, 
            cor_base="transparent", cor_hover="#2E2800",
            text="📖 Como Jogar", font=("Arial", 18, "bold"), text_color=COR_AMARELO,
            border_color=COR_AMARELO, border_width=2, width=200, height=55, corner_radius=12,
            command=lambda: self.trocar_tela_callback("como_jogar")
        )
        self.btn_como_jogar.pack(side="left", padx=15, pady=20)

        # 4. RODAPÉ
        self.label_rodape = ctk.CTkLabel(
            self, text="v1.0  |  Desenvolvido por Matheus", 
            font=("Arial", 12, "bold"), text_color="#2A2D3E"
        )
        self.label_rodape.pack(side="bottom", pady=20)

    def criar_fundo_decorativo(self):
        """
        Gera um efeito de 'Matrix Matemática' com profundidade.
        Usa múltiplas cores e tamanhos para simular 3D.
        """
        # Adicionado equações complexas e mais símbolos
        simbolos = [
            "+", "-", "x", "÷", "=", "∑", "π", "√", "∞", "∫", "θ", "Δ", 
            "E=mc²", "x²", "y=mx+b", "φ", "Ω", "α", "β", "f(x)", "lim", "dx/dy", "≠", "≈"
        ]
        
        # Três camadas de profundidade visual
        camadas_cores = [
            "#0E0F14", # Muito fundo (quase preto)
            "#12141C", # Fundo médio (cinza escuro)
            "#1A1525"  # Mais perto (roxo extremamente escuro)
        ]
        
        # Aumentamos de 15 para 65 tentativas de desenho
        for _ in range(65):
            simbolo = random.choice(simbolos)
            tamanho = random.randint(14, 40)
            cor = random.choice(camadas_cores)
            
            pos_x = random.uniform(0.01, 0.99)
            pos_y = random.uniform(0.01, 0.99)
            
            # Caixa de proteção: Impede que os símbolos cubram os botões e o título
            # Aumentamos a zona de segurança para acomodar os botões maiores
            if 0.20 < pos_x < 0.80 and 0.25 < pos_y < 0.85:
                continue 

            lbl = ctk.CTkLabel(self, text=simbolo, font=("Arial", tamanho, "bold"), text_color=cor)
            lbl.place(relx=pos_x, rely=pos_y, anchor="center")