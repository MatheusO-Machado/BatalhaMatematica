# =============================================================================
# BATALHA MATEMÁTICA — View: Tela de Resultados
# =============================================================================
# Exibe o resumo da partida com rank, estatísticas e botões de ação.
# =============================================================================

import customtkinter as ctk
import random
from screens.tema import *


class BotaoResultado(ctk.CTkFrame):
    """Botão animado para a tela de resultados."""

    def __init__(self, master, texto: str, cor: str,
                 is_primary: bool = False, command=None):
        super().__init__(master, fg_color="transparent", width=230, height=72)
        self.pack_propagate(False)
        self._primary = is_primary
        self._cor     = cor

        self.btn = ctk.CTkButton(
            self, text=texto.upper(),
            font=F_H2, text_color=BG_APP if is_primary else cor,
            fg_color=cor if is_primary else "transparent",
            hover_color=ROXO_HOVER if is_primary else BG_CARD2,
            border_color=cor, border_width=2,
            corner_radius=CORNER, width=210, height=52,
            command=command
        )
        self.btn.place(relx=0.5, rely=0.5, anchor="center")
        self.btn.bind("<Enter>", lambda _: self.btn.configure(width=220, height=58))
        self.btn.bind("<Leave>", lambda _: self.btn.configure(width=210, height=52))


class TelaResultados(ctk.CTkFrame):
    """Tela de fim de partida com rank, stats e opções de navegação."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback
        self._criar_fundo()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def _criar_fundo(self):
        for _ in range(28):
            sym  = random.choice(SIMBOLOS_FUNDO)
            size = random.randint(16, 60)
            px   = random.uniform(0.02, 0.98)
            py   = random.uniform(0.02, 0.98)
            if 0.25 < px < 0.75 and 0.15 < py < 0.85:
                continue
            ctk.CTkLabel(self, text=sym,
                         font=("Segoe UI Black", size, "bold"),
                         text_color=TEXTO3).place(relx=px, rely=py, anchor="center")

    # ─── Exibição ─────────────────────────────────────────────────────────────

    def mostrar_resultados(self, pontos: int, acertos: int, erros: int,
                           tempo: int, max_combo: int):
        """
        Renderiza a tela com os dados da partida encerrada.

        LÓGICA BOOLEANA — Classificação de Rank:
            O rank é determinado por proposições booleanas encadeadas (if/elif).
            Seja A = (taxa_acerto >= limiar) e B = (acertos > mínimo):
                A ∧ B → rank superior
            Isso implementa a operação AND da Álgebra Booleana.
        """
        for w in self.container.winfo_children():
            w.destroy()

        total = acertos + erros
        # FUNÇÕES MATEMÁTICAS: taxa de acerto = acertos / total × 100
        taxa  = (acertos / total * 100) if total > 0 else 0.0

        # ── ÁLGEBRA BOOLEANA: Classificação de rank ────────────────────────
        # Avalia proposições compostas (AND lógico) para cada rank.
        if taxa >= 90 and acertos > 5:
            rank, cor_rank, titulo = "👑", OURO,    "LENDÁRIO!"
        elif taxa >= 70 and acertos > 2:
            rank, cor_rank, titulo = "🌟", ROXO,    "EXCELENTE!"
        elif taxa >= 50:
            rank, cor_rank, titulo = "🔥", AZUL,    "MUITO BOM!"
        else:
            rank, cor_rank, titulo = "📚", TEXTO2,  "CONTINUE TREINANDO"

        # ── Cabeçalho ─────────────────────────────────────────────────────
        ctk.CTkLabel(self.container, text="⚔  FIM DE BATALHA",
                     font=F_H3, text_color=TEXTO2).pack(pady=(0, 10))

        # ── Card principal ─────────────────────────────────────────────────
        card = ctk.CTkFrame(
            self.container, fg_color=BG_CARD,
            border_color=cor_rank, border_width=2,
            corner_radius=CORNER_L, width=520
        )
        card.pack(pady=6)

        # Linha neon superior
        ctk.CTkFrame(card, fg_color=cor_rank,
                     height=3, corner_radius=2).pack(fill="x")

        # Selo de rank
        selo = ctk.CTkFrame(card, fg_color=BG_CARD2,
                             corner_radius=40, width=72, height=72)
        selo.pack(pady=(18, 4))
        selo.pack_propagate(False)
        ctk.CTkLabel(selo, text=rank,
                     font=("Segoe UI", 40)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=titulo,
                     font=F_H3, text_color=cor_rank).pack(pady=(0, 8))

        # Pontuação em destaque
        ctk.CTkLabel(card, text="PONTUAÇÃO TOTAL",
                     font=F_TINY, text_color=TEXTO2).pack()
        ctk.CTkLabel(card, text=f"{pontos:,}",
                     font=("Segoe UI Black", 60, "bold"),
                     text_color=TEXTO).pack(pady=(0, 16))

        # Separador
        ctk.CTkFrame(card, fg_color=BORDA, height=1).pack(fill="x", padx=36, pady=(0, 16))

        # Grid de 4 stats
        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=28, pady=(0, 24))

        self._stat(grid, "🎯", f"{acertos}", "Acertos",   VERDE,    0, 0)
        self._stat(grid, "❌", f"{erros}",   "Erros",     VERMELHO, 0, 1)
        self._stat(grid, "⏱️", f"{tempo}s",  "Tempo",     CIANO,    1, 0)
        self._stat(grid, "⚡", f"{max_combo}×","Max Combo",AMARELO,  1, 1)

        # ── Botões de ação ────────────────────────────────────────────────
        frame_btns = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_btns.pack(pady=16)

        BotaoResultado(frame_btns, "▶ Jogar Novamente",
                       ROXO, is_primary=True,
                       command=lambda: self.trocar_tela("selecao_modo")).pack(side="left", padx=10)
        BotaoResultado(frame_btns, "🏠 Menu Principal",
                       BORDA_NEON,
                       command=lambda: self.trocar_tela("menu")).pack(side="left", padx=10)

    def _stat(self, master, icone, valor, titulo, cor, linha, col):
        """Cria um mini-card de estatística no grid 2×2."""
        f = ctk.CTkFrame(master, fg_color=BG_CARD2,
                          border_color=BORDA, border_width=1,
                          corner_radius=CORNER, width=195, height=68)
        f.grid(row=linha, column=col, padx=8, pady=6)
        f.pack_propagate(False)

        ctk.CTkLabel(f, text=icone, font=("Segoe UI", 22),
                     text_color=cor).pack(side="left", padx=16)
        info = ctk.CTkFrame(f, fg_color="transparent")
        info.pack(side="left", fill="y", pady=10)
        ctk.CTkLabel(info, text=valor, font=F_H2,
                     text_color=TEXTO, anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=titulo, font=F_TINY,
                     text_color=TEXTO2, anchor="w").pack(fill="x")
