# =============================================================================
# BATALHA MATEMÁTICA — Controller: Sistema de Conquistas
# =============================================================================
# Define todas as conquistas do jogo e a lógica de verificação.
# Conquistas do Modo RPG são EXCLUSIVAS (só obtidas jogando a Jornada).
#
# MATEMÁTICA APLICADA:
#   - TEORIA DOS CONJUNTOS: conquistas do jogador são um conjunto;
#     a verificação usa diferença de conjuntos (novas = obtidas − já_tinha).
#   - LÓGICA BOOLEANA: cada conquista tem uma condição (proposição V/F).
# =============================================================================

from controllers.database import BancoDeDados


# ─── Catálogo de Conquistas ──────────────────────────────────────────────────
# Cada conquista: chave única, título, descrição, ícone e se é exclusiva do RPG.
CATALOGO = {
    # ── Conquistas GERAIS / Modo Clássico ──────────────────────────────────
    "pioneiro":   {"titulo": "Pioneiro",      "desc": "Complete sua 1ª partida",
                   "icone": "🌱", "rpg": False},
    "veterano":   {"titulo": "Veterano",      "desc": "Complete 10 partidas",
                   "icone": "⚔️", "rpg": False},
    "incansavel": {"titulo": "Incansável",    "desc": "Complete 50 partidas",
                   "icone": "🔁", "rpg": False},
    "lendario":   {"titulo": "Lenda Viva",    "desc": "Complete 100 partidas",
                   "icone": "🎖️", "rpg": False},
    "mestre":     {"titulo": "Mestre",        "desc": "Pontue mais de 500 numa partida",
                   "icone": "👑", "rpg": False},
    "imparavel":  {"titulo": "Imparável",     "desc": "Pontue mais de 1000 numa partida",
                   "icone": "💥", "rpg": False},
    "perfeito":   {"titulo": "Perfeição",     "desc": "Acerte todas as 10 questões numa partida",
                   "icone": "💯", "rpg": False},
    "perfeccionista": {"titulo": "Perfeccionista", "desc": "Faça 10 partidas perfeitas",
                   "icone": "🎯", "rpg": False},
    "algebrista": {"titulo": "Algebrista",    "desc": "Jogue 5 partidas de Equações",
                   "icone": "χ",  "rpg": False},
    "explorador": {"titulo": "Explorador",    "desc": "Jogue todos os 8 modos clássicos",
                   "icone": "🧭", "rpg": False},
    "centuriao":  {"titulo": "Centurião",     "desc": "Acerte 100 questões no total",
                   "icone": "🏹", "rpg": False},
    "milenar":    {"titulo": "Sábio Milenar", "desc": "Acerte 500 questões no total",
                   "icone": "📚", "rpg": False},
    "nivel10":    {"titulo": "Desperto",      "desc": "Alcance o nível 10",
                   "icone": "✨", "rpg": False},
    "nivel25":    {"titulo": "Iluminado",     "desc": "Alcance o nível 25",
                   "icone": "🌠", "rpg": False},
    "nivel50":    {"titulo": "Transcendente", "desc": "Alcance o nível 50",
                   "icone": "🔱", "rpg": False},

    # ── Conquistas EXCLUSIVAS do Modo RPG ───────────────────────────────────
    "rpg_inicio":  {"titulo": "A Jornada Começa", "desc": "Inicie sua 1ª Jornada RPG",
                    "icone": "🗺️", "rpg": True},
    "rpg_chefe1":  {"titulo": "Caçador de Chefes", "desc": "Derrote o 1º chefe (fase 5)",
                    "icone": "🛡️", "rpg": True},
    "rpg_fase10":  {"titulo": "Herói Lendário",    "desc": "Alcance a fase 10 do RPG",
                    "icone": "🏆", "rpg": True},
    "rpg_fase15":  {"titulo": "Conquistador",      "desc": "Alcance a fase 15 do RPG",
                    "icone": "💎", "rpg": True},
    "rpg_fase20":  {"titulo": "Semideus",          "desc": "Alcance a fase 20 do RPG",
                    "icone": "🌟", "rpg": True},
    "rpg_fase30":  {"titulo": "Imortal",           "desc": "Alcance a fase 30 do RPG",
                    "icone": "♾️", "rpg": True},
    "rpg_fase50":  {"titulo": "Divindade",         "desc": "Alcance a fase 50 do RPG",
                    "icone": "👑", "rpg": True},
    "rpg_chefe5":  {"titulo": "Matador de Lendas", "desc": "Derrote 5 chefes (fase 25)",
                    "icone": "⚔️", "rpg": True},
    "rpg_pontos":  {"titulo": "Aniquilador",       "desc": "Faça 3000 pontos numa Jornada",
                    "icone": "🔥", "rpg": True},
    "rpg_sobrevivente": {"titulo": "Sobrevivente", "desc": "Derrote 30 inimigos numa Jornada",
                    "icone": "🐺", "rpg": True},
}


