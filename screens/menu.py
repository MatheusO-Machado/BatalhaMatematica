import customtkinter as ctk
import random

# Paleta Dark UI Premium
COR_FUNDO_APP = "#0A0D14"       
COR_CARD = "#12151E"            
COR_BORDAS = "#222738"          
COR_TEXTO_PRINCIPAL = "#FFFFFF" 
COR_TEXTO_SECUNDARIO = "#7E849E"
COR_ROXO = "#8A2BE2"
COR_AZUL = "#00BFFF"
COR_AMARELO = "#FFBE0B"

class BotaoMenuAnimado(ctk.CTkFrame):
    def __init__(self, master, texto, cor_base, cor_texto, cor_borda, command, is_primary=False):
        # A caixa invisível que impede a tela de tremer na animação
        super().__init__(master, fg_color="transparent", width=200, height=75)
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.command = command
        self.is_primary = is_primary
        self.cor_borda = cor_borda
        self.cor_texto = cor_texto

        self.btn = ctk.CTkButton(
            self, text=texto, font=("Arial", 16, "bold"),
            fg_color=cor_base, hover_color="#2A145C" if is_primary else cor_borda, 
            text_color=cor_texto, border_color=cor_borda, border_width=2,
            corner_radius=12, width=170, height=50, command=self.command
        )
        self.btn.place(relx=0.5, rely=0.5, anchor="center")

        # Gatilhos de animação do mouse
        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        # Cresce suavemente. Se for botão de contorno, FORÇA o preenchimento e escurece a letra
        if not self.is_primary:
            self.btn.configure(width=185, height=58, fg_color=self.cor_borda, text_color="#0A0D14")
        else:
            self.btn.configure(width=185, height=58)

    def on_leave(self, e):
        # Retorna ao visual original (transparente com letra neon)
        if not self.is_primary:
            self.btn.configure(width=170, height=50, fg_color="transparent", text_color=self.cor_texto)
        else:
            self.btn.configure(width=170, height=50)


class TelaMenu(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.trocar_tela_callback = trocar_tela_callback

        self.criar_fundo_decorativo()

        # --- BOTÃO PERFIL (Topo Direita) ---
        frame_perfil = ctk.CTkFrame(self, fg_color="transparent")
        frame_perfil.pack(side="top", anchor="ne", padx=30, pady=20)
        
        self.btn_perfil = ctk.CTkButton(
            frame_perfil, text="👤 Meu Perfil", font=("Arial", 13, "bold"),
            fg_color=COR_CARD, hover_color=COR_BORDAS, text_color=COR_TEXTO_PRINCIPAL,
            border_color=COR_BORDAS, border_width=1, corner_radius=20, height=35,
            command=lambda: self.trocar_tela_callback("perfil")
        )
        self.btn_perfil.pack()

        # --- CONTAINER CENTRAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.45, anchor="center")

        # Ícones e Título Gigante
        ctk.CTkLabel(self.main_container, text="⚡ ✨", font=("Arial", 32), text_color=COR_TEXTO_PRINCIPAL).pack(pady=(0, 10))
        ctk.CTkLabel(self.main_container, text="Batalha", font=("Arial", 68, "bold"), text_color=COR_ROXO).pack(pady=0)
        ctk.CTkLabel(self.main_container, text="Matemática", font=("Arial", 68, "bold"), text_color=COR_TEXTO_PRINCIPAL).pack(pady=0)
        
        # Divisor Neon para separar o subtítulo
        ctk.CTkFrame(self.main_container, fg_color=COR_ROXO, width=120, height=3, corner_radius=5).pack(pady=20)
        
        ctk.CTkLabel(self.main_container, text="Aprender nunca foi tão divertido", font=("Arial", 18), text_color=COR_TEXTO_SECUNDARIO).pack(pady=(0, 45))

        # --- BOTÕES DE NAVEGAÇÃO ---
        frame_botoes = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame_botoes.pack()

        BotaoMenuAnimado(
            frame_botoes, texto="▶ Jogar", 
            cor_base=COR_ROXO, cor_texto=COR_TEXTO_PRINCIPAL, cor_borda=COR_ROXO, 
            command=lambda: self.trocar_tela_callback("selecao_modo"), is_primary=True
        ).pack(side="left", padx=10)

        BotaoMenuAnimado(
            frame_botoes, texto="🏆 Ranking", 
            cor_base="transparent", cor_texto=COR_AZUL, cor_borda=COR_AZUL, 
            command=lambda: self.trocar_tela_callback("ranking")
        ).pack(side="left", padx=10)

        BotaoMenuAnimado(
            frame_botoes, texto="📖 Como Jogar", 
            cor_base="transparent", cor_texto=COR_AMARELO, cor_borda=COR_AMARELO, 
            command=lambda: self.trocar_tela_callback("como_jogar")
        ).pack(side="left", padx=10)

        # --- RODAPÉ E ASSINATURA DE DEV ---
        frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        frame_rodape.pack(side="bottom", pady=30)

        ctk.CTkLabel(frame_rodape, text="v1.0", font=("Consolas", 12), text_color=COR_TEXTO_SECUNDARIO).pack(side="left", padx=10)
        ctk.CTkLabel(frame_rodape, text="|", font=("Arial", 12), text_color=COR_BORDAS).pack(side="left")
        ctk.CTkLabel(frame_rodape, text="</> Desenvolvido por Matheus", font=("Consolas", 13, "bold"), text_color=COR_TEXTO_SECUNDARIO).pack(side="left", padx=10)

    def criar_fundo_decorativo(self):
        elementos = ["7", "3", "9", "2", "4", "1", "+", "-", "x", "∑", "θ", "√n", "∞", "∫"]
        for _ in range(30): 
            texto = random.choice(elementos)
            tamanho = random.randint(20, 70)
            
            pos_x = random.uniform(0.05, 0.95)
            pos_y = random.uniform(0.05, 0.95)
            if 0.2 < pos_x < 0.8 and 0.2 < pos_y < 0.8:
                continue 

            lbl = ctk.CTkLabel(self, text=texto, font=("Arial", tamanho, "bold"), text_color="#141824")
            lbl.place(relx=pos_x, rely=pos_y, anchor="center")