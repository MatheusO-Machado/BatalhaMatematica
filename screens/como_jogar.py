import customtkinter as ctk
from screens.tema import *


class TelaComoJogar(ctk.CTkFrame):
    """Tela de manual com seções explicativas em cards rolável."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback
        self._construir()

    def _construir(self):
        # ── Cabeçalho ─────────────────────────────────────────────────────────
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=36, pady=(26, 10))

        ctk.CTkButton(
            topo, text="←", font=("Segoe UI Black", 22),
            fg_color="transparent", hover_color=BG_CARD,
            text_color=TEXTO2, width=40, height=40, corner_radius=CORNER,
            command=lambda: self.trocar_tela("menu")
        ).pack(side="left")

        ctk.CTkLabel(topo, text="📖  COMO JOGAR",
                     font=F_TITLE, text_color=TEXTO).pack(side="left", padx=16)

        # ── Conteúdo rolável ──────────────────────────────────────────────────
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=36, pady=(0, 20))

        secoes = [
            (
                "⚔️  Objetivo da Batalha",
                ROXO,
                [
                    "Você é um Herói enfrentando Monstros Matemáticos!",
                    "Resolva cálculos para atacar o inimigo — cada acerto causa 10 HP de dano.",
                    "Se errar ou o tempo acabar, você leva 5–10 HP de dano.",
                    "Sobreviva às 10 rodadas e maximize sua pontuação!",
                ]
            ),
            (
                "⏱️  Tempo e Pressão",
                CIANO,
                [
                    "Cada questão tem 30 segundos de limite.",
                    "Quanto mais rápido responder, maior o Bônus de Velocidade nos pontos.",
                    "Quando restam 10s, o timer fica amarelo. Abaixo de 5s, vermelho!",
                    "Tempo esgotado = −5 HP no Herói e combo zerado.",
                ]
            ),
            (
                "🔥  Sistema de Combo",
                LARANJA,
                [
                    "Acertos consecutivos ativam o multiplicador de Combo.",
                    "Combo × 0.1 é somado ao multiplicador a cada acerto seguido.",
                    "Exemplo: 5 acertos seguidos → multiplicador de 1.5× (50% a mais de pontos).",
                    "Errar ou deixar o tempo acabar zera o combo imediatamente.",
                    "Combo ≥ 5: cura automática de +5 HP no Herói!",
                ]
            ),
            (
                "📊  Sistema de Pontuação",
                AMARELO,
                [
                    "Pontos Base: 50 por questão correta.",
                    "Bônus de Velocidade: (30 − tempo_gasto) × 2 pts.",
                    "Multiplicador de Combo: 1.0 + (combo × 0.1).",
                    "Multiplicador de Dificuldade: Fácil ×1.0 | Médio ×1.5 | Difícil ×2.0 | Extremo ×3.0.",
                    "Fórmula: pts = int((50 + bônus_velocidade) × mult_combo × mult_dificuldade)",
                ]
            ),
            (
                "⚙️  Dificuldades",
                VERDE,
                [
                    "🟢 Fácil   — operandos de 1 a 5. Ideal para iniciantes.",
                    "🟡 Médio   — operandos de 2 a 12. O desafio padrão.",
                    "🟠 Difícil — operandos de 5 a 25. Calcule rápido!",
                    "🔴 Extremo — operandos de 15 a 99. Apenas para mestres da aritmética.",
                ]
            ),
            (
                "🗺️  Modo RPG — Jornada do Herói (NOVO!)",
                "#E040FB",
                [
                    "Desbloqueado ao atingir o NÍVEL 10!",
                    "Enfrente fases progressivas de dificuldade GRADUAL e infinita.",
                    "A cada 5 fases você encontra um CHEFE poderoso (mais HP e XP).",
                    "Mistura TODOS os modos: adição, subtração, tabuada, frações, %, equações e regra de três.",
                    "Cada acerto causa dano; cada erro fere o Herói. Sobreviva o máximo de fases!",
                    "Concede CONQUISTAS EXCLUSIVAS que só existem neste modo (🗺️ 🛡️ 🏆 💎 🌟).",
                    "Ao vencer um chefe, você recupera 15 HP e ganha XP triplo.",
                    "⚡ CRÍTICO DO HERÓI: acerte 3 perguntas seguidas e seu próximo golpe causa DANO DOBRADO!",
                    "💢 CONTRA-ATAQUE: errar 3 ou mais vezes seguidas faz o inimigo desferir um golpe crítico (pior contra chefes e dificuldades altas).",
                    "Observe a barra de FÚRIA (herói) e o medidor de PERIGO (inimigo) para se planejar.",
                ]
            ),
            (
                "🎮  Modos de Batalha",
                AZUL,
                [
                    "➕  Adição        — some 2 ou 3 parcelas conforme a dificuldade.",
                    "➖  Subtração     — diferença entre valores (sempre positiva).",
                    "✖  Tabuada       — multiplicações puras. Velocidade é tudo.",
                    "◴  Frações       — divisões exatas. Sem decimais.",
                    "↗  Porcentagem   — cálculo de % de um valor.",
                    "⚖️  Regra de Três — proporcionalidade direta.",
                    "χ  Equações      — equações do 1° grau (ax + b = c).",
                    "⚡  Desafio Rápido— sorteia modos aleatoriamente!",
                ]
            ),
            (
                "🧮  A Matemática por Trás do Jogo",
                ROXO,
                [
                    "• LÓGICA BOOLEANA: cada resposta avalia uma proposição V/F que controla dano e pontos.",
                    "• ANÁLISE COMBINATÓRIA: questões geradas por permutação aleatória de operandos.",
                    "• TEORIA DOS CONJUNTOS: um set() impede repetição de questões na mesma partida.",
                    "• FUNÇÕES MATEMÁTICAS: pontuação = função composta de base, velocidade, combo e dificuldade.",
                    "• FUNÇÃO ESCADA (XP): nivel = floor(xp / 500) + 1 — sobe 1 nível a cada 500 XP.",
                ]
            ),
            (
                "💡  Dicas de Campeão",
                AMARELO,
                [
                    "Responda rápido nos primeiros segundos para maximizar o Bônus de Velocidade.",
                    "Mantenha o combo ativo — 5 acertos seguidos curam você e triplicam os pontos!",
                    "No modo Extremo, prefira velocidade a perfeição: combo compensa erros esporádicos.",
                    "O Rank 👑 LENDÁRIO exige 90%+ de acertos E mais de 5 questões corretas.",
                ]
            ),
        ]

        for titulo, cor, itens in secoes:
            self._secao(scroll, titulo, cor, itens)

    def _secao(self, pai, titulo: str, cor: str, itens: list[str]):
        """Cria um card de seção do manual."""
        card = ctk.CTkFrame(pai, fg_color=BG_CARD,
                             border_color=BORDA, border_width=1,
                             corner_radius=CORNER_L)
        card.pack(fill="x", pady=8)

        # Linha neon no topo
        ctk.CTkFrame(card, fg_color=cor, height=3, corner_radius=2).pack(fill="x")

        ctk.CTkLabel(card, text=titulo, font=F_H2,
                     text_color=cor).pack(anchor="w", padx=22, pady=(16, 8))

        for item in itens:
            ctk.CTkLabel(card, text=f"  {item}",
                         font=F_BODY, text_color=TEXTO,
                         anchor="w", justify="left",
                         wraplength=820).pack(anchor="w", padx=22, pady=2)

        ctk.CTkFrame(card, fg_color="transparent", height=12).pack()