class GerenciadorConquistas:
    """Verifica e desbloqueia conquistas baseado nas ações do jogador."""

    @staticmethod
    def verificar_pos_partida(usuario_id: int, stats: dict) -> list:
        """
        Verifica conquistas GERAIS após uma partida normal.
        Retorna lista de conquistas recém-desbloqueadas (para notificar o jogador).

        LÓGICA BOOLEANA: avalia a condição de cada conquista (proposição V/F).
        TEORIA DOS CONJUNTOS: só notifica as que ainda não estavam no conjunto.
        """
        novas = []

        # Mapa chave → proposição booleana de desbloqueio
        condicoes = {
            "pioneiro":       stats["total_partidas"] >= 1,
            "veterano":       stats["total_partidas"] >= 10,
            "incansavel":     stats["total_partidas"] >= 50,
            "lendario":       stats["total_partidas"] >= 100,
            "mestre":         stats["maior_pontuacao"] >= 500,
            "imparavel":      stats["maior_pontuacao"] >= 1000,
            "perfeito":       stats.get("partidas_perfeitas", 0) >= 1,
            "perfeccionista": stats.get("partidas_perfeitas", 0) >= 10,
            "algebrista":     stats["partidas_equacoes"] >= 5,
            "explorador":     stats.get("modos_distintos", 0) >= 8,
            "centuriao":      stats.get("total_acertos", 0) >= 100,
            "milenar":        stats.get("total_acertos", 0) >= 500,
        }

        for chave, condicao in condicoes.items():
            if condicao:  # proposição verdadeira
                if BancoDeDados.desbloquear_conquista(usuario_id, chave):
                    novas.append(CATALOGO[chave])

        return novas

    @staticmethod
    def verificar_nivel(usuario_id: int, nivel: int) -> list:
        """Conquistas de marcos de nível (10, 25, 50)."""
        novas = []
        marcos = {10: "nivel10", 25: "nivel25", 50: "nivel50"}
        for marco, chave in marcos.items():
            if nivel >= marco:
                if BancoDeDados.desbloquear_conquista(usuario_id, chave):
                    novas.append(CATALOGO[chave])
        return novas

    @staticmethod
    def verificar_rpg(usuario_id: int, fase_alcancada: int,
                      iniciou: bool = False, chefe_derrotado: bool = False,
                      pontos: int = 0, inimigos_derrotados: int = 0) -> list:
        """
        Verifica conquistas EXCLUSIVAS do Modo RPG.
        Estas só podem ser obtidas jogando a Jornada do Herói.

        FUNÇÕES (por partes): marcos de fase mapeiam para conquistas.
        """
        novas = []

        # Início da jornada
        if iniciou:
            if BancoDeDados.desbloquear_conquista(usuario_id, "rpg_inicio"):
                novas.append(CATALOGO["rpg_inicio"])

        # Primeiro chefe derrotado (fase 5)
        if chefe_derrotado and fase_alcancada >= 5:
            if BancoDeDados.desbloquear_conquista(usuario_id, "rpg_chefe1"):
                novas.append(CATALOGO["rpg_chefe1"])

        # Marcos de fase alcançada
        marcos_fase = {
            10: "rpg_fase10", 15: "rpg_fase15", 20: "rpg_fase20",
            25: "rpg_chefe5", 30: "rpg_fase30", 50: "rpg_fase50",
        }
        for fase_marco, chave in marcos_fase.items():
            if fase_alcancada >= fase_marco:
                if BancoDeDados.desbloquear_conquista(usuario_id, chave):
                    novas.append(CATALOGO[chave])

        # Marco de pontuação numa única jornada
        if pontos >= 3000:
            if BancoDeDados.desbloquear_conquista(usuario_id, "rpg_pontos"):
                novas.append(CATALOGO["rpg_pontos"])

        # Marco de inimigos derrotados numa jornada
        if inimigos_derrotados >= 30:
            if BancoDeDados.desbloquear_conquista(usuario_id, "rpg_sobrevivente"):
                novas.append(CATALOGO["rpg_sobrevivente"])

        return novas