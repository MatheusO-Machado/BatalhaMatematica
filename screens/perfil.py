# =============================================================================
# BATALHA MATEMÁTICA — View: Perfil do Jogador (ATUALIZADO)
# =============================================================================
# Exibe avatar, tag única, nível/XP, stats e TODAS as conquistas (incluindo
# as exclusivas do Modo RPG). Lê conquistas reais do banco de dados.
# =============================================================================

import customtkinter as ctk
from controllers.database   import BancoDeDados
from controllers.conquistas import CATALOGO
from screens.tema import *


class TelaPerfil(ctk.CTkFrame):
    """Perfil com XP, nível, tag, conquistas e histórico."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback

        self.col_esq = ctk.CTkFrame(self, fg_color=GLASS_BG,
                                   border_color=GLASS_BORDA, border_width=1,
                                   corner_radius=0, width=300)
        self.col_esq.pack(side="left", fill="y")
        self.col_esq.pack_propagate(False)

        self.col_dir = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.col_dir.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    def atualizar_tela(self):
        for w in self.col_esq.winfo_children(): w.destroy()
        for w in self.col_dir.winfo_children(): w.destroy()

        uid = getattr(self.master, "usuario_logado_id", None)
        if not uid:
            self._convidado()
            return

        dados   = BancoDeDados.obter_dados_perfil(uid)
        stats   = BancoDeDados.obter_estatisticas_conquistas(uid)
        hist    = BancoDeDados.obter_historico_recente(uid, 5)
        obtidas = BancoDeDados.obter_conquistas(uid)   # conjunto de chaves

        username, tag, xp, nivel, fase_rpg = dados

        xp_por_nivel = 500
        xp_no_nivel  = xp % xp_por_nivel
        progresso    = xp_no_nivel / xp_por_nivel

        self._esquerda(username, tag, nivel, xp, progresso, xp_por_nivel, stats)
        self._direita(obtidas, hist)

    # ─── Coluna esquerda ────────────────────────────────────────────────────────

    def _esquerda(self, nome, tag, nivel, xp, progresso, xp_por_nivel, stats):
        ctk.CTkButton(self.col_esq, text="← Menu", font=F_SMALL, text_color=TEXTO2,
                     fg_color="transparent", hover_color=BG_CARD2, anchor="w",
                     height=36, corner_radius=CORNER,
                     command=lambda: self.trocar_tela("menu")).pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkFrame(self.col_esq, fg_color=BORDA, height=1).pack(fill="x", padx=16)

        # Avatar
        cont = ctk.CTkFrame(self.col_esq, fg_color="transparent")
        cont.pack(pady=(20, 8))
        av = ctk.CTkFrame(cont, fg_color=ROXO, width=88, height=88, corner_radius=44)
        av.pack(); av.pack_propagate(False)
        ctk.CTkLabel(av, text=(nome[0].upper() if nome else "?"),
                     font=("Segoe UI Black", 40, "bold"),
                     text_color=TEXTO).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.col_esq, text=f"NÍVEL {nivel}", font=F_TINY,
                     text_color=AMARELO).pack()
        # Nome + tag
        linha = ctk.CTkFrame(self.col_esq, fg_color="transparent")
        linha.pack(pady=(2, 16))
        ctk.CTkLabel(linha, text=nome.upper(), font=F_H1, text_color=TEXTO).pack(side="left")
        ctk.CTkLabel(linha, text=f"#{tag}", font=F_SMALL,
                     text_color=TEXTO2).pack(side="left", padx=(4, 0), pady=(6, 0))

        # Barra XP
        fxp = ctk.CTkFrame(self.col_esq, fg_color="transparent")
        fxp.pack(fill="x", padx=28, pady=(0, 4))
        ctk.CTkLabel(fxp, text="XP", font=F_TINY, text_color=TEXTO2).pack(side="left")
        ctk.CTkLabel(fxp, text=f"{xp % xp_por_nivel} / {xp_por_nivel}",
                     font=F_TINY, text_color=TEXTO2).pack(side="right")
        barra = ctk.CTkProgressBar(self.col_esq, height=8, fg_color=BORDA,
                                  progress_color=ROXO)
        barra.pack(fill="x", padx=28); barra.set(progresso)

        ctk.CTkFrame(self.col_esq, fg_color=BORDA, height=1).pack(fill="x", padx=20, pady=20)

        # Mini-stats
        grid = ctk.CTkFrame(self.col_esq, fg_color="transparent")
        grid.pack(fill="x", padx=14)
        self._mini(grid, "🏆", stats["total_partidas"], "Partidas", 0, 0)
        self._mini(grid, "⭐", stats["maior_pontuacao"], "Recorde",  0, 1)
        self._mini(grid, "🗺️", stats["rpg_fase_max"],    "Fase RPG", 1, 0)
        self._mini(grid, "χ",  stats["partidas_equacoes"],"Equações", 1, 1)

        ctk.CTkButton(self.col_esq, text="Sair da Conta", font=F_H3,
                     text_color=VERMELHO, fg_color="transparent",
                     hover_color="#1A0808", border_color=VERMELHO, border_width=1,
                     height=44, corner_radius=CORNER,
                     command=self._logout).pack(side="bottom", fill="x", padx=24, pady=24)

    def _mini(self, master, icone, valor, titulo, r, c):
        f = ctk.CTkFrame(master, fg_color=BG_APP, border_color=BORDA, border_width=1,
                        corner_radius=CORNER, width=126, height=88)
        f.grid(row=r, column=c, padx=6, pady=6); f.pack_propagate(False)
        ctk.CTkLabel(f, text=icone, font=("Segoe UI", 22), text_color=ROXO).pack(pady=(12, 2))
        ctk.CTkLabel(f, text=str(valor), font=F_H2, text_color=TEXTO).pack()
        ctk.CTkLabel(f, text=titulo, font=F_TINY, text_color=TEXTO2).pack()

    # ─── Coluna direita ─────────────────────────────────────────────────────────

    def _direita(self, obtidas: set, hist):
        # Conquistas — separadas em Gerais e Exclusivas do RPG
        ctk.CTkLabel(self.col_dir, text="🏅  Conquistas", font=F_H1,
                     text_color=TEXTO).pack(anchor="w", pady=(0, 4))
        total = len(obtidas)
        ctk.CTkLabel(self.col_dir, text=f"{total} de {len(CATALOGO)} desbloqueadas",
                     font=F_SMALL, text_color=TEXTO2).pack(anchor="w", pady=(0, 12))

        # Gerais
        ctk.CTkLabel(self.col_dir, text="Gerais", font=F_H3,
                     text_color=AZUL).pack(anchor="w", pady=(0, 6))
        grid_g = ctk.CTkFrame(self.col_dir, fg_color="transparent")
        grid_g.pack(fill="x", pady=(0, 16))
        gerais = [(k, v) for k, v in CATALOGO.items() if not v["rpg"]]
        for i, (chave, c) in enumerate(gerais):
            self._card_conq(grid_g, chave, c, chave in obtidas, i % 2, i // 2)

        # Exclusivas RPG
        ctk.CTkLabel(self.col_dir, text="🗺️ Exclusivas do Modo RPG", font=F_H3,
                     text_color=MAGENTA).pack(anchor="w", pady=(0, 6))
        grid_r = ctk.CTkFrame(self.col_dir, fg_color="transparent")
        grid_r.pack(fill="x", pady=(0, 16))
        rpgs = [(k, v) for k, v in CATALOGO.items() if v["rpg"]]
        for i, (chave, c) in enumerate(rpgs):
            self._card_conq(grid_r, chave, c, chave in obtidas, i % 2, i // 2, rpg=True)

        # Histórico
        ctk.CTkLabel(self.col_dir, text="📜  Partidas Recentes", font=F_H1,
                     text_color=TEXTO).pack(anchor="w", pady=(8, 10))
        if not hist:
            ctk.CTkLabel(self.col_dir, text="Nenhuma partida ainda. Entre em batalha!",
                         font=F_BODY, text_color=TEXTO2).pack(anchor="w")
            return
        for modo, pontos, acertos, tempo in hist:
            row = ctk.CTkFrame(self.col_dir, fg_color=BG_CARD, border_color=BORDA,
                             border_width=1, corner_radius=CORNER, height=56)
            row.pack(fill="x", pady=4); row.pack_propagate(False)
            cor = CORES_MODO.get(modo, ROXO)
            ctk.CTkLabel(row, text=ICONES_MODO.get(modo, "🎮"), font=("Segoe UI", 22),
                         text_color=cor).pack(side="left", padx=16)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="y", pady=8)
            ctk.CTkLabel(info, text=modo, font=F_H3, text_color=TEXTO, anchor="w").pack(fill="x")
            ctk.CTkLabel(info, text=f"⏱ {tempo}s", font=F_TINY, text_color=TEXTO2, anchor="w").pack(fill="x")
            ctk.CTkLabel(row, text=f"{pontos:,} pts", font=F_H3,
                         text_color=AMARELO).pack(side="right", padx=18)

    def _card_conq(self, master, chave, dados, ativo, col, linha, rpg=False):
        cor_b = (MAGENTA if rpg else ROXO) if ativo else BORDA
        bg    = BG_CARD if ativo else BG_APP
        ct    = TEXTO if ativo else TEXTO2
        card = ctk.CTkFrame(master, fg_color=bg, border_color=cor_b, border_width=1,
                          corner_radius=CORNER, width=250, height=64)
        card.grid(row=linha, column=col, padx=6, pady=6); card.pack_propagate(False)
        ctk.CTkLabel(card, text=dados["icone"], font=("Segoe UI", 24),
                     text_color=(AMARELO if ativo else TEXTO3)).pack(side="left", padx=12)
        txt = ctk.CTkFrame(card, fg_color="transparent")
        txt.pack(side="left", fill="both", expand=True, pady=8)
        ctk.CTkLabel(txt, text=dados["titulo"], font=F_H3, text_color=ct, anchor="w").pack(fill="x")
        ctk.CTkLabel(txt, text=dados["desc"], font=F_TINY, text_color=TEXTO2,
                     anchor="w", wraplength=160, justify="left").pack(fill="x")
        if ativo:
            ctk.CTkLabel(card, text="✓", font=F_H2, text_color=VERDE).pack(side="right", padx=10)
        else:
            ctk.CTkLabel(card, text="🔒", font=F_BODY, text_color=TEXTO3).pack(side="right", padx=12)

    # ─── Convidado / Logout ───────────────────────────────────────────────────

    def _convidado(self):
        ctk.CTkButton(self.col_esq, text="← Menu", font=F_SMALL, text_color=TEXTO2,
                     fg_color="transparent", hover_color=BG_CARD2, anchor="w",
                     height=36, corner_radius=CORNER,
                     command=lambda: self.trocar_tela("menu")).pack(fill="x", padx=16, pady=(16, 8))
        ctk.CTkLabel(self.col_esq, text="👻", font=("Segoe UI", 52)).pack(pady=(30, 8))
        ctk.CTkLabel(self.col_esq, text="CONVIDADO", font=F_H1, text_color=TEXTO).pack()
        ctk.CTkLabel(self.col_dir, text="Faça login para ver seu perfil.",
                     font=F_H3, text_color=TEXTO2).pack(pady=100)

    def _logout(self):
        self.master.usuario_logado_id = None
        self.master.usuario_logado_nome = None
        self.trocar_tela("login")
