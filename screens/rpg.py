# =============================================================================
# BATALHA MATEMÁTICA — View: Modo RPG (Jornada do Herói) — VISUAL APRIMORADO
# =============================================================================
# Tela de batalha por fases com visual épico:
#   - Arenas estilizadas para Herói e Inimigo com molduras temáticas
#   - Barras de HP grandes com numérico e animação de dano (flash + shake)
#   - Barra de FÚRIA do herói: enche a cada acerto; cheia = próximo golpe CRÍTICO
#   - Indicador de PERIGO do inimigo: erros seguidos acendem o alerta de crítico
#   - Inimigos variados (bestiário) e efeitos visuais de golpe crítico
# =============================================================================

import customtkinter as ctk
import random
from controllers.rpg        import MotorRPG, SEQUENCIA_CRITICA
from controllers.pontuacao  import SistemaPontuacao
from controllers.database   import BancoDeDados
from controllers.conquistas import GerenciadorConquistas
from screens.tema import *


class BarraHP(ctk.CTkFrame):
    """Barra de vida grande com rótulo, valor numérico e cor dinâmica."""

    def __init__(self, master, largura=240, **kw):
        super().__init__(master, fg_color="transparent", **kw)
        self._max, self._atual = 100, 100

        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x")
        self._titulo = ctk.CTkLabel(topo, text="❤ VIDA", font=F_TINY, text_color=TEXTO)
        self._titulo.pack(side="left")
        self._val = ctk.CTkLabel(topo, text="100 / 100", font=F_TINY, text_color=TEXTO2)
        self._val.pack(side="right")

        # Trilho com moldura
        moldura = ctk.CTkFrame(self, fg_color=BG_APP, corner_radius=8,
                               border_color=BORDA, border_width=1,
                               width=largura, height=20)
        moldura.pack(fill="x", pady=(2, 0))
        moldura.pack_propagate(False)
        self._trilho = ctk.CTkFrame(moldura, fg_color="#0A0C16", corner_radius=8)
        self._trilho.pack(fill="both", expand=True, padx=3, pady=3)
        self._fill = ctk.CTkFrame(self._trilho, fg_color=VERDE, corner_radius=6)
        self._fill.place(x=0, y=0, relheight=1.0, relwidth=1.0)
        # Brilho no topo da barra (efeito de relevo)
        self._brilho = ctk.CTkFrame(self._fill, fg_color="#FFFFFF", corner_radius=6,
                                    height=3)
        self._brilho.place(relx=0.02, rely=0.12, relwidth=0.96)

    def _cor(self):
        r = self._atual / self._max if self._max else 0
        if r > 0.5:  return VERDE
        if r > 0.25: return AMARELO
        return VERMELHO

    def set(self, atual, maximo=None):
        if maximo is not None:
            self._max = maximo
        self._atual = max(0, min(atual, self._max))
        r = self._atual / self._max if self._max else 0
        cor = self._cor()
        self._fill.configure(fg_color=cor)
        self._fill.place(x=0, y=0, relheight=1.0, relwidth=max(0.001, r))
        self._val.configure(text=f"{self._atual} / {self._max}")

    def flash(self, cor=VERMELHO):
        atual = self._fill.cget("fg_color")
        self._fill.configure(fg_color=cor)
        self.after(220, lambda: self._fill.configure(fg_color=self._cor()))

    def set_titulo(self, t):
        self._titulo.configure(text=t)


