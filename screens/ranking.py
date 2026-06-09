# =============================================================================
# BATALHA MATEMÁTICA — View: Ranking
# =============================================================================
# Leaderboard reorganizado em 3 categorias claras via abas:
#   -  GLOBAL: ranking por XP total (com tag e nível)
#   -  RPG:    ranking exclusivo por fase máxima da Jornada
#   -  MODOS:  ranking por modo específico (com filtro)
# =============================================================================

import customtkinter as ctk
from controllers.database import BancoDeDados
from screens.tema import *


class TelaRanking(ctk.CTkFrame):
    """Ranking com 3 categorias em abas e pódio visual."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback
        self._categoria  = "global"       # global | rpg | modo
        self._modo_filtro = "Tabuada"
        self._construir()

    def _construir(self):
        # ── Cabeçalho ─────────────────────────────────────────────────────────
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=40, pady=(26, 8))
        ctk.CTkButton(topo, text="←", font=("Segoe UI Black", 22),
                     fg_color="transparent", hover_color=BG_CARD,
                     text_color=TEXTO2, width=40, height=40, corner_radius=CORNER,
                     command=lambda: self.trocar_tela("menu")).pack(side="left")
        ctk.CTkLabel(topo, text="🏆  RANKING", font=F_TITLE,
                     text_color=TEXTO).pack(side="left", padx=16)

        # ── Abas de categoria ──────────────────────────────────────────────────
        abas = ctk.CTkFrame(self, fg_color=GLASS_BG, corner_radius=24,
                           border_color=GLASS_BORDA, border_width=1)
        abas.pack(pady=(4, 12))
        inner = ctk.CTkFrame(abas, fg_color="transparent")
        inner.pack(padx=6, pady=6)

        self._botoes_aba = {}
        for cat, label, cor in [("global", "🌍 Global", AZUL),
                                ("rpg", "🗺️ Modo RPG", MAGENTA),
                                ("modo", "🎯 Por Modo", TURQUESA)]:
            btn = ctk.CTkButton(
                inner, text=label, font=F_H3, width=140, height=36, corner_radius=20,
                fg_color=cor if cat == "global" else "transparent",
                text_color=BG_APP if cat == "global" else cor,
                hover_color=BG_CARD2,
                command=lambda c=cat: self._mudar_categoria(c)
            )
            btn.pack(side="left", padx=3)
            self._botoes_aba[cat] = (btn, cor)

        # ── Filtro de modo (só visível na categoria "modo") ────────────────────
        self.frame_filtro_modo = ctk.CTkFrame(self, fg_color="transparent")
        self._botoes_modo = []
        for modo in ["Adição", "Subtração", "Tabuada", "Frações",
                     "Porcentagem", "Regra de Três", "Equações", "Desafio Rápido"]:
            b = ctk.CTkButton(
                self.frame_filtro_modo, text=modo, font=F_SMALL,
                height=28, corner_radius=16,
                fg_color="transparent", text_color=TEXTO2,
                border_color=BORDA, border_width=1, hover_color=BG_CARD2,
                command=lambda m=modo: self._selecionar_modo(m)
            )
            b.pack(side="left", padx=3)
            self._botoes_modo.append((b, modo))

        # ── Pódio ───────────────────────────────────────────────────────────────
        self.frame_podio = ctk.CTkFrame(self, fg_color="transparent", height=180)
        self.frame_podio.pack(pady=(6, 4))

        # ── Tabela ────────────────────────────────────────────────────────────
        self.frame_tabela = ctk.CTkFrame(self, fg_color=GLASS_BG,
                                        border_color=GLASS_BORDA, border_width=1,
                                        corner_radius=CORNER_L)
        self.frame_tabela.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        cab = ctk.CTkFrame(self.frame_tabela, fg_color="transparent", height=34)
        cab.pack(fill="x", padx=20, pady=(10, 0))
        cab.pack_propagate(False)
        ctk.CTkLabel(cab, text="#     JOGADOR", font=F_TINY,
                     text_color=TEXTO2).pack(side="left", padx=12)
        self.lbl_cab_dir = ctk.CTkLabel(cab, text="PONTUAÇÃO", font=F_TINY,
                                        text_color=TEXTO2)
        self.lbl_cab_dir.pack(side="right", padx=50)
        ctk.CTkFrame(self.frame_tabela, fg_color=BORDA, height=1).pack(fill="x", padx=16)
        self.lista = ctk.CTkScrollableFrame(self.frame_tabela, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=8, pady=8)

    # ─── Navegação de categoria ──────────────────────────────────────────────

    def atualizar_tela(self):
        self._mudar_categoria(self._categoria)

    def _mudar_categoria(self, cat: str):
        self._categoria = cat
        for c, (btn, cor) in self._botoes_aba.items():
            ativo = c == cat
            btn.configure(fg_color=cor if ativo else "transparent",
                         text_color=BG_APP if ativo else cor)

        # Mostra/esconde filtro de modo
        if cat == "modo":
            self.frame_filtro_modo.pack(pady=(0, 10), after=self._botoes_aba["global"][0].master.master)
            self.frame_filtro_modo.pack(pady=(0, 10))
            self._atualizar_botoes_modo()
        else:
            self.frame_filtro_modo.pack_forget()

        self._carregar()

    def _selecionar_modo(self, modo: str):
        self._modo_filtro = modo
        self._atualizar_botoes_modo()
        self._carregar()

    def _atualizar_botoes_modo(self):
        for b, m in self._botoes_modo:
            ativo = m == self._modo_filtro
            b.configure(fg_color=TURQUESA if ativo else "transparent",
                       text_color=BG_APP if ativo else TEXTO2)

    # ─── Carregamento de dados ────────────────────────────────────────────────

    def _carregar(self):
        for w in self.frame_podio.winfo_children():
            w.destroy()
        for w in self.lista.winfo_children():
            w.destroy()

        if self._categoria == "global":
            dados = BancoDeDados.obter_ranking_geral(100)
            self.lbl_cab_dir.configure(text="XP TOTAL      NÍVEL")
            self._render(dados, tipo="global")
        elif self._categoria == "rpg":
            dados = BancoDeDados.obter_ranking_rpg(100)
            self.lbl_cab_dir.configure(text="FASE MÁX     NÍVEL")
            self._render(dados, tipo="rpg")
        else:
            dados = BancoDeDados.obter_ranking_modo(self._modo_filtro, 100)
            self.lbl_cab_dir.configure(text="PONTOS       TEMPO")
            self._render(dados, tipo="modo")

    def _render(self, dados, tipo: str):
        # Deduplica por jogador (melhor resultado)
        vistos, unicos = set(), []
        for linha in dados:
            chave = (linha[0], linha[1])  # (nome, tag)
            if chave not in vistos:
                vistos.add(chave)
                unicos.append(linha)

        if not unicos:
            msg = "Nenhum herói registrado nesta categoria ainda."
            if tipo == "rpg":
                msg = "Nenhuma jornada RPG registrada. Seja o primeiro herói!"
            ctk.CTkLabel(self.lista, text=msg, font=F_BODY,
                         text_color=TEXTO2).pack(pady=40)
            return

        # ── Pódio Top 3 ─────────────────────────────────────────────────────
        top3 = (unicos + [None, None, None])[:3]
        for dados_pos, posicao, altura in [(top3[1], 2, 70),
                                           (top3[0], 1, 100),
                                           (top3[2], 3, 50)]:
            self._coluna_podio(dados_pos, posicao, altura, tipo)

        # ── Tabela ──────────────────────────────────────────────────────────
        medalhas = {1: "🥇", 2: "🥈", 3: "🥉"}
        meu_id = getattr(self.master, "usuario_logado_id", None)
        minha_tag = BancoDeDados.obter_tag(meu_id) if meu_id else None

        for i, linha in enumerate(unicos):
            pos = i + 1
            nome, tag = linha[0], linha[1]
            destaque = (tag == minha_tag)
            bg = "#1E2540" if destaque else (BG_CARD if i % 2 == 0 else BG_CARD2)
            row = ctk.CTkFrame(self.lista, fg_color=bg, corner_radius=6, height=42)
            row.pack(fill="x", pady=2)
            row.pack_propagate(False)

            cor_pos = {1: OURO, 2: PRATA, 3: BRONZE}.get(pos, TEXTO2)
            ctk.CTkLabel(row, text=medalhas.get(pos, str(pos)), font=F_H3,
                         text_color=cor_pos, width=34).pack(side="left", padx=(12, 12))

            nome_box = ctk.CTkFrame(row, fg_color="transparent")
            nome_box.pack(side="left")
            ctk.CTkLabel(nome_box, text=nome.upper(), font=F_BODY,
                         text_color=TEXTO).pack(side="left")
            ctk.CTkLabel(nome_box, text=f"#{tag}", font=F_TINY,
                         text_color=TEXTO2).pack(side="left", padx=(4, 0))
            if destaque:
                ctk.CTkLabel(nome_box, text=" ◄ VOCÊ", font=F_TINY,
                             text_color=AMARELO).pack(side="left", padx=6)

            if tipo == "global":
                xp, nivel = linha[2], linha[3]
                ctk.CTkLabel(row, text=f"Nv.{nivel}", font=F_SMALL,
                             text_color=TEXTO2).pack(side="right", padx=(0, 18))
                ctk.CTkLabel(row, text=f"{xp:,} XP", font=F_H3,
                             text_color=AMARELO).pack(side="right", padx=10)
            elif tipo == "rpg":
                fase, nivel = linha[2], linha[3]
                ctk.CTkLabel(row, text=f"Nv.{nivel}", font=F_SMALL,
                             text_color=TEXTO2).pack(side="right", padx=(0, 18))
                ctk.CTkLabel(row, text=f"Fase {fase}", font=F_H3,
                             text_color=MAGENTA).pack(side="right", padx=10)
            else:
                pts, _, tempo = linha[2], linha[3], linha[4]
                ctk.CTkLabel(row, text=f"⏱{tempo}s", font=F_SMALL,
                             text_color=TEXTO2).pack(side="right", padx=(0, 18))
                ctk.CTkLabel(row, text=f"{pts:,} pts", font=F_H3,
                             text_color=AMARELO).pack(side="right", padx=10)

    def _coluna_podio(self, dados, posicao, altura, tipo):
        cor = {1: OURO, 2: PRATA, 3: BRONZE}.get(posicao, TEXTO2)
        col = ctk.CTkFrame(self.frame_podio, fg_color="transparent", width=130)
        col.pack(side="left", padx=16, anchor="s")
        if not dados:
            ctk.CTkFrame(col, fg_color=BG_CARD2, corner_radius=CORNER,
                         width=80, height=altura).pack()
            return

        nome, tag, valor = dados[0], dados[1], dados[2]
        ctk.CTkLabel(col, text=nome.upper()[:11], font=F_H3,
                     text_color=TEXTO).pack()
        ctk.CTkLabel(col, text=f"#{tag}", font=F_TINY, text_color=TEXTO2).pack()

        if tipo == "global":
            sufixo = f"{valor:,} XP"
        elif tipo == "rpg":
            sufixo = f"Fase {valor}"
        else:
            sufixo = f"{valor:,} pts"
        ctk.CTkLabel(col, text=sufixo, font=F_H3, text_color=cor).pack(pady=(2, 8))

        bloco = ctk.CTkFrame(col, fg_color=BG_CARD, border_color=cor,
                           border_width=2, corner_radius=CORNER,
                           width=84, height=altura)
        bloco.pack()
        bloco.pack_propagate(False)
        ctk.CTkLabel(bloco, text=str(posicao),
                     font=("Segoe UI Black", 30, "bold"),
                     text_color=cor).place(relx=0.5, rely=0.5, anchor="center")
