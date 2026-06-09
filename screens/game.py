# =============================================================================
# BATALHA MATEMÁTICA — View: Tela de Jogo (HUD de Batalha RPG)
# =============================================================================
# A tela mais complexa do projeto. Gerencia:
#   - Loop de partida com 10 questões
#   - Temporizador regressivo de 30s por questão
#   - HUD de HP do Herói e do Inimigo (barras de vida estilo RPG)
#   - Efeitos visuais: piscar, animação de dano, flash de combo
#
# MATEMÁTICA APLICADA (comentada in-code):
#   1. LÓGICA BOOLEANA       — controle de fluxo (acerto/erro/fim)
#   2. TEORIA DOS CONJUNTOS  — anti-repetição de perguntas via set()
#   3. FUNÇÕES MATEMÁTICAS   — pontuação (SistemaPontuacao)
#   4. ANÁLISE COMBINATÓRIA  — geração de questões (GeradorMatematico)
# =============================================================================

import customtkinter as ctk
import random
from controllers.pontuacao import SistemaPontuacao
from controllers.geradores import GeradorMatematico
from controllers.database  import BancoDeDados
from controllers.conquistas import GerenciadorConquistas
from screens.tema import *


def clarear(cor, fator=0.1):
    """
    Clareia (fator>0) ou escurece (fator<0) uma cor hex #RRGGBB.
    Usado para gerar a cor de hover do botão a partir da cor do modo.
    """
    cor = cor.lstrip("#")
    r, g, b = int(cor[0:2], 16), int(cor[2:4], 16), int(cor[4:6], 16)
    if fator >= 0:
        r = r + (255 - r) * fator
        g = g + (255 - g) * fator
        b = b + (255 - b) * fator
    else:
        f = 1 + fator
        r, g, b = r * f, g * f, b * f
    clamp = lambda v: max(0, min(255, int(v)))
    return f"#{clamp(r):02x}{clamp(g):02x}{clamp(b):02x}"


# ─── Bestiário do Modo Clássico ─────────────────────────────────────────────
# Cada inimigo tem NOME e SPRITE próprios, dando identidade visual única.
# A dificuldade define o conjunto de inimigos possíveis (atmosfera crescente).
INIMIGOS = {
    "Fácil": [
        {"nome": "Goblin Calculista",  "sprite": "👺"},
        {"nome": "Slime Somador",      "sprite": "🟢"},
        {"nome": "Kobold Subtrator",   "sprite": "🦎"},
        {"nome": "Rato Contador",      "sprite": "🐀"},
        {"nome": "Fada Numérica",      "sprite": "🧚"},
    ],
    "Médio": [
        {"nome": "Ogro Multiplicador", "sprite": "👹"},
        {"nome": "Troll Divisório",    "sprite": "🧌"},
        {"nome": "Esqueleto Algébrico","sprite": "💀"},
        {"nome": "Vampiro das Frações","sprite": "🧛"},
        {"nome": "Golem de Cálculo",   "sprite": "🗿"},
    ],
    "Difícil": [
        {"nome": "Dragão das Frações", "sprite": "🐲"},
        {"nome": "Lich da Equação",    "sprite": "☠️"},
        {"nome": "Titã Combinatório",  "sprite": "🗿"},
        {"nome": "Serpe Polinomial",   "sprite": "🐍"},
        {"nome": "Mago do Caos",       "sprite": "🧙"},
    ],
    "Extremo": [
        {"nome": "Caos Matemático",    "sprite": "🌌"},
        {"nome": "Void Infinito",      "sprite": "🕳️"},
        {"nome": "Deus dos Números",   "sprite": "👁️"},
        {"nome": "Devorador de Axiomas","sprite": "👾"},
        {"nome": "Leviatã do Cálculo", "sprite": "🐉"},
    ],
}


