import customtkinter as ctk

COR_FUNDO = "#0B0C10"
COR_ROXO = "#8A2BE2"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#A0A0A0"
COR_AMARELO = "#FFBE0B"
COR_VERDE = "#38B000"
COR_VERMELHO = "#D90429"

class TelaComoJogar(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback

        # --- CABEÇALHO ---
        frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        frame_topo.pack(fill="x", padx=40, pady=(30, 10))

        btn_voltar = ctk.CTkButton(
            frame_topo, text="←", font=("Arial", 24, "bold"), width=40, height=40,
            fg_color="transparent", hover_color="#1E1E2E", command=lambda: trocar_tela_callback("menu")
        )
        btn_voltar.pack(side="left")

        texto_titulo = " ".join("COMO JOGAR")
        ctk.CTkLabel(frame_topo, text=texto_titulo, font=("Arial", 28, "bold"), text_color=COR_BRANCO).pack(side="left", padx=20)

        # --- CONTAINER DE REGRAS (Rolável) ---
        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent", width=800, height=450)
        self.scroll_container.pack(padx=40, pady=10, fill="both", expand=True)

        # Criando as seções explicativas
        self.criar_secao(
            "🎯 Objetivo do Jogo", 
            "Resolva o máximo de questões matemáticas antes do tempo acabar. Quanto mais rápido você responder corretamente, mais pontos você ganha na partida!", 
            COR_ROXO
        )
        
        self.criar_secao(
            "🔥 Sistema de Combos", 
            "Acerte 3 questões seguidas para ativar o Fogo do Combo! Enquanto o combo estiver ativo, todos os seus pontos serão multiplicados. Se errar ou o tempo acabar, o combo zera.", 
            COR_AMARELO
        )
        
        self.criar_secao(
            "⏱️ O Relógio", 
            "Você tem 30 segundos por questão. Quando restarem apenas 5 segundos, o cronômetro ficará vermelho. Se o tempo esgotar, a questão é considerada errada.", 
            COR_VERMELHO
        )
        
        self.criar_secao(
            "📈 XP e Progressão", 
            "Cada ponto conquistado nas partidas é convertido em XP (Experiência) para o seu Perfil. Acumule XP para subir de nível e jogue bastante para desbloquear as Medalhas de Conquista.", 
            COR_VERDE
        )
        
        self.criar_secao(
            "⚙️ Dificuldades", 
            "• Fácil: Cálculos básicos para relaxar.\n• Médio: O desafio padrão.\n• Difícil: Números maiores e cálculos de cabeça complexos.\n• Extremo: Modo insano. Apenas para os verdadeiros mestres da matemática.", 
            COR_CINZA
        )

    def criar_secao(self, titulo, texto, cor_destaque):
        """Cria um card estilizado para cada regra do jogo"""
        frame = ctk.CTkFrame(self.scroll_container, fg_color="#12131C", border_color="#1A1C29", border_width=2, corner_radius=15)
        frame.pack(fill="x", pady=10, ipady=10)

        ctk.CTkLabel(frame, text=titulo, font=("Arial", 20, "bold"), text_color=cor_destaque).pack(anchor="w", padx=25, pady=(20, 5))
        ctk.CTkLabel(frame, text=texto, font=("Arial", 14), text_color=COR_BRANCO, justify="left", wraplength=700).pack(anchor="w", padx=25, pady=(0, 20))