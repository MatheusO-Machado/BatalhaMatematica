# =============================================================================
# BATALHA MATEMÁTICA — View: Menu Principal
# =============================================================================
# Layout com:
#   - Header com saudação personalizada, nível e tag do jogador
#   - Card "hero" de destaque para JOGAR
#   - Grid de cards de navegação (Ranking, Como Jogar, Perfil)
#   - Barra de XP visível e indicador de desbloqueio do Modo RPG
# =============================================================================

import customtkinter as ctk
import random
from screens.tema import *
from controllers.database import BancoDeDados, NIVEL_DESBLOQUEIO_RPG


# ─── Helpers de cor para animações ────────────────────────────────────────────
def _hex_para_rgb(c):
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)

def _rgb_para_hex(r, g, b):
    clamp = lambda v: max(0, min(255, int(v)))
    return f"#{clamp(r):02x}{clamp(g):02x}{clamp(b):02x}"

def interpola_cor(c1, c2, t):
    """Interpola duas cores hex por um fator t ∈ [0,1]."""
    r1, g1, b1 = _hex_para_rgb(c1)
    r2, g2, b2 = _hex_para_rgb(c2)
    return _rgb_para_hex(r1 + (r2-r1)*t, g1 + (g2-g1)*t, b1 + (b2-b1)*t)

def clarear_cor(c, fator=0.1):
    """Clareia uma cor hex em direção ao branco pelo fator dado."""
    return interpola_cor(c, "#FFFFFF", fator)


