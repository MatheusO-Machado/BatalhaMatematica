# =============================================================================
# BATALHA MATEMÁTICA — Controller: Motor do Modo RPG
# =============================================================================
# Lógica das fases progressivas, chefes, recompensas e DANOS CRÍTICOS.
#
# REGRAS DO MODO:
#   - Fases progressivas infinitas com dificuldade GRADUAL.
#   - A cada 5 fases (5, 10, 15...) há um CHEFE (boss) mais forte.
#   - Cada fase tem um inimigo a derrotar; cada acerto causa dano.
#   - O Herói tem HP. Erros e tempo esgotado causam dano.
#   - Desbloqueado apenas no nível 10.
#
# DANO CRÍTICO:
#   - HERÓI: ao acertar 3 perguntas seguidas, o próximo golpe é CRÍTICO
#     (dano dobrado). O contador de acertos seguidos reinicia após o crítico.
#   - INIMIGO: ao errar 3 ou mais vezes seguidas, o inimigo desfere um
#     contra-ataque CRÍTICO, proporcional à dificuldade e se for chefe.
#
# MATEMÁTICA APLICADA:
#   - FUNÇÕES (progressão): HP do inimigo e dano crescem por funções da fase.
#   - LÓGICA BOOLEANA: detecção de chefe (fase % 5 == 0) e de crítico
#     (sequência de acertos/erros >= 3).
#   - ANÁLISE COMBINATÓRIA: nomes/sprites de inimigos sorteados de conjuntos.
# =============================================================================

import random
from controllers.geradores import GeradorMatematico


# ─── Bestiário expandido (inimigos variados por dificuldade) ─────────────────
# Cada inimigo tem nome + sprite (emoji) próprios para dar variedade visual.
INIMIGOS_COMUNS = {
    "Fácil": [
        {"nome": "Slime Aritmético", "sprite": "🟢"},
        {"nome": "Goblin Iniciante", "sprite": "👺"},
        {"nome": "Morcego Somador",  "sprite": "🦇"},
        {"nome": "Rato das Cavernas","sprite": "🐀"},
        {"nome": "Cogumelo Saltitante","sprite": "🍄"},
    ],
    "Médio": [
        {"nome": "Orc Multiplicador", "sprite": "👹"},
        {"nome": "Esqueleto Veloz",   "sprite": "💀"},
        {"nome": "Harpia Divisória",  "sprite": "🦅"},
        {"nome": "Lobo Selvagem",     "sprite": "🐺"},
        {"nome": "Aranha Gigante",    "sprite": "🕷️"},
    ],
    "Difícil": [
        {"nome": "Golem de Pedra",        "sprite": "🗿"},
        {"nome": "Necromante Fracionário","sprite": "🧙"},
        {"nome": "Quimera Algébrica",     "sprite": "🦁"},
        {"nome": "Serpente Abissal",      "sprite": "🐍"},
        {"nome": "Gárgula Sombria",       "sprite": "🦇"},
    ],
    "Extremo": [
        {"nome": "Demônio do Caos",   "sprite": "😈"},
        {"nome": "Espectro Infinito", "sprite": "👻"},
        {"nome": "Aberração Numérica","sprite": "👾"},
        {"nome": "Ceifador das Trevas","sprite": "☠️"},
        {"nome": "Hidra Multiforme",  "sprite": "🐲"},
    ],
}

CHEFES = [
    {"nome": "Rei Goblin",          "sprite": "👑"},
    {"nome": "Dragão Ancião",       "sprite": "🐉"},
    {"nome": "Lich Supremo",        "sprite": "💀"},
    {"nome": "Senhor do Caos",      "sprite": "👹"},
    {"nome": "Devorador de Mundos", "sprite": "🛸"},
    {"nome": "Titã Primordial",     "sprite": "⚡"},
]

# Multiplicador de dano crítico do inimigo conforme a dificuldade da fase.
# FUNÇÕES: mapeia dificuldade → fator de crítico (cresce com a dificuldade).
FATOR_CRIT_INIMIGO = {
    "Fácil":   1.5,
    "Médio":   1.8,
    "Difícil": 2.2,
    "Extremo": 2.6,
}

