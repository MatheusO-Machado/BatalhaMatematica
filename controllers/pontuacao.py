# =============================================================================
# BATALHA MATEMÁTICA — Controller: Sistema de Pontuação
# =============================================================================
# Responsável por todo o cálculo de pontos, combos e multiplicadores.
#
# MATEMÁTICA APLICADA:
#
# 1. FUNÇÕES MATEMÁTICAS (Obrigatório — 5 pts):
#    A pontuação final de cada rodada é calculada por uma função composta:
#
#       f(base, tempo, combo, dif) = (base + g(tempo)) × h(combo) × k(dif)
#
#    Onde:
#       base        = 50 pts fixos por acerto
#       g(tempo)    = max(0, 30 - tempo_gasto) × 2   → bônus de velocidade
#       h(combo)    = 1.0 + (combo_atual × 0.1)       → multiplicador de combo
#       k(dif)      = {Fácil:1.0, Médio:1.5, Difícil:2.0, Extremo:3.0}
#
# 2. ANÁLISE COMBINATÓRIA (Escolha adicional — 5 pts):
#    O multiplicador de combo cresce progressivamente a cada acerto
#    consecutivo, formando uma progressão aritmética de razão 0.1.
#    Após n acertos seguidos: h(n) = 1.0 + 0.1n
#    Essa função representa a soma de uma P.A. aplicada ao multiplicador.
#
# 3. LÓGICA BOOLEANA:
#    O método registrar_erro() zera o combo usando atribuição condicional
#    implícita: combo_atual ← 0 (proposição: "errou == True").
# =============================================================================


class SistemaPontuacao:
    """
    Motor de pontuação da partida.
    Encapsula pontos totais, combo atual e cálculo de bônus.
    """

    def __init__(self, dificuldade: str = "Médio"):
        self.pontos_totais = 0
        self.combo_atual   = 0
        self.combo_maximo  = 0

        # ── MATEMÁTICA: Multiplicadores de Dificuldade ────────────────────────
        # k: {Fácil, Médio, Difícil, Extremo} → ℝ⁺
        # É uma função que mapeia cada dificuldade a um fator real positivo.
        # "Extremo" concede 3× mais pontos que "Fácil" — risco vs. recompensa.
        self._multiplicadores = {
            "Fácil":   1.0,
            "Médio":   1.5,
            "Difícil": 2.0,
            "Extremo": 3.0,
        }
        self.mult_dificuldade = self._multiplicadores.get(dificuldade, 1.0)

    # ─── Registro de Acerto ───────────────────────────────────────────────────

    def registrar_acerto(self, tempo_gasto: float) -> tuple[int, float]:
        """
        Processa um acerto e retorna (pontos_ganhos, multiplicador_combo).

        FUNÇÕES MATEMÁTICAS — Cálculo da Pontuação (f composta):

            Passo 1 — Base fixa:
                pontos_base = 50

            Passo 2 — Bônus de velocidade g(t):
                g(t) = max(0, 30 - t) × 2
                Quanto menor o tempo gasto (t), maior o bônus.
                g é uma função linear decrescente, limitada inferiormente por 0.

            Passo 3 — Multiplicador de combo h(n):
                h(n) = 1.0 + (n × 0.1)   onde n = acertos consecutivos
                Progressão Aritmética: cada acerto adiciona 0.1 ao multiplicador.
                Após 5 combos: h(5) = 1.5 → 50% de bônus sobre a pontuação.

            Passo 4 — Multiplicador de dificuldade k:
                k ∈ {1.0, 1.5, 2.0, 3.0}

            Passo 5 — Resultado final (função composta):
                pontos = int((pontos_base + g(t)) × h(n) × k)
        """
        # Incrementa o combo (contador de acertos consecutivos)
        self.combo_atual += 1
        if self.combo_atual > self.combo_maximo:
            self.combo_maximo = self.combo_atual

        # Passo 1: pontuação base
        pontos_base = 50

        # Passo 2: bônus de velocidade — g(t) = max(0, 30 - t) × 2
        bonus_velocidade = max(0, 30 - tempo_gasto) * 2

        # Passo 3: multiplicador de combo — h(n) = 1.0 + n × 0.1
        mult_combo = 1.0 + (self.combo_atual * 0.1)

        # Passo 5: função composta final
        pontos_ganhos = int(
            (pontos_base + bonus_velocidade) * mult_combo * self.mult_dificuldade
        )

        self.pontos_totais += pontos_ganhos
        return pontos_ganhos, mult_combo

    # ─── Registro de Erro ─────────────────────────────────────────────────────

    def registrar_erro(self):
        """
        LÓGICA BOOLEANA:
            Se (resposta_errada == True) → combo_atual ← 0
        Zera o combo, penalizando sequências interrompidas.
        """
        self.combo_atual = 0

    # ─── Utilitários ──────────────────────────────────────────────────────────

    def get_nivel_combo(self) -> str:
        """Retorna o título do combo atual para exibição visual."""
        if self.combo_atual >= 10:
            return "👑 LENDÁRIO"
        elif self.combo_atual >= 7:
            return "💀 IMPARÁVEL"
        elif self.combo_atual >= 5:
            return "🔥 DEVASTADOR"
        elif self.combo_atual >= 3:
            return "⚡ COMBO"
        return ""