class BarraVida(ctk.CTkFrame):
    """
    Barra de HP estilo RPG com cor dinâmica.
    Verde → Amarela → Vermelha conforme HP diminui.
    """

    def __init__(self, master, largura: int = 280, **kw):
        super().__init__(master, fg_color="transparent", **kw)
        self._max = 100
        self._atual = 100

        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x")
        self._lbl_titulo = ctk.CTkLabel(topo, text="HP", font=F_TINY, text_color=TEXTO2)
        self._lbl_titulo.pack(side="left")
        self._lbl_val = ctk.CTkLabel(topo, text="100 / 100", font=F_TINY, text_color=TEXTO2)
        self._lbl_val.pack(side="right")

        self._trilho = ctk.CTkFrame(self, fg_color=BG_CARD2,
                                    corner_radius=6, width=largura, height=14)
        self._trilho.pack(fill="x", pady=(3, 0))
        self._trilho.pack_propagate(False)

        self._fill = ctk.CTkFrame(self._trilho, fg_color=VERDE, corner_radius=6)
        self._fill.place(x=0, y=0, relheight=1.0, relwidth=1.0)

    def _cor(self) -> str:
        r = self._atual / self._max if self._max > 0 else 0
        if r > 0.5: return VERDE
        if r > 0.25: return AMARELO
        return VERMELHO

    def set(self, atual: int, maximo: int = None):
        if maximo is not None:
            self._max = maximo
        self._atual = max(0, min(atual, self._max))
        ratio = self._atual / self._max if self._max > 0 else 0
        self._fill.configure(fg_color=self._cor())
        self._fill.place(x=0, y=0, relheight=1.0, relwidth=ratio)
        self._lbl_val.configure(text=f"{self._atual} / {self._max}")

    def flash(self, cor: str = VERMELHO):
        """Pisca a barra com uma cor e volta à cor normal."""
        self._fill.configure(fg_color=cor)
        self.after(300, lambda: self._fill.configure(fg_color=self._cor()))

    def set_titulo(self, texto: str):
        self._lbl_titulo.configure(text=texto)


