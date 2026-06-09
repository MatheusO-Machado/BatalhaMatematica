# =============================================================================
# BATALHA MATEMÁTICA — View: Seleção de Modo
# =============================================================================
# Grid de cards com 8 modos (incluindo Adição e Subtração novos).
# Seletor de dificuldade em segmented control no topo.
# =============================================================================

import customtkinter as ctk
import random
from screens.tema import *


class TelaSelecaoModo(ctk.CTkFrame):
    """Seleção de modo e dificuldade com layout moderno em grid 4×2."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela       = trocar_tela_callback
        self.dificuldade_atual = "Médio"
        self._botoes_dif       = {}
        self._criar_fundo()
        self._construir()

    def _criar_fundo(self):
        for _ in range(26):
            sym  = random.choice(SIMBOLOS_FUNDO)
            size = random.randint(16, 58)
            px   = random.uniform(0.02, 0.98)
            py   = random.uniform(0.02, 0.98)
            if 0.12 < px < 0.88 and 0.1 < py < 0.9:
                continue
            ctk.CTkLabel(self, text=sym,
                         font=("Segoe UI Black", size, "bold"),
                         text_color=TEXTO3).place(relx=px, rely=py, anchor="center")

    def _construir(self):
        # ── Cabeçalho ─────────────────────────────────────────────────────────
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=40, pady=(28, 8))

        ctk.CTkButton(
            topo, text="←  Voltar", font=F_H3,
            fg_color="transparent", hover_color=BG_CARD,
            text_color=TEXTO2, width=110, height=38, corner_radius=CORNER,
            command=lambda: self.trocar_tela("menu")
        ).pack(side="left")

        ctk.CTkLabel(topo, text="⚔  ESCOLHA SUA BATALHA",
                     font=F_TITLE, text_color=TEXTO).pack(side="left", padx=20)

        # ── Seletor de dificuldade (segmented) ─────────────────────────────────
        cont_dif = ctk.CTkFrame(self, fg_color="transparent")
        cont_dif.pack(pady=(4, 16))

        ctk.CTkLabel(cont_dif, text="DIFICULDADE",
                     font=F_TINY, text_color=TEXTO2).pack()

        seg = ctk.CTkFrame(cont_dif, fg_color=GLASS_BG,
                          border_color=GLASS_BORDA, border_width=1,
                          corner_radius=24)
        seg.pack(pady=(6, 0))

        inner = ctk.CTkFrame(seg, fg_color="transparent")
        inner.pack(padx=6, pady=6)

        for dif, cor in [("Fácil", COR_FACIL), ("Médio", COR_MEDIO),
                         ("Difícil", COR_DIFICIL), ("Extremo", COR_EXTREMO)]:
            btn = ctk.CTkButton(
                inner, text=dif.upper(), font=F_H3,
                width=110, height=34, corner_radius=20,
                fg_color=cor if dif == "Médio" else "transparent",
                text_color=BG_APP if dif == "Médio" else cor,
                hover_color=BG_CARD2,
                command=lambda d=dif: self._mudar_dif(d)
            )
            btn.pack(side="left", padx=3)
            self._botoes_dif[dif] = (btn, cor)

        # ── Grid de modos (4 × 2) ──────────────────────────────────────────────
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(expand=True)

        modos = [
            ("Adição",        "Some os números"),
            ("Subtração",     "Diferença entre valores"),
            ("Tabuada",       "Multiplicação ágil"),
            ("Frações",       "Divisão exata"),
            ("Porcentagem",   "Cálculo de %"),
            ("Regra de Três", "Proporcionalidade"),
            ("Equações",      "Descubra o X"),
            ("Desafio Rápido","Mix de todos!"),
        ]

        for i, (modo, desc) in enumerate(modos):
            r, c = divmod(i, 4)
            self._card_modo(grid, modo, desc).grid(
                row=r, column=c, padx=8, pady=8)

    # ─── Card de modo moderno ──────────────────────────────────────────────────

    def _card_modo(self, master, modo: str, desc: str):
        cor  = CORES_MODO.get(modo, ROXO)
        icon = ICONES_MODO.get(modo, "?")

        card = ctk.CTkFrame(master, fg_color=GLASS_BG,
                           border_color=BORDA, border_width=1,
                           corner_radius=CORNER_L, width=200, height=150)
        card.pack_propagate(False)

        ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=2).pack(fill="x")
        ctk.CTkLabel(card, text=icon, font=("Segoe UI", 38),
                     text_color=cor).pack(pady=(16, 4))
        ctk.CTkLabel(card, text=modo, font=F_H3,
                     text_color=TEXTO).pack()
        ctk.CTkLabel(card, text=desc, font=F_TINY,
                     text_color=TEXTO2, wraplength=170).pack(pady=(2, 0))

        # Hover + clique no card todo
        def enter(_): card.configure(border_color=cor, border_width=2,
                                     fg_color="#171D33")
        def leave(_): card.configure(border_color=BORDA, border_width=1,
                                     fg_color=GLASS_BG)
        def click(_): self._iniciar(modo)
        def bind_rec(w):
            w.bind("<Enter>", enter); w.bind("<Leave>", leave)
            w.bind("<Button-1>", click)
            for ch in w.winfo_children():
                bind_rec(ch)
        bind_rec(card)
        return card

    # ─── Callbacks ──────────────────────────────────────────────────────────────

    def _mudar_dif(self, nova: str):
        self.dificuldade_atual = nova
        for nome, (btn, cor) in self._botoes_dif.items():
            ativo = (nome == nova)
            btn.configure(
                fg_color=cor if ativo else "transparent",
                text_color=BG_APP if ativo else cor
            )

    def _iniciar(self, modo: str):
        self.master.telas["jogo"].configurar_modo(modo, self.dificuldade_atual)
        self.trocar_tela("jogo")