# Nº de acertos/erros seguidos para disparar crítico.
SEQUENCIA_CRITICA = 3


class FaseRPG:
    """Representa uma fase do Modo RPG com seu inimigo e parâmetros."""

    def __init__(self, numero: int):
        self.numero = numero
        self.dificuldade = GeradorMatematico.dificuldade_por_fase(numero)

        # LÓGICA BOOLEANA: é fase de chefe? (a cada 5 fases)
        self.eh_chefe = (numero % 5 == 0)

        if self.eh_chefe:
            # Seleciona chefe ciclicamente conforme o nº de chefes já enfrentados
            idx = ((numero // 5) - 1) % len(CHEFES)
            chefe = CHEFES[idx]
            self.nome_inimigo = chefe["nome"]
            self.sprite = chefe["sprite"]
            # FUNÇÕES: HP do chefe = 60 + 25 × fase (cresce linearmente)
            self.hp_inimigo = 60 + 25 * numero
            # Chefes exigem mais acertos
            self.dano_por_acerto = 15
        else:
            inimigo = random.choice(
                INIMIGOS_COMUNS.get(self.dificuldade, INIMIGOS_COMUNS["Médio"])
            )
            self.nome_inimigo = inimigo["nome"]
            self.sprite = inimigo["sprite"]
            # FUNÇÕES: HP do inimigo comum = 30 + 8 × fase
            self.hp_inimigo = 30 + 8 * numero
            self.dano_por_acerto = 20

        # Dano que o inimigo causa no herói por erro (cresce com a fase)
        # FUNÇÕES: dano = 8 + floor(fase / 3)
        self.dano_no_heroi = 8 + (numero // 3)

    def gerar_pergunta(self) -> dict:
        """Gera uma pergunta do RPG na dificuldade atual da fase."""
        return GeradorMatematico.gerar("Jornada RPG", self.dificuldade)

    def dano_critico_inimigo(self) -> int:
        """
        Calcula o dano do contra-ataque CRÍTICO do inimigo.

        FUNÇÕES MATEMÁTICAS — proporcional à dificuldade e ao tipo (chefe):
            crit = dano_base × fator(dificuldade) × (1.5 se chefe senão 1)
        """
        fator = FATOR_CRIT_INIMIGO.get(self.dificuldade, 1.8)
        bonus_chefe = 1.5 if self.eh_chefe else 1.0
        return int(self.dano_no_heroi * fator * bonus_chefe)

    def recompensa_xp(self) -> int:
        """
        FUNÇÕES MATEMÁTICAS — Recompensa por completar a fase:
            xp(fase) = 50 × fase × (3 se chefe senão 1)
        Chefes valem o triplo de XP.
        """
        base = 50 * self.numero
        return base * 3 if self.eh_chefe else base


class MotorRPG:
    """
    Gerencia o estado completo de uma jornada no Modo RPG.
    Controla HP do herói, fase atual, pontuação, progressão e CRÍTICOS.
    """

    HP_MAX_HEROI = 120

    def __init__(self):
        self.fase_numero = 1
        self.hp_heroi = self.HP_MAX_HEROI
        self.pontos = 0
        self.acertos_totais = 0
        self.erros_totais = 0
        self.fase = FaseRPG(1)
        self.hp_inimigo_atual = self.fase.hp_inimigo
        self.inimigos_derrotados = 0

        # Contadores de sequência para a mecânica de crítico
        self.acertos_seguidos = 0
        self.erros_seguidos = 0

    # ─── Combate ──────────────────────────────────────────────────────────────

    def acertar(self, bonus_combo: float = 1.0) -> dict:
        """
        Processa um acerto: causa dano no inimigo e concede pontos.
        Pode aplicar DANO CRÍTICO do herói (3 acertos seguidos).
        Retorna dict com o resultado completo.
        """
        self.acertos_totais += 1
        self.acertos_seguidos += 1
        self.erros_seguidos = 0   # acertou → zera a sequência de erros

        # LÓGICA BOOLEANA: crítico do herói a cada 3 acertos seguidos
        eh_critico = (self.acertos_seguidos >= SEQUENCIA_CRITICA)

        dano = self.fase.dano_por_acerto
        if eh_critico:
            dano *= 2                     # dano dobrado no crítico
            self.acertos_seguidos = 0     # reinicia a sequência após o crítico

        self.hp_inimigo_atual = max(0, self.hp_inimigo_atual - dano)

        # FUNÇÕES: pontos = 20 × fase × bonus_combo (×2 se crítico)
        ganho = int(20 * self.fase_numero * bonus_combo * (2 if eh_critico else 1))
        self.pontos += ganho

        resultado = {
            "dano_causado": dano,
            "critico": eh_critico,
            "pontos_ganhos": ganho,
            "inimigo_derrotado": False,
            "avancou_fase": False,
            "xp_ganho": 0,
            "acertos_seguidos": self.acertos_seguidos,
        }

        # LÓGICA BOOLEANA: inimigo morreu? (hp <= 0)
        if self.hp_inimigo_atual <= 0:
            resultado["inimigo_derrotado"] = True
            self.inimigos_derrotados += 1
            resultado["xp_ganho"] = self.fase.recompensa_xp()
            self.pontos += resultado["xp_ganho"]
            self._avancar_fase()
            resultado["avancou_fase"] = True

        return resultado

    def errar(self) -> dict:
        """
        Processa um erro: o inimigo contra-ataca o herói.
        Pode aplicar CONTRA-ATAQUE CRÍTICO (3+ erros seguidos).
        """
        self.erros_totais += 1
        self.erros_seguidos += 1
        self.acertos_seguidos = 0   # errou → zera a sequência de acertos

        # LÓGICA BOOLEANA: crítico do inimigo a partir de 3 erros seguidos
        eh_critico = (self.erros_seguidos >= SEQUENCIA_CRITICA)

        if eh_critico:
            dano = self.fase.dano_critico_inimigo()
        else:
            dano = self.fase.dano_no_heroi

        self.hp_heroi = max(0, self.hp_heroi - dano)
        return {
            "dano_recebido": dano,
            "critico": eh_critico,
            "heroi_morreu": self.hp_heroi <= 0,
            "erros_seguidos": self.erros_seguidos,
        }

    def tempo_esgotado(self) -> dict:
        """
        Tempo acabou: conta como erro (alimenta a sequência de erros)
        mas com dano reduzido. Também pode escalar para crítico.
        """
        self.erros_seguidos += 1
        self.acertos_seguidos = 0
        eh_critico = (self.erros_seguidos >= SEQUENCIA_CRITICA)

        if eh_critico:
            dano = self.fase.dano_critico_inimigo() // 2
        else:
            dano = max(3, self.fase.dano_no_heroi // 2)

        self.hp_heroi = max(0, self.hp_heroi - dano)
        return {
            "dano_recebido": dano,
            "critico": eh_critico,
            "heroi_morreu": self.hp_heroi <= 0,
            "erros_seguidos": self.erros_seguidos,
        }

    def _avancar_fase(self):
        """Cria a próxima fase e restaura parte do HP do herói."""
        self.fase_numero += 1
        self.fase = FaseRPG(self.fase_numero)
        self.hp_inimigo_atual = self.fase.hp_inimigo
        # Cura de 15 HP ao avançar (recompensa de sobrevivência)
        self.hp_heroi = min(self.HP_MAX_HEROI, self.hp_heroi + 15)
        # Ao trocar de inimigo, as sequências de crítico reiniciam
        self.acertos_seguidos = 0
        self.erros_seguidos = 0

    # ─── Estado ───────────────────────────────────────────────────────────────

    @property
    def heroi_vivo(self) -> bool:
        return self.hp_heroi > 0

    @property
    def golpes_para_critico(self) -> int:
        """Quantos acertos faltam para o próximo crítico do herói."""
        return max(0, SEQUENCIA_CRITICA - self.acertos_seguidos)

    def gerar_pergunta(self) -> dict:
        return self.fase.gerar_pergunta()