class BarraFuria(ctk.CTkFrame):
    """
    Barra de FÚRIA do herói: enche a cada acerto consecutivo.
    Quando cheia (3 acertos), o próximo golpe é crítico.
    """

    def __init__(self, master, largura=240, **kw):
        super().__init__(master, fg_color="transparent", **kw)
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x")
        ctk.CTkLabel(topo, text="🔥 FÚRIA", font=F_TINY,
                     text_color=LARANJA).pack(side="left")
        self._status = ctk.CTkLabel(topo, text="", font=F_TINY, text_color=ROSA)
        self._status.pack(side="right")

        # Segmentos (um por acerto necessário)
        self._segmentos = []
        seg_cont = ctk.CTkFrame(self, fg_color="transparent")
        seg_cont.pack(fill="x", pady=(3, 0))
        for i in range(SEQUENCIA_CRITICA):
            seg = ctk.CTkFrame(seg_cont, fg_color=BG_CARD2, corner_radius=4,
                               height=10, border_color=BORDA, border_width=1)
            seg.pack(side="left", fill="x", expand=True,
                     padx=(0 if i == 0 else 3, 0))
            self._segmentos.append(seg)

    def set_nivel(self, acertos_seguidos: int):
        cheio = acertos_seguidos >= SEQUENCIA_CRITICA
        for i, seg in enumerate(self._segmentos):
            if i < (acertos_seguidos % SEQUENCIA_CRITICA) or (cheio and acertos_seguidos > 0):
                seg.configure(fg_color=LARANJA if not cheio else ROSA)
            else:
                seg.configure(fg_color=BG_CARD2)
        if cheio:
            self._status.configure(text="CRÍTICO PRONTO!")
            for seg in self._segmentos:
                seg.configure(fg_color=ROSA)
        else:
            faltam = SEQUENCIA_CRITICA - (acertos_seguidos % SEQUENCIA_CRITICA)
            self._status.configure(
                text=f"+{faltam} p/ crítico" if acertos_seguidos > 0 else "")


class IndicadorPerigo(ctk.CTkFrame):
    """Mostra erros seguidos do herói; acende quando o inimigo vai dar crítico."""

    def __init__(self, master, **kw):
        super().__init__(master, fg_color="transparent", **kw)
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x")
        ctk.CTkLabel(topo, text="⚠ PERIGO", font=F_TINY,
                     text_color=VERMELHO).pack(side="left")
        self._status = ctk.CTkLabel(topo, text="", font=F_TINY, text_color=VERMELHO)
        self._status.pack(side="right")

        self._segmentos = []
        seg_cont = ctk.CTkFrame(self, fg_color="transparent")
        seg_cont.pack(fill="x", pady=(3, 0))
        for i in range(SEQUENCIA_CRITICA):
            seg = ctk.CTkFrame(seg_cont, fg_color=BG_CARD2, corner_radius=4,
                               height=8, border_color=BORDA, border_width=1)
            seg.pack(side="left", fill="x", expand=True,
                     padx=(0 if i == 0 else 3, 0))
            self._segmentos.append(seg)

    def set_nivel(self, erros_seguidos: int):
        perigo = erros_seguidos >= SEQUENCIA_CRITICA
        for i, seg in enumerate(self._segmentos):
            ativo = i < min(erros_seguidos, SEQUENCIA_CRITICA)
            seg.configure(fg_color=VERMELHO if ativo else BG_CARD2)
        if perigo:
            self._status.configure(text="CONTRA-ATAQUE!")
        elif erros_seguidos > 0:
            self._status.configure(text=f"{erros_seguidos} erro(s)")
        else:
            self._status.configure(text="")


