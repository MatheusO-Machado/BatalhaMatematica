# =============================================================================
# BATALHA MATEMÁTICA — Controller: Gerador Matemático
# =============================================================================
# Responsável pela geração procedural de questões matemáticas.
#
# MATEMÁTICA APLICADA — ANÁLISE COMBINATÓRIA:
#   O gerador cria um espaço amostral Ω de questões por modo e dificuldade.
#   Usando Análise Combinatória, os operandos são escolhidos por permutação
#   aleatória dentro de intervalos definidos (min_val, max_val), garantindo
#   variedade suficiente para que a mesma equação dificilmente se repita.
# =============================================================================

import random


class GeradorMatematico:
    """
    Fábrica de questões matemáticas.
    Cada método retorna um dict {"pergunta": str, "resposta": str}.
    """

    # Tabela de limites de operandos por dificuldade.
    # ANÁLISE COMBINATÓRIA: define o domínio (intervalo) dos operandos.
    LIMITES = {
        "Fácil":   (1,  5),
        "Médio":   (2,  12),
        "Difícil": (5,  25),
        "Extremo": (15, 99),
    }

    @staticmethod
    def gerar(modo: str, dificuldade: str = "Médio") -> dict:
        """
        Gera uma questão aleatória para o modo e dificuldade informados.

        ANÁLISE COMBINATÓRIA — Espaço Amostral por Dificuldade:
            Fácil   → operandos ∈ [1, 5]
            Médio   → operandos ∈ [2, 12]
            Difícil → operandos ∈ [5, 25]
            Extremo → operandos ∈ [15, 99]
        O aumento do intervalo expande |Ω| exponencialmente.
        """
        min_val, max_val = GeradorMatematico.LIMITES.get(dificuldade, (2, 12))

        geradores = {
            "Adição":         GeradorMatematico._adicao,
            "Subtração":      GeradorMatematico._subtracao,
            "Tabuada":        GeradorMatematico._tabuada,
            "Frações":        GeradorMatematico._fracoes,
            "Porcentagem":    GeradorMatematico._porcentagem,
            "Regra de Três":  GeradorMatematico._regra_de_tres,
            "Equações":       GeradorMatematico._equacoes,
            "Desafio Rápido": GeradorMatematico._desafio_rapido,
            "Jornada RPG":    GeradorMatematico._jornada_rpg,
        }
        gerador = geradores.get(modo, GeradorMatematico._tabuada)
        return gerador(min_val, max_val, dificuldade)

    # ─── Modos Básicos: Adição e Subtração ─────────────────────────────────────

    @staticmethod
    def _adicao(min_val: int, max_val: int, dif: str) -> dict:
        """
        FUNÇÕES MATEMÁTICAS — Adição: f(a,b) = a + b
        Em dificuldades altas, soma 3 parcelas para aumentar o desafio.
        ANÁLISE COMBINATÓRIA: escala os operandos para ampliar o espaço amostral.
        """
        escala = {"Fácil": 10, "Médio": 50, "Difícil": 200, "Extremo": 999}
        teto = escala.get(dif, 50)
        if dif in ("Difícil", "Extremo"):
            a, b, c = (random.randint(1, teto) for _ in range(3))
            return {"pergunta": f"{a} + {b} + {c}", "resposta": str(a + b + c)}
        a, b = random.randint(1, teto), random.randint(1, teto)
        return {"pergunta": f"{a} + {b}", "resposta": str(a + b)}

    @staticmethod
    def _subtracao(min_val: int, max_val: int, dif: str) -> dict:
        """
        FUNÇÕES MATEMÁTICAS — Subtração: f(a,b) = a - b  (com a >= b)
        LÓGICA BOOLEANA: garante a >= b para evitar resultados negativos
        nas dificuldades iniciais (troca a e b se necessário).
        """
        escala = {"Fácil": 10, "Médio": 50, "Difícil": 200, "Extremo": 999}
        teto = escala.get(dif, 50)
        a, b = random.randint(1, teto), random.randint(1, teto)
        # Proposição booleana: se b > a, inverte para manter resultado positivo
        if b > a:
            a, b = b, a
        return {"pergunta": f"{a} − {b}", "resposta": str(a - b)}

    # ─── Modos Existentes ───────────────────────────────────────────────────────

    @staticmethod
    def _tabuada(min_val: int, max_val: int, _dif: str) -> dict:
        """
        ANÁLISE COMBINATÓRIA — Produto Cartesiano:
            A = {min_val,...,max_val};  Ω = A × A;  |Ω| = (max-min+1)²
        """
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        return {"pergunta": f"{a} × {b}", "resposta": str(a * b)}

    @staticmethod
    def _fracoes(min_val: int, max_val: int, _dif: str) -> dict:
        """Divisão exata: numerador é múltiplo do denominador → resposta inteira."""
        den = random.randint(2, 10)
        num = den * random.randint(min_val, max_val)
        return {"pergunta": f"{num} ÷ {den}", "resposta": str(num // den)}

    @staticmethod
    def _porcentagem(min_val: int, max_val: int, dif: str) -> dict:
        """FUNÇÕES MATEMÁTICAS — Porcentagem: f(pct,val) = (pct/100) × val"""
        if dif in ("Fácil", "Médio"):
            pct = random.choice([10, 20, 25, 50])
            val = random.randint(1, 10) * 10
        else:
            pct = random.randint(1, 99)
            val = random.randint(10, 500)
        resp = int((pct / 100) * val)
        return {"pergunta": f"{pct}% de {val}", "resposta": str(resp)}

    @staticmethod
    def _regra_de_tres(min_val: int, max_val: int, _dif: str) -> dict:
        """Proporcionalidade direta: a/b = c/x → x = (b×c)/a (sempre inteiro)."""
        a = random.randint(2, max_val)
        b = a * random.randint(2, 10)
        c = random.randint(2, max_val)
        x = (b * c) // a
        return {"pergunta": f"{a} → {b}\n{c} → x", "resposta": str(x)}

    @staticmethod
    def _equacoes(min_val: int, max_val: int, _dif: str) -> dict:
        """
        FUNÇÕES MATEMÁTICAS — Equação Linear: ax + b = c → x = (c-b)/a
        LÓGICA BOOLEANA: se a == 1, omite o coeficiente por estética.
        """
        x = random.randint(min_val, max_val)
        a = random.randint(1, 5)
        b = random.randint(1, 20)
        c = (a * x) + b
        pergunta = f"x + {b} = {c}" if a == 1 else f"{a}x + {b} = {c}"
        return {"pergunta": pergunta, "resposta": str(x)}

    @staticmethod
    def _desafio_rapido(min_val: int, max_val: int, dif: str) -> dict:
        """Mix aleatório de modos básicos."""
        modos = ["Adição", "Subtração", "Tabuada", "Porcentagem", "Equações", "Frações"]
        return GeradorMatematico.gerar(random.choice(modos), dif)

    # ─── Modo RPG: Jornada do Herói ─────────────────────────────────────────────

    @staticmethod
    def dificuldade_por_fase(fase: int) -> str:
        """
        Mapeia a fase do RPG para uma dificuldade — DIFICULDADE GRADUAL.

        FUNÇÕES MATEMÁTICAS (função por partes / step function):
            d(fase) = Fácil    se fase ∈ [1, 3]
                      Médio    se fase ∈ [4, 7]
                      Difícil  se fase ∈ [8, 12]
                      Extremo  se fase >= 13
        A dificuldade cresce de forma monotônica com a fase.
        """
        if fase <= 3:
            return "Fácil"
        elif fase <= 7:
            return "Médio"
        elif fase <= 12:
            return "Difícil"
        return "Extremo"

    @staticmethod
    def _jornada_rpg(min_val: int, max_val: int, dif: str) -> dict:
        """
        Mistura TODOS os modos, incluindo adição e subtração.
        A dificuldade já vem calculada pela fase (dificuldade_por_fase).
        ANÁLISE COMBINATÓRIA: sorteia um modo do conjunto completo de modos.
        """
        modos = ["Adição", "Subtração", "Tabuada", "Frações",
                 "Porcentagem", "Regra de Três", "Equações"]
        return GeradorMatematico.gerar(random.choice(modos), dif)
