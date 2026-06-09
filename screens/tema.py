# =============================================================================
# BATALHA MATEMÁTICA — Tema Visual RPG
# Paleta de cores, fontes e helpers compartilhados por todas as telas.
# =============================================================================

# ── Paleta Principal ──────────────────────────────────────────────────────────
BG_APP        = "#080A12"   # fundo raiz (quase preto azulado)
BG_CARD       = "#0F1320"   # cards e painéis
BG_CARD2      = "#141828"   # cards secundários / hover
BG_INPUT      = "#080A12"   # campos de entrada

BORDA         = "#1E2440"   # borda padrão
BORDA_NEON    = "#3D5AFE"   # borda destaque

TEXTO         = "#E8ECF8"   # texto principal
TEXTO2        = "#6B7494"   # texto secundário
TEXTO3        = "#2E3454"   # texto mudo (fundo decorativo)

# ── Cores de Ação ─────────────────────────────────────────────────────────────
ROXO          = "#7C3AED"   # ação primária (roxo RPG)
ROXO_HOVER    = "#6D28D9"
AZUL          = "#3D5AFE"   # destaque azul neon
CIANO         = "#00E5FF"   # energia / mana
VERDE         = "#00E676"   # acerto / vida
VERDE_DARK    = "#00C853"
VERMELHO      = "#FF1744"   # erro / dano
VERMELHO_DARK = "#D50000"
AMARELO       = "#FFD600"   # ouro / XP / pontos
LARANJA       = "#FF6D00"   # fogo / combo
ROSA          = "#F50057"   # crítico

# ── Cores de Dificuldade ─────────────────────────────────────────────────────
COR_FACIL    = "#00E676"
COR_MEDIO    = "#FFD600"
COR_DIFICIL  = "#FF6D00"
COR_EXTREMO  = "#FF1744"

CORES_DIFIC = {
    "Fácil":   COR_FACIL,
    "Médio":   COR_MEDIO,
    "Difícil": COR_DIFICIL,
    "Extremo": COR_EXTREMO,
}

# ── Cores do Pódio ───────────────────────────────────────────────────────────
OURO   = "#FFD700"
PRATA  = "#C0C0C0"
BRONZE = "#CD7F32"

# ── Fontes ───────────────────────────────────────────────────────────────────
F_GIANT  = ("Segoe UI Black", 64, "bold")
F_TITLE  = ("Segoe UI Black", 32, "bold")
F_H1     = ("Segoe UI Bold",  22, "bold")
F_H2     = ("Segoe UI Bold",  18, "bold")
F_H3     = ("Segoe UI Semibold", 14, "bold")
F_BODY   = ("Segoe UI", 13)
F_SMALL  = ("Segoe UI", 11)
F_TINY   = ("Segoe UI", 10)
F_MONO   = ("Consolas", 13)
F_QUESTION = ("Segoe UI Black", 52, "bold")
F_TIMER    = ("Segoe UI Black", 28, "bold")

# ── Constantes de Layout ─────────────────────────────────────────────────────
CORNER   = 12    # raio padrão de cantos
CORNER_L = 18    # raio grande

# ── Símbolos Decorativos ─────────────────────────────────────────────────────
SIMBOLOS_FUNDO = ["+", "−", "×", "÷", "=", "∑", "π", "√", "∞", "∫",
                  "x²", "f(x)", "Δ", "θ", "λ", "∀", "∃", "∈", "⊂", "ℝ"]

# ── Ícones de Modo ───────────────────────────────────────────────────────────
ICONES_MODO = {
    "Tabuada":        "✖",
    "Frações":        "◴",
    "Porcentagem":    "%",
    "Regra de Três":  "⚖️",
    "Equações":       "χ",
    "Desafio Rápido": "⚡",
}

CORES_MODO = {
    "Tabuada":        ROXO,
    "Frações":        AZUL,
    "Porcentagem":    VERDE,
    "Regra de Três":  AMARELO,
    "Equações":       VERMELHO,
    "Desafio Rápido": LARANJA,
}

# Gradientes simulados (cores de transição)
GRAD_TOPO    = "#12152A"
GRAD_MEIO    = "#0C0E1C"
GRAD_BAIXO   = "#080A12"

# Glassmorphism
GLASS_BG     = "#141A30"
GLASS_BORDA  = "#28304F"

# Cores extras vibrantes
TURQUESA     = "#1DE9B6"
MAGENTA      = "#E040FB"
INDIGO       = "#536DFE"
AMBAR        = "#FFC400"

# Ícones e cores do novo modo RPG
ICONES_MODO["Adição"]      = "➕"
ICONES_MODO["Subtração"]   = "➖"
ICONES_MODO["Jornada RPG"] = "🗺️"

CORES_MODO["Adição"]      = TURQUESA
CORES_MODO["Subtração"]   = INDIGO
CORES_MODO["Jornada RPG"] = MAGENTA