class TelaRPG(ctk.CTkFrame):
    """Modo RPG: Jornada do Herói com fases, chefes e danos críticos."""

    LIMITE_TEMPO = 25

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback
        self.motor       = None
        self.pontos      = SistemaPontuacao("Difícil")
        self.pergunta    = None
        self.timer_id    = None
        self.tempo_rest  = self.LIMITE_TEMPO
        self.tempo_total = 0
        self._criar_fundo()
        self._construir()

    def pack(self, **kw):
        super().pack(**kw)
        self._iniciar_jornada()

    def _criar_fundo(self):
        for _ in range(46):
            sym  = random.choice(SIMBOLOS_FUNDO)
            size = random.randint(14, 54)
            px   = random.uniform(0.01, 0.99)
            py   = random.uniform(0.01, 0.99)
            if 0.16 < px < 0.84 and 0.12 < py < 0.92:
                continue
            ctk.CTkLabel(self, text=sym,
                         font=("Segoe UI Black", size, "bold"),
                         text_color="#0C0F1A").place(relx=px, rely=py, anchor="center")

    # ─── HUD ────────────────────────────────────────────────────────────────────

    def _construir(self):
        # ── Topbar ─────────────────────────────────────────────────────────────
        topbar = ctk.CTkFrame(self, fg_color=GLASS_BG, corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        bar = ctk.CTkFrame(topbar, fg_color="transparent")
        bar.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.97)

        ctk.CTkButton(bar, text="✖ Fugir", font=F_SMALL, text_color=VERMELHO,
                     fg_color="transparent", hover_color="#1A0808",
                     border_color=VERMELHO, border_width=1,
                     width=86, height=30, corner_radius=CORNER,
                     command=self._sair).pack(side="left", padx=6)
        ctk.CTkLabel(bar, text="🗺️  JORNADA DO HERÓI", font=F_H2,
                     text_color=MAGENTA).pack(side="left", padx=14)

        self.lbl_pontos = ctk.CTkLabel(bar, text="⭐ 0", font=F_H2, text_color=AMARELO)
        self.lbl_pontos.pack(side="right", padx=12)
        self.lbl_tempo = ctk.CTkLabel(bar, text="⏱ 25", font=F_TIMER, text_color=CIANO)
        self.lbl_tempo.pack(side="right", padx=12)

        # ── Banner de fase ──────────────────────────────────────────────────────
        self.banner = ctk.CTkFrame(self, fg_color="#16112B", corner_radius=0, height=42)
        self.banner.pack(fill="x")
        self.banner.pack_propagate(False)
        bn = ctk.CTkFrame(self.banner, fg_color="transparent")
        bn.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96)
        self.lbl_fase = ctk.CTkLabel(bn, text="FASE 1", font=F_H1, text_color=TEXTO)
        self.lbl_fase.pack(side="left")
        self.lbl_chefe = ctk.CTkLabel(bn, text="", font=F_H2, text_color=ROSA)
        self.lbl_chefe.pack(side="left", padx=10)
        self.lbl_dif_fase = ctk.CTkLabel(bn, text="● Fácil", font=F_H3, text_color=COR_FACIL)
        self.lbl_dif_fase.pack(side="right")

        # ── Barra de tempo ────────────────────────────────────────────────────
        self.barra_tempo = ctk.CTkProgressBar(self, height=5, fg_color=BG_CARD2,
                                              progress_color=CIANO, corner_radius=0)
        self.barra_tempo.pack(fill="x")
        self.barra_tempo.set(1.0)

        # ── Arena de batalha ──────────────────────────────────────────────────
        # Usa pack horizontal: HUDs laterais com largura fixa (side left/right),
        # centro (cálculos) absorve todo o espaço restante (expand=True).
        arena = ctk.CTkFrame(self, fg_color="transparent")
        arena.pack(fill="both", expand=True, padx=14, pady=10)

        # Importante: monta laterais ANTES do centro para reservarem largura fixa.
        self._montar_arena_heroi(arena)
        self._montar_arena_inimigo(arena)
        self._montar_centro(arena)

    def _montar_arena_heroi(self, master):
        col = ctk.CTkFrame(master, fg_color=GLASS_BG, corner_radius=CORNER_L,
                          border_width=2, border_color=TURQUESA, width=200)
        col.pack(side="left", fill="y", padx=(0, 8))
        col.pack_propagate(False)
        ctk.CTkFrame(col, fg_color=TURQUESA, height=3, corner_radius=2).pack(fill="x")
        ctk.CTkFrame(col, fg_color=TURQUESA, height=3, corner_radius=2).pack(fill="x")

        ctk.CTkLabel(col, text="⚔ HERÓI", font=F_TINY, text_color=TURQUESA).pack(pady=(8, 0))

        # Plataforma do herói (menor)
        palco = ctk.CTkFrame(col, fg_color="#0E1A1E", corner_radius=44,
                            width=84, height=84, border_color=TURQUESA, border_width=2)
        palco.pack(pady=4)
        palco.pack_propagate(False)
        self.sprite_h = ctk.CTkLabel(palco, text="🦸", font=("Segoe UI", 40))
        self.sprite_h.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_nome_h = ctk.CTkLabel(col, text="Herói", font=F_H3, text_color=TEXTO)
        self.lbl_nome_h.pack(pady=(2, 0))

        self.flash_h = ctk.CTkLabel(col, text="", font=("Segoe UI Black", 16, "bold"))
        self.flash_h.pack(pady=(0, 2))

        self.hp_heroi = BarraHP(col, largura=150)
        self.hp_heroi.set_titulo("❤ VIDA")
        self.hp_heroi.pack(padx=12, pady=(0, 6))

        # Barra de fúria (combo → crítico)
        self.furia = BarraFuria(col, largura=150)
        self.furia.pack(padx=12, pady=(0, 4))

        ctk.CTkFrame(col, fg_color=BORDA, height=1).pack(fill="x", padx=12, pady=2)
        self.lbl_stats_h = ctk.CTkLabel(col, text="✅ 0   ❌ 0",
                                        font=F_TINY, text_color=TEXTO2)
        self.lbl_stats_h.pack(pady=(2, 8))

    def _montar_centro(self, master):
        col = ctk.CTkFrame(master, fg_color="transparent")
        col.pack(side="left", fill="both", expand=True)

        card = ctk.CTkFrame(col, fg_color=GLASS_BG, corner_radius=CORNER_L,
                           border_width=2, border_color=MAGENTA)
        card.pack(fill="both", expand=True)
        self._card_q = card
        ctk.CTkFrame(card, fg_color=MAGENTA, height=4, corner_radius=2).pack(fill="x")

        self.lbl_combo = ctk.CTkLabel(card, text="", font=("Segoe UI Black", 16),
                                     text_color=LARANJA)
        self.lbl_combo.pack(pady=(16, 0))
        # Pergunta em destaque grande, ocupando o espaço central
        self.lbl_pergunta = ctk.CTkLabel(card, text="?",
                                        font=("Segoe UI Black", 68, "bold"),
                                        text_color=TEXTO, wraplength=560)
        self.lbl_pergunta.pack(expand=True, pady=10)
        self.entrada = ctk.CTkEntry(card, font=("Segoe UI Black", 34, "bold"),
                                   width=380, height=70, justify="center",
                                   placeholder_text="Resposta...", text_color=AMARELO,
                                   fg_color=BG_INPUT, border_color=BORDA,
                                   border_width=2, corner_radius=CORNER)
        self.entrada.pack(pady=(0, 14))
        self.entrada.bind("<Return>", lambda _: self._verificar())
        self.btn = ctk.CTkButton(card, text="⚔  ATACAR", font=("Segoe UI Bold", 20, "bold"),
                                text_color=TEXTO, fg_color=MAGENTA,
                                hover_color="#C026D3", width=380, height=56,
                                corner_radius=CORNER, command=self._verificar)
        self.btn.pack(pady=(0, 22))
        self.lbl_feedback = ctk.CTkLabel(col, text="", font=F_H1)
        self.lbl_feedback.pack(pady=(8, 0))

    def _montar_arena_inimigo(self, master):
        col = ctk.CTkFrame(master, fg_color=GLASS_BG, corner_radius=CORNER_L,
                          border_width=2, border_color=VERMELHO, width=200)
        col.pack(side="right", fill="y", padx=(8, 0))
        col.pack_propagate(False)
        self._col_inimigo = col
        self._faixa_inimigo = ctk.CTkFrame(col, fg_color=VERMELHO, height=3, corner_radius=2)
        self._faixa_inimigo.pack(fill="x")

        ctk.CTkLabel(col, text="💀 INIMIGO", font=F_TINY, text_color=VERMELHO).pack(pady=(8, 0))

        self._palco_i = ctk.CTkFrame(col, fg_color="#1E0E12", corner_radius=44,
                            width=84, height=84, border_color=VERMELHO, border_width=2)
        self._palco_i.pack(pady=4)
        self._palco_i.pack_propagate(False)
        self.sprite_i = ctk.CTkLabel(self._palco_i, text="🟢", font=("Segoe UI", 40))
        self.sprite_i.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_nome_i = ctk.CTkLabel(col, text="...", font=F_H3,
                                      text_color=TEXTO, wraplength=150)
        self.lbl_nome_i.pack(pady=(2, 0))

        self.flash_i = ctk.CTkLabel(col, text="", font=("Segoe UI Black", 16, "bold"))
        self.flash_i.pack(pady=(0, 2))

        self.hp_inimigo = BarraHP(col, largura=150)
        self.hp_inimigo.set_titulo("💀 HP")
        self.hp_inimigo.pack(padx=12, pady=(0, 6))

        # Indicador de perigo (erros seguidos → contra-ataque crítico)
        self.perigo = IndicadorPerigo(col)
        self.perigo.pack(padx=12, pady=(0, 4))

        ctk.CTkFrame(col, fg_color=BORDA, height=1).pack(fill="x", padx=12, pady=2)
        self.lbl_derrotados = ctk.CTkLabel(col, text="☠️ Derrotados: 0",
                                          font=F_TINY, text_color=TEXTO2)
        self.lbl_derrotados.pack(pady=(2, 8))

    # ─── Jornada ─────────────────────────────────────────────────────────────

    def _iniciar_jornada(self):
        self.motor = MotorRPG()
        self.pontos = SistemaPontuacao("Difícil")
        self.tempo_total = 0

        nome = getattr(self.master, "usuario_logado_nome", None) or "Herói"
        self.lbl_nome_h.configure(text=nome)
        self.hp_heroi.set(self.motor.hp_heroi, MotorRPG.HP_MAX_HEROI)
        self.furia.set_nivel(0)
        self.perigo.set_nivel(0)
        self.lbl_pontos.configure(text="⭐ 0")

        uid = getattr(self.master, "usuario_logado_id", None)
        if uid:
            GerenciadorConquistas.verificar_rpg(uid, 0, iniciou=True)

        self._carregar_fase()

    def _carregar_fase(self):
        f = self.motor.fase
        cor_dif = CORES_DIFIC.get(f.dificuldade, COR_MEDIO)

        self.lbl_fase.configure(text=f"FASE {f.numero}")
        self.lbl_dif_fase.configure(text=f"● {f.dificuldade}", text_color=cor_dif)
        self.sprite_i.configure(text=f.sprite)
        self.lbl_nome_i.configure(text=f.nome_inimigo)
        self.hp_inimigo.set(self.motor.hp_inimigo_atual, f.hp_inimigo)
        self.lbl_derrotados.configure(text=f"☠️ Derrotados: {self.motor.inimigos_derrotados}")
        self.furia.set_nivel(self.motor.acertos_seguidos)
        self.perigo.set_nivel(self.motor.erros_seguidos)

        # Visual de chefe: molduras douradas/rosa e palco maior
        if f.eh_chefe:
            self.lbl_chefe.configure(text="⚠ CHEFE")
            self.banner.configure(fg_color="#2A0E1A")
            self._col_inimigo.configure(border_color=ROSA, border_width=3)
            self._faixa_inimigo.configure(fg_color=ROSA)
            self._palco_i.configure(border_color=ROSA, fg_color="#2A0E1A")
            self.sprite_i.configure(font=("Segoe UI", 50))
        else:
            self.lbl_chefe.configure(text="")
            self.banner.configure(fg_color="#16112B")
            self._col_inimigo.configure(border_color=VERMELHO, border_width=2)
            self._faixa_inimigo.configure(fg_color=VERMELHO)
            self._palco_i.configure(border_color=VERMELHO, fg_color="#1E0E12")
            self.sprite_i.configure(font=("Segoe UI", 40))

        self._proxima_pergunta()

    def _proxima_pergunta(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.pergunta = self.motor.gerar_pergunta()
        self.lbl_pergunta.configure(text=self.pergunta["pergunta"])
        self.entrada.configure(state="normal", border_color=BORDA)
        self.entrada.delete(0, "end")
        self.entrada.focus()
        self.lbl_feedback.configure(text="")
        self.lbl_combo.configure(text=self.pontos.get_nivel_combo())
        self.tempo_rest = self.LIMITE_TEMPO
        self._atualizar_timer()
        self.timer_id = self.after(1000, self._tick)

    def _tick(self):
        self.tempo_rest -= 1
        self.tempo_total += 1
        self._atualizar_timer()
        if self.tempo_rest <= 0:
            self._tempo_esgotado()
        else:
            self.timer_id = self.after(1000, self._tick)

    def _atualizar_timer(self):
        cor = VERMELHO if self.tempo_rest <= 5 else (AMARELO if self.tempo_rest <= 10 else CIANO)
        self.lbl_tempo.configure(text=f"⏱ {self.tempo_rest}", text_color=cor)
        self.barra_tempo.configure(progress_color=cor)
        self.barra_tempo.set(self.tempo_rest / self.LIMITE_TEMPO)

    # ─── Combate ────────────────────────────────────────────────────────────────

    def _verificar(self):
        if self.entrada.cget("state") == "disabled":
            return
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        resp_user = self.entrada.get().strip()
        resp_ok   = self.pergunta["resposta"]
        tempo_gasto = self.LIMITE_TEMPO - self.tempo_rest
        self.entrada.configure(state="disabled")

        # ÁLGEBRA BOOLEANA: proposição de acerto
        if resp_user == resp_ok:
            self._processar_acerto(tempo_gasto)
        else:
            self._processar_erro(resp_ok)

    def _processar_acerto(self, tempo_gasto):
        _, mult = self.pontos.registrar_acerto(tempo_gasto)
        r = self.motor.acertar(bonus_combo=mult)

        self.entrada.configure(border_color=VERDE)
        self.hp_inimigo.set(self.motor.hp_inimigo_atual, self.motor.fase.hp_inimigo)
        self.lbl_pontos.configure(text=f"⭐ {self.motor.pontos:,}")
        self.lbl_combo.configure(text=self.pontos.get_nivel_combo())
        self.furia.set_nivel(self.motor.acertos_seguidos)
        self.perigo.set_nivel(0)

        if r["critico"]:
            # Efeito de CRÍTICO do herói
            self.hp_inimigo.flash(ROSA)
            self._shake(self._palco_i)
            self._flash(self.flash_i, f"💥CRÍTICO! −{r['dano_causado']}", ROSA)
            self.lbl_feedback.configure(text="⚡ GOLPE CRÍTICO! ⚡", text_color=ROSA)
            self.furia.set_nivel(0)
        else:
            self.hp_inimigo.flash(VERMELHO)
            self._flash(self.flash_i, f"−{r['dano_causado']}", VERMELHO)
            self.lbl_feedback.configure(text="✓ Acerto!", text_color=VERDE)

        if r["inimigo_derrotado"]:
            self.lbl_feedback.configure(
                text=f"☠️ Derrotado! +{r['xp_ganho']} XP", text_color=VERDE)
            self.hp_heroi.set(self.motor.hp_heroi, MotorRPG.HP_MAX_HEROI)
            self.furia.set_nivel(0)
            self.perigo.set_nivel(0)
            self._verificar_conquistas_rpg()
            self.after(1300, self._carregar_fase)
            return

        self._atualizar_stats()
        self.after(1150, self._proxima_pergunta)

    def _processar_erro(self, resp_ok):
        self.pontos.registrar_erro()
        r = self.motor.errar()
        self.entrada.configure(border_color=VERMELHO)
        self.hp_heroi.set(self.motor.hp_heroi, MotorRPG.HP_MAX_HEROI)
        self.furia.set_nivel(0)
        self.perigo.set_nivel(self.motor.erros_seguidos)

        if r["critico"]:
            # Contra-ataque CRÍTICO do inimigo
            self.hp_heroi.flash(ROSA)
            self._shake(self.sprite_h)
            self._flash(self.flash_h, f"💢CRÍTICO! −{r['dano_recebido']}", ROSA)
            self.lbl_feedback.configure(
                text=f"💢 CONTRA-ATAQUE CRÍTICO! Era {resp_ok}", text_color=ROSA)
        else:
            self.hp_heroi.flash(VERMELHO)
            self._flash(self.flash_h, f"−{r['dano_recebido']}", VERMELHO)
            self.lbl_feedback.configure(text=f"✗ Errou! Era {resp_ok}", text_color=VERMELHO)

        if r["heroi_morreu"]:
            self.after(1300, self._game_over)
            return

        self._atualizar_stats()
        self.after(1200, self._proxima_pergunta)

    def _tempo_esgotado(self):
        self.entrada.configure(state="disabled", border_color=VERMELHO)
        self.pontos.registrar_erro()
        r = self.motor.tempo_esgotado()
        self.hp_heroi.set(self.motor.hp_heroi, MotorRPG.HP_MAX_HEROI)
        self.furia.set_nivel(0)
        self.perigo.set_nivel(self.motor.erros_seguidos)

        if r["critico"]:
            self.hp_heroi.flash(ROSA)
            self._shake(self.sprite_h)
            self._flash(self.flash_h, f"💢−{r['dano_recebido']}", ROSA)
            self.lbl_feedback.configure(
                text=f"💢 Tempo + crítico! Era {self.pergunta['resposta']}", text_color=ROSA)
        else:
            self.hp_heroi.flash(AMARELO)
            self._flash(self.flash_h, f"⏰−{r['dano_recebido']}", AMARELO)
            self.lbl_feedback.configure(
                text=f"⏰ Tempo! Era {self.pergunta['resposta']}", text_color=AMARELO)

        if r["heroi_morreu"]:
            self.after(1300, self._game_over)
        else:
            self._atualizar_stats()
            self.after(1200, self._proxima_pergunta)

    def _atualizar_stats(self):
        self.lbl_stats_h.configure(
            text=f"✅ {self.motor.acertos_totais}   ❌ {self.motor.erros_totais}")
        self.lbl_derrotados.configure(
            text=f"☠️ Derrotados: {self.motor.inimigos_derrotados}")

    def _verificar_conquistas_rpg(self):
        uid = getattr(self.master, "usuario_logado_id", None)
        if not uid:
            return
        fase_atual = self.motor.fase_numero
        chefe = (fase_atual - 1) % 5 == 0 and fase_atual > 1
        GerenciadorConquistas.verificar_rpg(
            uid, fase_alcancada=fase_atual - 1, chefe_derrotado=chefe)

    # ─── Animações ────────────────────────────────────────────────────────────

    def _flash(self, lbl, txt, cor):
        lbl.configure(text=txt, text_color=cor)
        self.after(900, lambda: lbl.configure(text=""))

    def _shake(self, widget):
        """Pequena animação de tremor para reforçar o impacto do crítico."""
        try:
            info = widget.place_info()
            base = float(info.get("relx", 0.5))
        except Exception:
            return
        deslocamentos = [0.04, -0.04, 0.03, -0.03, 0.0]
        def passo(i=0):
            if i >= len(deslocamentos):
                widget.place_configure(relx=base)
                return
            widget.place_configure(relx=base + deslocamentos[i])
            self.after(45, lambda: passo(i + 1))
        passo()

    # ─── Fim de Jogo ─────────────────────────────────────────────────────────────

    def _game_over(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        m = self.motor
        uid = getattr(self.master, "usuario_logado_id", None)
        if uid:
            BancoDeDados.salvar_partida(
                usuario_id=uid, modo="Jornada RPG",
                pontos=m.pontos, acertos=m.acertos_totais,
                tempo=self.tempo_total, fase_rpg=m.fase_numero)
            GerenciadorConquistas.verificar_rpg(
                uid, fase_alcancada=m.fase_numero,
                pontos=m.pontos, inimigos_derrotados=m.inimigos_derrotados)

        overlay = ctk.CTkFrame(self, fg_color="#05060A", corner_radius=0)
        overlay.place(relwidth=1, relheight=1)
        box = ctk.CTkFrame(overlay, fg_color=GLASS_BG, border_color=MAGENTA,
                          border_width=2, corner_radius=CORNER_L, width=460, height=360)
        box.place(relx=0.5, rely=0.5, anchor="center")
        box.pack_propagate(False)
        ctk.CTkFrame(box, fg_color=MAGENTA, height=4, corner_radius=2).pack(fill="x")
        ctk.CTkLabel(box, text="🗺️", font=("Segoe UI", 48)).pack(pady=(20, 0))
        ctk.CTkLabel(box, text="JORNADA ENCERRADA", font=F_TITLE, text_color=TEXTO).pack()
        ctk.CTkLabel(box, text=f"Você alcançou a Fase {m.fase_numero}!",
                     font=F_H1, text_color=MAGENTA).pack(pady=(4, 0))
        ctk.CTkLabel(box, text=f"⭐ {m.pontos:,} pontos",
                     font=F_H2, text_color=AMARELO).pack(pady=8)
        ctk.CTkLabel(box,
                     text=f"☠️ {m.inimigos_derrotados} inimigos   ✅ {m.acertos_totais} acertos   ❌ {m.erros_totais} erros",
                     font=F_SMALL, text_color=TEXTO2).pack()

        bf = ctk.CTkFrame(box, fg_color="transparent")
        bf.pack(pady=22)
        ctk.CTkButton(bf, text="🔄 Nova Jornada", font=F_H2,
                     fg_color=MAGENTA, hover_color="#C026D3", text_color=TEXTO,
                     width=170, height=46, corner_radius=CORNER,
                     command=lambda: [overlay.destroy(), self._iniciar_jornada()]).pack(side="left", padx=8)
        ctk.CTkButton(bf, text="🏠 Menu", font=F_H2,
                     fg_color="transparent", hover_color=BG_CARD2,
                     border_color=BORDA, border_width=1, text_color=TEXTO,
                     width=130, height=46, corner_radius=CORNER,
                     command=lambda: [overlay.destroy(), self.trocar_tela("menu")]).pack(side="left", padx=8)

    def _sair(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        m = self.motor
        uid = getattr(self.master, "usuario_logado_id", None)
        if uid and m and m.fase_numero > 1:
            BancoDeDados.salvar_partida(
                usuario_id=uid, modo="Jornada RPG",
                pontos=m.pontos, acertos=m.acertos_totais,
                tempo=self.tempo_total, fase_rpg=m.fase_numero)
        self.trocar_tela("menu")