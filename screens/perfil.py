import customtkinter as ctk
from utils.database import BancoDeDados

COR_FUNDO = "#0B0C10"
COR_ROXO = "#8A2BE2"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#A0A0A0"
COR_AMARELO = "#FFD700"

class TelaPerfil(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback

        # Container Centralizado
        self.container_central = ctk.CTkFrame(self, fg_color="transparent")
        self.container_central.place(relx=0.5, rely=0.5, anchor="center")

    def atualizar_tela(self):
        """Recarrega os dados do perfil sempre que a tela é aberta."""
        for widget in self.container_central.winfo_children():
            widget.destroy()

        usuario_id = self.master.usuario_logado_id
        if not usuario_id:
            return

        # Puxa os dados do banco
        dados = BancoDeDados.obter_dados_perfil(usuario_id)
        stats = BancoDeDados.obter_estatisticas_conquistas(usuario_id)

        username, xp_total, _ = dados
        
        # Lógica de Nível (Cada nível precisa de 200 XP)
        xp_por_nivel = 200
        nivel_atual = (xp_total // xp_por_nivel) + 1
        xp_atual_no_nivel = xp_total % xp_por_nivel
        progresso_xp = xp_atual_no_nivel / xp_por_nivel

        # --- BOTÃO VOLTAR ---
        btn_voltar = ctk.CTkButton(
            self.container_central, text="← Voltar ao Menu", font=("Arial", 14, "bold"),
            fg_color="transparent", hover_color="#1A1C29", text_color=COR_CINZA,
            border_color="#2A2D3E", border_width=1, width=150, height=35, corner_radius=10,
            command=lambda: self.trocar_tela_callback("menu")
        )
        btn_voltar.pack(anchor="w", pady=(0, 20))

        # --- CARD DE IDENTIDADE DO JOGADOR ---
        card_usuario = ctk.CTkFrame(self.container_central, fg_color="#12131C", border_color="#1A1C29", border_width=2, corner_radius=20, width=750, height=140)
        card_usuario.pack(pady=(0, 20))
        card_usuario.pack_propagate(False)

        # Avatar / Círculo de Nível
        box_nivel = ctk.CTkFrame(card_usuario, fg_color=COR_ROXO, width=80, height=80, corner_radius=40)
        box_nivel.place(x=30, y=30)
        ctk.CTkLabel(box_nivel, text=str(nivel_atual), font=("Arial", 32, "bold"), text_color=COR_BRANCO).place(relx=0.5, rely=0.5, anchor="center")

        # Nome e XP
        ctk.CTkLabel(card_usuario, text=username.upper(), font=("Arial", 24, "bold"), text_color=COR_BRANCO).place(x=130, y=30)
        ctk.CTkLabel(card_usuario, text=f"Nível {nivel_atual}  •  {xp_total} XP Total", font=("Arial", 14), text_color=COR_CINZA).place(x=130, y=65)

        # Barra de Progresso de XP
        barra_xp = ctk.CTkProgressBar(card_usuario, width=580, height=8, fg_color="#1A1C29", progress_color=COR_ROXO)
        barra_xp.place(x=130, y=95)
        barra_xp.set(progresso_xp)
        
        # Texto de quanto falta para upar
        xp_restante = xp_por_nivel - xp_atual_no_nivel
        ctk.CTkLabel(card_usuario, text=f"Faltam {xp_restante} XP para o Nível {nivel_atual + 1}", font=("Arial", 11), text_color="#5D6275").place(x=130, y=108)

        # --- SEÇÃO DE CONQUISTAS ---
        ctk.CTkLabel(self.container_central, text="M E D A L H A S   E   C O N Q U I S T A S", font=("Arial", 14, "bold"), text_color=COR_ROXO).pack(pady=(10, 15))

        frame_medalhas = ctk.CTkFrame(self.container_central, fg_color="transparent")
        frame_medalhas.pack()

        # Definição das regras das conquistas
        lista_conquistas = [
            {"titulo": "Pioneiro", "desc": "Jogou a primeira partida", "condicao": stats["total_partidas"] >= 1, "icone": "🌱"},
            {"titulo": "Veterano", "desc": "Completou 10 partidas", "condicao": stats["total_partidas"] >= 10, "icone": "⚔️"},
            {"titulo": "Mestre do Placar", "desc": "Fez +150 pts em uma partida", "condicao": stats["maior_pontuacao"] >= 150, "icone": "👑"},
            {"titulo": "Carrasco do X", "desc": "Completou 5 Equações", "condicao": stats["partidas_equacoes"] >= 5, "icone": "⊞"}
        ]

        # Renderiza os cards de conquista na horizontal
        for col, conq in enumerate(lista_conquistas):
            self.criar_card_conquista(frame_medalhas, conq, col)

    def criar_card_conquista(self, master, dados, coluna):
        desbloqueado = dados["condicao"]
        cor_borda = COR_ROXO if desbloqueado else "#1A1C29"
        cor_fundo = "#12131C" if desbloqueado else "#0D0E15"
        cor_texto_titulo = COR_BRANCO if desbloqueado else "#5D6275"
        cor_icone = COR_AMARELO if desbloqueado else "#3D4155"

        card = ctk.CTkFrame(master, fg_color=cor_fundo, border_color=cor_borda, border_width=1.5, corner_radius=15, width=175, height=200)
        card.grid(row=0, column=coluna, padx=8)
        card.pack_propagate(False)

        # Ícone da medalha
        ctk.CTkLabel(card, text=dados["icone"], font=("Arial", 46), text_color=cor_icone).pack(pady=(25, 10))
        
        # Título da Conquista
        ctk.CTkLabel(card, text=dados["titulo"], font=("Arial", 14, "bold"), text_color=cor_texto_titulo).pack(pady=2)
        
        # Descrição menor
        lbl_desc = ctk.CTkLabel(card, text=dados["desc"], font=("Arial", 11), text_color="#5D6275", wrap_length=150)
        lbl_desc.pack(pady=5)

        # Selo de Bloqueado/Desbloqueado na base
        status_texto = "CONCLUÍDO" if desbloqueado else "BLOQUEADO"
        status_cor = "#38B000" if desbloqueado else "#2A2D3E"
        status_cor_texto = "white" if desbloqueado else COR_CINZA
        
        ctk.CTkLabel(
            card, text=status_texto, font=("Arial", 9, "bold"), 
            fg_color=status_cor, text_color=status_cor_texto, corner_radius=6, width=110, height=22
        ).pack(side="bottom", pady=15)