class TelaJogo(ctk.CTkFrame):
    """HUD de batalha completo com estética RPG."""

    # ─── Inicialização ────────────────────────────────────────────────────────

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback

        # Estado da partida
        self.modo_atual       = "Tabuada"
        self.dificuldade_atual = "Médio"
        self.sistema_pontos   = SistemaPontuacao("Médio")
        self.pergunta_atual   = None
        self.timer_id         = None
        self.limite_tempo     = 30
        self.tempo_restante   = 30
        self.tempo_total      = 0
        self.max_perguntas    = 10
        self.idx_pergunta     = 0
        self.acertos          = 0

        # HP do jogador e do inimigo (para o HUD)
        self._hp_heroi   = 100
        self._hp_inimigo = 100

        # ──────────────────────────────────────────────────────────────────────
        # TEORIA DOS CONJUNTOS:
        # 'perguntas_feitas' é inicializado aqui como conjunto vazio (∅).
        # Ao longo da partida, cada pergunta exibida é inserida neste conjunto.
        # A estrutura set() do Python garante unicidade (sem duplicatas),
        # implementando o conceito matemático de Conjunto.
        # ──────────────────────────────────────────────────────────────────────
        self.perguntas_feitas = set()

        self._criar_fundo()
        self._construir_hud()

    def _criar_fundo(self):
        """Fundo temático com símbolos matemáticos em ultra low opacity."""
        for _ in range(45):
            sym  = random.choice(SIMBOLOS_FUNDO)
            size = random.randint(14, 55)
            px   = random.uniform(0.01, 0.99)
            py   = random.uniform(0.01, 0.99)
            if 0.15 < px < 0.85 and 0.1 < py < 0.9:
                continue
            ctk.CTkLabel(self, text=sym,
                         font=("Segoe UI Black", size, "bold"),
                         text_color="#0C0F1A").place(relx=px, rely=py, anchor="center")

    # ─── Construção do HUD ────────────────────────────────────────────────────

    def _construir_hud(self):
        """Monta toda a interface do HUD de batalha."""

        # ── Topbar: Modo | Questão | Tempo | Sair ────────────────────────────
        topbar = ctk.CTkFrame(self, fg_color=BG_CARD,
                               corner_radius=0, height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        inner_top = ctk.CTkFrame(topbar, fg_color="transparent")
        inner_top.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.96)

        self.btn_sair = ctk.CTkButton(
            inner_top, text="✖ Abandonar",
            font=F_SMALL, text_color=VERMELHO,
            fg_color="transparent", hover_color="#1A0808",
            border_color=VERMELHO, border_width=1,
            width=110, height=30, corner_radius=CORNER,
            command=self._voltar
        )
        self.btn_sair.pack(side="left", padx=8)

        self.lbl_modo = ctk.CTkLabel(inner_top, text="MODO",
                                      font=F_H3, text_color=TEXTO)
        self.lbl_modo.pack(side="left", padx=16)

        self.lbl_dif = ctk.CTkLabel(inner_top, text="● Médio",
                                     font=F_SMALL, text_color=COR_MEDIO)
        self.lbl_dif.pack(side="left", padx=4)

        self.lbl_questao = ctk.CTkLabel(inner_top, text="0 / 10",
                                         font=F_H3, text_color=TEXTO2)
        self.lbl_questao.pack(side="left", padx=20)

        self.lbl_tempo = ctk.CTkLabel(inner_top, text="⏱ 30",
                                       font=F_TIMER, text_color=CIANO)
        self.lbl_tempo.pack(side="right", padx=16)

        self.lbl_pontos_top = ctk.CTkLabel(inner_top, text="⭐ 0",
                                            font=F_H2, text_color=AMARELO)
        self.lbl_pontos_top.pack(side="right", padx=16)

        # ── Barra de progresso da partida ─────────────────────────────────────
        self.barra_prog = ctk.CTkProgressBar(
            self, height=5, fg_color=BG_CARD2, progress_color=ROXO
        )
        self.barra_prog.pack(fill="x")
        self.barra_prog.set(0)

        # ── Área central (3 colunas) ──────────────────────────────────────────
        area = ctk.CTkFrame(self, fg_color="transparent")
        area.pack(fill="both", expand=True, padx=16, pady=10)

        # Coluna esquerda: painel do herói
        col_esq = ctk.CTkFrame(area, fg_color=BG_CARD,
                                corner_radius=CORNER_L,
                                border_width=1, border_color=BORDA,
                                width=200)
        col_esq.pack(side="left", fill="y", padx=(0, 10))
        col_esq.pack_propagate(False)
        self._construir_painel_heroi(col_esq)

        # Coluna central: pergunta e resposta
        col_mid = ctk.CTkFrame(area, fg_color="transparent")
        col_mid.pack(side="left", fill="both", expand=True, padx=10)
        self._construir_painel_pergunta(col_mid)

        # Coluna direita: painel do inimigo
        col_dir = ctk.CTkFrame(area, fg_color=BG_CARD,
                                corner_radius=CORNER_L,
                                border_width=1, border_color=BORDA,
                                width=200)
        col_dir.pack(side="right", fill="y", padx=(10, 0))
        col_dir.pack_propagate(False)
        self._construir_painel_inimigo(col_dir)

    def _construir_painel_heroi(self, pai):
        """Painel esquerdo: avatar do herói, HP e stats."""
        ctk.CTkLabel(pai, text="HERÓI",
                     font=F_TINY, text_color=TEXTO2).pack(pady=(16, 4))

        self.lbl_sprite_heroi = ctk.CTkLabel(pai, text="🧙",
                                              font=("Segoe UI", 48))
        self.lbl_sprite_heroi.pack()

        self.lbl_nome_heroi = ctk.CTkLabel(pai, text="...",
                                            font=F_H3, text_color=AZUL,
                                            wraplength=170)
        self.lbl_nome_heroi.pack(pady=(4, 10))

        self.barra_hp_heroi = BarraVida(pai, largura=160)
        self.barra_hp_heroi.set_titulo("❤️ HP do Herói")
        self.barra_hp_heroi.pack(padx=16, pady=(0, 16))

        sep = ctk.CTkFrame(pai, fg_color=BORDA, height=1)
        sep.pack(fill="x", padx=12, pady=8)

        ctk.CTkLabel(pai, text="STATUS DA PARTIDA",
                     font=F_TINY, text_color=TEXTO3).pack()

        self.lbl_acertos = ctk.CTkLabel(pai, text="✅  Acertos: 0",
                                         font=F_SMALL, text_color=VERDE)
        self.lbl_acertos.pack(pady=4)

        self.lbl_erros = ctk.CTkLabel(pai, text="❌  Erros: 0",
                                       font=F_SMALL, text_color=VERMELHO)
        self.lbl_erros.pack(pady=4)

        self.lbl_flash_heroi = ctk.CTkLabel(pai, text="",
                                             font=("Segoe UI Black", 20, "bold"),
                                             text_color=VERDE)
        self.lbl_flash_heroi.pack(pady=8)

    def _construir_painel_inimigo(self, pai):
        """Painel direito: sprite do inimigo, HP e nome."""
        ctk.CTkLabel(pai, text="INIMIGO",
                     font=F_TINY, text_color=TEXTO2).pack(pady=(16, 4))

        self.lbl_sprite_ini = ctk.CTkLabel(pai, text="👹",
                                            font=("Segoe UI", 48))
        self.lbl_sprite_ini.pack()

        self.lbl_nome_ini = ctk.CTkLabel(pai, text="...",
                                          font=F_H3, text_color=VERMELHO,
                                          wraplength=170)
        self.lbl_nome_ini.pack(pady=(4, 10))

        self.barra_hp_ini = BarraVida(pai, largura=160)
        self.barra_hp_ini.set_titulo("💀 HP do Inimigo")
        self.barra_hp_ini.pack(padx=16, pady=(0, 16))

        sep = ctk.CTkFrame(pai, fg_color=BORDA, height=1)
        sep.pack(fill="x", padx=12, pady=8)

        ctk.CTkLabel(pai, text="DANO POR ACERTO",
                     font=F_TINY, text_color=TEXTO3).pack()

        self.lbl_dano_ini = ctk.CTkLabel(pai, text="⚔️  10 HP",
                                          font=F_SMALL, text_color=AMARELO)
        self.lbl_dano_ini.pack(pady=4)

        self.lbl_flash_ini = ctk.CTkLabel(pai, text="",
                                           font=("Segoe UI Black", 20, "bold"),
                                           text_color=VERMELHO)
        self.lbl_flash_ini.pack(pady=8)

    def _construir_painel_pergunta(self, pai):
        """Coluna central: barra de tempo, pergunta, input e HUD inferior."""

        # Barra de tempo
        self.barra_tempo = ctk.CTkProgressBar(
            pai, height=8, fg_color=BG_CARD2, progress_color=CIANO
        )
        self.barra_tempo.pack(fill="x", pady=(0, 8))
        self.barra_tempo.set(1.0)

        # Card da pergunta
        card_q = ctk.CTkFrame(pai, fg_color=GLASS_BG,
                               corner_radius=CORNER_L,
                               border_width=2, border_color=ROXO)
        card_q.pack(fill="both", expand=True)
        self._card_pergunta = card_q

        # Faixa de cor no topo (igual ao Modo RPG)
        self.faixa_modo = ctk.CTkFrame(card_q, fg_color=ROXO, height=4, corner_radius=2)
        self.faixa_modo.pack(fill="x")

        # Cabeçalho do card
        cab_q = ctk.CTkFrame(card_q, fg_color="transparent")
        cab_q.pack(fill="x", padx=20, pady=(14, 0))

        self.lbl_titulo_modo_card = ctk.CTkLabel(
            cab_q, text="M O D O",
            font=("Segoe UI Black", 13), text_color=TEXTO2
        )
        self.lbl_titulo_modo_card.pack(side="left")

        self.lbl_combo_card = ctk.CTkLabel(
            cab_q, text="",
            font=("Segoe UI Black", 13), text_color=LARANJA
        )
        self.lbl_combo_card.pack(side="right")

        # Linha neon
        self.linha_modo = ctk.CTkFrame(card_q, fg_color=ROXO,
                                        height=2, corner_radius=2)
        self.linha_modo.pack(fill="x", padx=20)

        # Container central que agrupa pergunta + input + botão, centralizado
        # verticalmente (evita o vão grande entre a pergunta e a resposta).
        miolo = ctk.CTkFrame(card_q, fg_color="transparent")
        miolo.pack(expand=True)

        # Pergunta (fonte gigante)
        self.lbl_pergunta = ctk.CTkLabel(
            miolo, text="?",
            font=("Segoe UI Black", 66, "bold"), text_color=TEXTO,
            wraplength=560
        )
        self.lbl_pergunta.pack(pady=(0, 28))

        # Campo de resposta
        self.entrada = ctk.CTkEntry(
            miolo, font=("Segoe UI Black", 32, "bold"),
            width=360, height=66, justify="center",
            placeholder_text="Resposta...",
            text_color=AMARELO,
            fg_color=BG_INPUT,
            border_color=BORDA, border_width=2,
            corner_radius=CORNER
        )
        self.entrada.pack(pady=(0, 12))
        self.entrada.bind("<Return>", lambda _: self._verificar())

        # Botão confirmar
        self.btn_confirmar = ctk.CTkButton(
            miolo, text="⚡  ATACAR",
            font=("Segoe UI Bold", 19, "bold"), text_color=TEXTO,
            fg_color=ROXO, hover_color=ROXO_HOVER,
            width=360, height=54, corner_radius=CORNER,
            command=self._verificar
        )
        self.btn_confirmar.pack()

        # Feedback
        self.lbl_feedback = ctk.CTkLabel(
            pai, text="", font=F_H2
        )
        self.lbl_feedback.pack(pady=(6, 0))

    # ─── Configuração de Partida ──────────────────────────────────────────────

    def configurar_modo(self, modo: str, dificuldade: str = "Médio"):
        """
        Chamado pela tela de seleção antes de navegar para cá.
        Reinicia todos os contadores e inicia a primeira pergunta.
        """
        self.modo_atual        = modo
        self.dificuldade_atual = dificuldade
        self.sistema_pontos    = SistemaPontuacao(dificuldade)
        self.idx_pergunta      = 0
        self.acertos           = 0
        self.tempo_total       = 0
        self._hp_heroi         = 100
        self._hp_inimigo       = 100

        # ──────────────────────────────────────────────────────────────────────
        # TEORIA DOS CONJUNTOS — Reinicialização:
        # Cada nova partida começa com o conjunto vazio (∅).
        # Isso garante que o histórico de perguntas da partida anterior
        # não interfira na nova sessão.
        # ──────────────────────────────────────────────────────────────────────
        self.perguntas_feitas = set()

        # Escolhe inimigo aleatório conforme dificuldade (nome + sprite próprios)
        inimigo  = random.choice(INIMIGOS.get(dificuldade, INIMIGOS["Médio"]))
        nome_ini = inimigo["nome"]
        sprite   = inimigo["sprite"]

        # Atualiza topbar
        cor_dif = CORES_DIFIC.get(dificuldade, COR_MEDIO)
        cor_modo = CORES_MODO.get(modo, ROXO)
        self.lbl_modo.configure(text=f"⚔  {modo.upper()}")
        self.lbl_dif.configure(text=f"● {dificuldade}", text_color=cor_dif)
        self.linha_modo.configure(fg_color=cor_modo)

        # Tema do card central segue a cor do modo (faixa, borda e botão)
        self.faixa_modo.configure(fg_color=cor_modo)
        self._card_pergunta.configure(border_color=cor_modo)
        self.btn_confirmar.configure(fg_color=cor_modo,
                                     hover_color=clarear(cor_modo, -0.15))

        # Atualiza card
        self.lbl_titulo_modo_card.configure(
            text=" ".join(f"{modo.upper()} | {dificuldade.upper()}")
        )

        # Atualiza painel inimigo
        self.lbl_sprite_ini.configure(text=sprite)
        self.lbl_nome_ini.configure(text=nome_ini)
        self.barra_hp_ini.set(100, 100)
        self.lbl_flash_ini.configure(text="")

        # Atualiza painel herói
        nome = getattr(self.master, "usuario_logado_nome", None) or "Herói"
        self.lbl_nome_heroi.configure(text=nome)
        self.barra_hp_heroi.set(100, 100)
        self.lbl_flash_heroi.configure(text="")

        # Reinicia HUD
        self.barra_prog.set(0)
        self.lbl_pontos_top.configure(text="⭐ 0")
        self.lbl_acertos.configure(text="✅  Acertos: 0")
        self.lbl_erros.configure(text="❌  Erros: 0")
        self.lbl_combo_card.configure(text="")
        self.lbl_feedback.configure(text="")

        self._proxima_pergunta()

    # ─── Loop Principal ───────────────────────────────────────────────────────

    def _proxima_pergunta(self):
        """
        Avança para a próxima pergunta ou finaliza a partida.

        ──────────────────────────────────────────────────────────────────────
        LÓGICA BOOLEANA — Controle de Fluxo:
            P: "idx_pergunta >= max_perguntas"
            Se P = True  → finaliza partida (fim de jogo)
            Se P = False → continua o loop (próxima questão)

        Essa é a proposição booleana central do gameplay loop.
        ──────────────────────────────────────────────────────────────────────
        """
        if self.timer_id:
            self.after_cancel(self.timer_id)

        # LÓGICA BOOLEANA: verifica condição de parada
        if self.idx_pergunta >= self.max_perguntas:
            self._finalizar()
            return

        self.idx_pergunta += 1
        self.lbl_questao.configure(text=f"{self.idx_pergunta} / {self.max_perguntas}")
        self.barra_prog.set(self.idx_pergunta / self.max_perguntas)

        # ──────────────────────────────────────────────────────────────────────
        # TEORIA DOS CONJUNTOS + ANÁLISE COMBINATÓRIA:
        #
        # Objetivo: gerar uma pergunta que NÃO pertença ao conjunto de
        # perguntas já exibidas nesta partida.
        #
        # Seja Ω o espaço amostral de todas as perguntas possíveis (geradas
        # aleatoriamente pelo GeradorMatematico — Análise Combinatória).
        # Seja F ⊆ Ω o conjunto das perguntas já feitas (Teoria dos Conjuntos).
        #
        # Buscamos p ∈ (Ω \ F) — pertencente ao complemento de F em Ω.
        #
        # Operação de pertinência: "p ∉ F" verifica se a nova pergunta
        # já foi exibida. Complexidade O(1) no set do Python.
        # ──────────────────────────────────────────────────────────────────────
        tentativas = 0
        nova = None
        while tentativas < 20:
            candidata = GeradorMatematico.gerar(self.modo_atual, self.dificuldade_atual)

            # Operação de pertinência: candidata ∉ F ?
            if candidata["pergunta"] not in self.perguntas_feitas:
                nova = candidata
                # Adição ao conjunto: F ← F ∪ {candidata}
                self.perguntas_feitas.add(candidata["pergunta"])
                break
            tentativas += 1

        # Se esgotou tentativas, usa a última gerada (fallback)
        if nova is None:
            nova = candidata

        self.pergunta_atual = nova

        # Exibe a pergunta
        self.lbl_pergunta.configure(text=nova["pergunta"])
        self.entrada.configure(state="normal", border_color=BORDA)
        self.entrada.delete(0, "end")
        self.entrada.focus()
        self.lbl_feedback.configure(text="")
        self.lbl_combo_card.configure(text=self.sistema_pontos.get_nivel_combo())

        # Reinicia o timer
        self.tempo_restante = self.limite_tempo
        self._atualizar_timer()
        self.timer_id = self.after(1000, self._tick_tempo)

    def _tick_tempo(self):
        """Decrementa o timer e atualiza a barra visual."""
        self.tempo_restante -= 1
        self.tempo_total    += 1
        self._atualizar_timer()

        if self.tempo_restante <= 0:
            self._tempo_esgotado()
        else:
            self.timer_id = self.after(1000, self._tick_tempo)

    def _atualizar_timer(self):
        """Atualiza label e cor do timer conforme urgência."""
        # LÓGICA BOOLEANA: cor muda conforme condição de urgência
        if self.tempo_restante <= 5:
            cor = VERMELHO
        elif self.tempo_restante <= 10:
            cor = AMARELO
        else:
            cor = CIANO

        self.lbl_tempo.configure(text=f"⏱ {self.tempo_restante}", text_color=cor)
        self.barra_tempo.configure(progress_color=cor)
        self.barra_tempo.set(self.tempo_restante / self.limite_tempo)

    # ─── Verificação de Resposta ──────────────────────────────────────────────

    def _verificar(self):
        """
        Processa a resposta do jogador.

        ──────────────────────────────────────────────────────────────────────
        ÁLGEBRA BOOLEANA — Avaliação da Proposição de Acerto:
            P: "resposta_usuario == resposta_correta"

            P = True  (acerto):
                → chama SistemaPontuacao.registrar_acerto()   [Funções Mat.]
                → causa dano no inimigo (barra HP inimigo −10)
                → exibe feedback verde

            P = False (erro):
                → chama SistemaPontuacao.registrar_erro()
                → causa dano no herói (barra HP herói −10)
                → exibe feedback vermelho

        Essa avaliação booleana é o núcleo da lógica de jogo.
        ──────────────────────────────────────────────────────────────────────
        """
        # Guarda de reentrada: ignora clique se entrada desabilitada
        if self.entrada.cget("state") == "disabled":
            return

        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        resposta_usuario  = self.entrada.get().strip()
        resposta_correta  = self.pergunta_atual["resposta"]
        tempo_gasto       = self.limite_tempo - self.tempo_restante

        self.entrada.configure(state="disabled")

        # ── AVALIAÇÃO BOOLEANA CENTRAL ─────────────────────────────────────
        if resposta_usuario == resposta_correta:
            # ── P = True: ACERTO ──────────────────────────────────────────
            self.acertos += 1

            # FUNÇÕES MATEMÁTICAS: calcula pontos via função composta
            pts, mult = self.sistema_pontos.registrar_acerto(tempo_gasto)

            # Efeito visual: borda verde
            self.entrada.configure(border_color=VERDE)

            # Dano no inimigo: −10 HP por acerto
            self._hp_inimigo = max(0, self._hp_inimigo - 10)
            self.barra_hp_ini.set(self._hp_inimigo, 100)
            self.barra_hp_ini.flash(VERMELHO)
            self._flash_label(self.lbl_flash_ini, f"−10 💥", VERMELHO)

            # Cura leve do herói se combo alto
            if self.sistema_pontos.combo_atual >= 5:
                self._hp_heroi = min(100, self._hp_heroi + 5)
                self.barra_hp_heroi.set(self._hp_heroi, 100)
                self.barra_hp_heroi.flash(VERDE)
                self._flash_label(self.lbl_flash_heroi, "+5 ❤️", VERDE)

            # Feedback de pontuação
            extra = "🔥" if mult > 1.0 else "✨"
            self.lbl_feedback.configure(
                text=f"CORRETO! {extra} +{pts} pts", text_color=VERDE
            )
            self.lbl_pontos_top.configure(
                text=f"⭐ {self.sistema_pontos.pontos_totais:,}"
            )

        else:
            # ── P = False: ERRO ───────────────────────────────────────────
            self.sistema_pontos.registrar_erro()

            # Efeito visual: borda vermelha
            self.entrada.configure(border_color=VERMELHO)

            # Dano no herói: −10 HP por erro
            self._hp_heroi = max(0, self._hp_heroi - 10)
            self.barra_hp_heroi.set(self._hp_heroi, 100)
            self.barra_hp_heroi.flash(VERMELHO)
            self._flash_label(self.lbl_flash_heroi, "−10 💔", VERMELHO)

            self.lbl_feedback.configure(
                text=f"INCORRETO! ✗  Resposta: {resposta_correta}",
                text_color=VERMELHO
            )

        # Atualiza stats laterais
        erros = self.idx_pergunta - self.acertos
        self.lbl_acertos.configure(text=f"✅  Acertos: {self.acertos}")
        self.lbl_erros.configure(text=f"❌  Erros: {erros}")
        self.lbl_combo_card.configure(
            text=self.sistema_pontos.get_nivel_combo()
        )

        # Aguarda 1.5s e avança
        self.after(1500, self._proxima_pergunta)

    def _tempo_esgotado(self):
        """Tempo da questão esgotou: penaliza e avança."""
        self.entrada.configure(state="disabled", border_color=VERMELHO)
        self.sistema_pontos.registrar_erro()

        # Dano no herói por tempo esgotado
        self._hp_heroi = max(0, self._hp_heroi - 5)
        self.barra_hp_heroi.set(self._hp_heroi, 100)
        self.barra_hp_heroi.flash(VERMELHO)
        self._flash_label(self.lbl_flash_heroi, "−5 ⏰", VERMELHO)

        resp = self.pergunta_atual["resposta"]
        self.lbl_feedback.configure(
            text=f"⏰ Tempo! Era {resp}.", text_color=AMARELO
        )
        self.after(1500, self._proxima_pergunta)

    # ─── Finalização ──────────────────────────────────────────────────────────

    def _finalizar(self):
        """Salva a partida no banco e navega para a tela de resultados."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        uid = getattr(self.master, "usuario_logado_id", None)
        if uid:
            BancoDeDados.salvar_partida(
                usuario_id=uid,
                modo=self.modo_atual,
                pontos=self.sistema_pontos.pontos_totais,
                acertos=self.acertos,
                tempo=self.tempo_total
            )
            # Verifica conquistas gerais e de nível após salvar
            stats = BancoDeDados.obter_estatisticas_conquistas(uid)
            GerenciadorConquistas.verificar_pos_partida(uid, stats)
            dados = BancoDeDados.obter_dados_perfil(uid)
            if dados:
                GerenciadorConquistas.verificar_nivel(uid, dados[3])

        erros = self.idx_pergunta - self.acertos
        self.master.telas["resultados"].mostrar_resultados(
            pontos=self.sistema_pontos.pontos_totais,
            acertos=self.acertos,
            erros=erros,
            tempo=self.tempo_total,
            max_combo=self.sistema_pontos.combo_maximo
        )
        self.trocar_tela("resultados")

    # ─── Helpers visuais ──────────────────────────────────────────────────────

    def _flash_label(self, lbl, texto: str, cor: str):
        """Exibe um texto temporário num label e some após 900ms."""
        lbl.configure(text=texto, text_color=cor)
        self.after(900, lambda: lbl.configure(text=""))

    def _voltar(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.trocar_tela("selecao_modo")