class TelaMenu(ctk.CTkFrame):
    """Menu principal moderno com dashboard do jogador."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback
        self._criar_fundo()
        # A interface é (re)construída ao exibir, para refletir XP/nível atuais
        self._raiz = None

    def pack(self, **kw):
        """Sobrescreve pack para reconstruir a tela sempre que exibida."""
        self._reconstruir()
        super().pack(**kw)

    def _criar_fundo(self):
        """Brilho radial decorativo simulado + símbolos sutis."""
        # Glow superior (simulado com frame translúcido escuro)
        for _ in range(30):
            sym  = random.choice(SIMBOLOS_FUNDO)
            size = random.randint(18, 66)
            px   = random.uniform(0.02, 0.98)
            py   = random.uniform(0.02, 0.98)
            if 0.2 < px < 0.8 and 0.15 < py < 0.85:
                continue
            ctk.CTkLabel(self, text=sym,
                         font=("Segoe UI Black", size, "bold"),
                         text_color=TEXTO3).place(relx=px, rely=py, anchor="center")

    def _reconstruir(self):
        if self._raiz is not None:
            self._raiz.destroy()

        self._raiz = ctk.CTkFrame(self, fg_color="transparent")
        self._raiz.place(relx=0.5, rely=0.5, anchor="center")

        # Carrega dados do jogador
        uid = getattr(self.master, "usuario_logado_id", None)
        nome = getattr(self.master, "usuario_logado_nome", None) or "Herói"
        nivel, xp, tag, fase_rpg = 1, 0, "0000", 0
        if uid:
            dados = BancoDeDados.obter_dados_perfil(uid)
            if dados:
                _, tag, xp, nivel, fase_rpg = dados

        rpg_ok = nivel >= NIVEL_DESBLOQUEIO_RPG

        self._montar_header(nome, tag, nivel, xp)
        self._montar_titulo()
        self._montar_cards(rpg_ok, nivel, fase_rpg)

    # ─── Header (dashboard do jogador) ─────────────────────────────────────────

    def _montar_header(self, nome, tag, nivel, xp):
        header = ctk.CTkFrame(self._raiz, fg_color=GLASS_BG,
                              border_color=GLASS_BORDA, border_width=1,
                              corner_radius=CORNER_L, height=72, width=760)
        header.pack(pady=(0, 24))
        header.pack_propagate(False)

        inner = ctk.CTkFrame(header, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=12)

        # Avatar circular com inicial
        av = ctk.CTkFrame(inner, fg_color=ROXO, width=48, height=48, corner_radius=24)
        av.pack(side="left")
        av.pack_propagate(False)
        ctk.CTkLabel(av, text=(nome[0].upper() if nome else "?"),
                     font=("Segoe UI Black", 22, "bold"),
                     text_color=TEXTO).place(relx=0.5, rely=0.5, anchor="center")

        # Nome + tag
        ident = ctk.CTkFrame(inner, fg_color="transparent")
        ident.pack(side="left", padx=14)
        linha_nome = ctk.CTkFrame(ident, fg_color="transparent")
        linha_nome.pack(anchor="w")
        ctk.CTkLabel(linha_nome, text=nome,
                     font=F_H2, text_color=TEXTO).pack(side="left")
        ctk.CTkLabel(linha_nome, text=f"#{tag}",
                     font=F_SMALL, text_color=TEXTO2).pack(side="left", padx=(4, 0), pady=(4, 0))
        ctk.CTkLabel(ident, text=f"⚔ Bem-vindo de volta!",
                     font=F_TINY, text_color=TEXTO2).pack(anchor="w")

        # Nível + barra XP
        nivel_box = ctk.CTkFrame(inner, fg_color="transparent")
        nivel_box.pack(side="right")

        topo_xp = ctk.CTkFrame(nivel_box, fg_color="transparent")
        topo_xp.pack(anchor="e")
        ctk.CTkLabel(topo_xp, text=f"NÍVEL {nivel}",
                     font=F_H3, text_color=AMARELO).pack(side="left")

        xp_no_nivel = xp % 500
        ctk.CTkLabel(nivel_box, text=f"{xp_no_nivel} / 500 XP",
                     font=F_TINY, text_color=TEXTO2).pack(anchor="e", pady=(0, 2))
        barra = ctk.CTkProgressBar(nivel_box, width=180, height=6,
                                    fg_color=BG_CARD2, progress_color=ROXO)
        barra.pack(anchor="e")
        barra.set(xp_no_nivel / 500)

    # ─── Título ────────────────────────────────────────────────────────────────

    def _montar_titulo(self):
        cont = ctk.CTkFrame(self._raiz, fg_color="transparent")
        cont.pack(pady=(0, 20))
        ctk.CTkLabel(cont, text="⚔️  BATALHA MATEMÁTICA",
                     font=("Segoe UI Black", 38, "bold"),
                     text_color=TEXTO).pack()
        ctk.CTkFrame(cont, fg_color=MAGENTA, width=120, height=3,
                     corner_radius=4).pack(pady=8)
        ctk.CTkLabel(cont, text="Resolva • Vença • Evolua",
                     font=F_BODY, text_color=TEXTO2).pack()

    # ─── Cards ───────────────────────────────────────────────────────────────

    def _montar_cards(self, rpg_ok: bool, nivel: int, fase_rpg: int):
        grid = ctk.CTkFrame(self._raiz, fg_color="transparent")
        grid.pack()

        # ── Card grande JOGAR (esquerda) ──────────────────────────────────────
        card_jogar = self._card_grande(
            grid, "▶", "JOGAR", "Modos clássicos de batalha",
            ROXO, lambda: self.trocar_tela("selecao_modo")
        )
        card_jogar.grid(row=0, column=0, rowspan=2, padx=8, pady=8, sticky="nsew")

        # ── Card Modo RPG (destaque, topo direita) ────────────────────────────
        if rpg_ok:
            sub = f"Jornada do Herói • Fase máx: {fase_rpg}" if fase_rpg else "Jornada do Herói"
            card_rpg = self._card_medio(
                grid, "🗺️", "MODO RPG", sub, MAGENTA,
                lambda: self.trocar_tela("rpg"), destaque=True
            )
        else:
            falta = NIVEL_DESBLOQUEIO_RPG - nivel
            card_rpg = self._card_medio(
                grid, "🔒", "MODO RPG",
                f"Desbloqueie no nível {NIVEL_DESBLOQUEIO_RPG} (faltam {falta})",
                TEXTO3, None, bloqueado=True
            )
        card_rpg.grid(row=0, column=1, columnspan=2, padx=8, pady=8, sticky="nsew")

        # ── Cards pequenos (linha inferior) ───────────────────────────────────
        self._card_pequeno(grid, "🏆", "Ranking", AZUL,
                           lambda: self.trocar_tela("ranking")).grid(
            row=1, column=1, padx=8, pady=8, sticky="nsew")
        self._card_pequeno(grid, "👤", "Perfil", TURQUESA,
                           lambda: self.trocar_tela("perfil")).grid(
            row=1, column=2, padx=8, pady=8, sticky="nsew")

        # ── Botão Como Jogar (largura total) ──────────────────────────────────
        ctk.CTkButton(
            self._raiz, text="📖  Como Jogar",
            font=F_H3, text_color=AMARELO,
            fg_color="transparent", hover_color=BG_CARD2,
            border_color=BORDA, border_width=1,
            height=40, corner_radius=CORNER,
            command=lambda: self.trocar_tela("como_jogar")
        ).pack(fill="x", pady=(16, 0))

    # ─── Construtores de cards ─────────────────────────────────────────────────

    def _card_grande(self, master, icone, titulo, desc, cor, command):
        card = ctk.CTkFrame(master, fg_color=GLASS_BG,
                            border_color=cor, border_width=2,
                            corner_radius=CORNER_L, width=240, height=240)
        card.pack_propagate(False)
        ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=2).pack(fill="x")
        ctk.CTkLabel(card, text=icone, font=("Segoe UI", 64),
                     text_color=cor).pack(pady=(40, 8))
        ctk.CTkLabel(card, text=titulo, font=("Segoe UI Black", 28, "bold"),
                     text_color=TEXTO).pack()
        ctk.CTkLabel(card, text=desc, font=F_SMALL,
                     text_color=TEXTO2, wraplength=200).pack(pady=(6, 0))
        self._tornar_clicavel(card, command, cor)
        return card

    def _card_medio(self, master, icone, titulo, desc, cor, command,
                    destaque=False, bloqueado=False):
        bg = GLASS_BG if not destaque else "#1A1230"
        card = ctk.CTkFrame(master, fg_color=bg,
                            border_color=cor, border_width=2,
                            corner_radius=CORNER_L, height=116)
        card.pack_propagate(False)
        ctk.CTkFrame(card, fg_color=cor, height=4, corner_radius=2).pack(fill="x")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(inner, text=icone, font=("Segoe UI", 40),
                     text_color=cor).pack(side="left", padx=(0, 16))
        txt = ctk.CTkFrame(inner, fg_color="transparent")
        txt.pack(side="left", fill="y", expand=True, anchor="w")
        linha = ctk.CTkFrame(txt, fg_color="transparent")
        linha.pack(anchor="w", pady=(14, 0))
        ctk.CTkLabel(linha, text=titulo, font=("Segoe UI Black", 22, "bold"),
                     text_color=TEXTO if not bloqueado else TEXTO2).pack(side="left")
        if destaque:
            ctk.CTkLabel(linha, text="  NOVO", font=F_TINY,
                         text_color=BG_APP, fg_color=MAGENTA,
                         corner_radius=6).pack(side="left", padx=8)
        ctk.CTkLabel(txt, text=desc, font=F_SMALL,
                     text_color=TEXTO2, anchor="w", wraplength=320).pack(anchor="w")

        if not bloqueado:
            self._tornar_clicavel(card, command, cor)
        return card

    def _card_pequeno(self, master, icone, titulo, cor, command):
        card = ctk.CTkFrame(master, fg_color=GLASS_BG,
                           border_color=BORDA, border_width=1,
                           corner_radius=CORNER_L, height=116)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=icone, font=("Segoe UI", 34),
                     text_color=cor).pack(pady=(24, 4))
        ctk.CTkLabel(card, text=titulo, font=F_H3,
                     text_color=TEXTO).pack()
        self._tornar_clicavel(card, command, cor)
        return card

    def _tornar_clicavel(self, card, command, cor):
        """
        Torna o card inteiro clicável de forma LEVE (sem lag):
        adiciona um realce instantâneo no hover e um pulso curto ao clicar.
        Evita animações por-frame de fg_color (caro no CustomTkinter) e só
        vincula Enter/Leave ao card, não aos filhos, prevenindo lag.
        """
        if command is None:
            return

        # Lê a cor real do card (cards diferentes têm fundos diferentes).
        try:
            cor_base = card.cget("fg_color")
            if isinstance(cor_base, (list, tuple)):
                cor_base = cor_base[-1]
        except Exception:
            cor_base = GLASS_BG
        if not isinstance(cor_base, str) or not cor_base.startswith("#"):
            cor_base = GLASS_BG
        cor_hover = clarear_cor(cor_base, 0.08)   # leve clareada no hover

        # Bordas em repouso (o card de destaque mantém borda colorida)
        borda_repouso_cor = cor if cor == MAGENTA else BORDA
        borda_repouso_larg = 2 if cor == MAGENTA else 1

        estado = {"dentro": False}

        def enter(_):
            # Guarda contra reentradas: só age na 1ª vez que entra no card
            if estado["dentro"]:
                return
            estado["dentro"] = True
            # Troca instantânea (sem loop de frames) → sem lag
            card.configure(fg_color=cor_hover, border_color=cor, border_width=2)

        def leave(e):
            # Só processa o leave real do card (não quando passa sobre um filho).
            # Verifica se o ponteiro ainda está dentro da área do card.
            try:
                x, y = card.winfo_pointerxy()
                wx, wy = card.winfo_rootx(), card.winfo_rooty()
                ww, wh = card.winfo_width(), card.winfo_height()
                if wx <= x <= wx + ww and wy <= y <= wy + wh:
                    return  # ainda dentro do card (passou sobre um filho)
            except Exception:
                pass
            estado["dentro"] = False
            card.configure(fg_color=cor_base,
                           border_color=borda_repouso_cor,
                           border_width=borda_repouso_larg)

        def _restaura_borda():
            larg = 2 if estado["dentro"] else borda_repouso_larg
            card.configure(border_width=larg,
                           border_color=cor if estado["dentro"] else borda_repouso_cor)

        def click(_):
            # Pulso curto e barato: engrossa a borda, dispara a ação logo após
            card.configure(border_color=TEXTO, border_width=3)
            card.after(110, _restaura_borda)
            card.after(120, command)

        # Vincula apenas ao card (não recursivo) para não disparar em cada filho.
        card.bind("<Enter>", enter)
        card.bind("<Leave>", leave)
        card.bind("<Button-1>", click)
        # Filhos só recebem o clique (para a área inteira ser clicável),
        # mas NÃO recebem Enter/Leave (que causavam o lag).
        def bind_click(w):
            for c in w.winfo_children():
                c.bind("<Button-1>", click)
                bind_click(c)
        bind_click(card)