import random

class GeradorMatematico:
    """
    =========================================================================
    MÓDULO DE GERAÇÃO PROCEDURAL UNIVERSAL
    =========================================================================
    Aplica conceitos de Álgebra, Proporcionalidade e Análise Combinatória 
    para gerar desafios infinitos e dinâmicos para todos os modos do jogo.
    =========================================================================
    """

    @staticmethod
    def gerar(modo):
        # Lógica Booleana de Roteamento
        if modo == "Tabuada":
            return GeradorMatematico.gerar_tabuada()
        elif modo == "Frações":
            return GeradorMatematico.gerar_fracoes()
        elif modo == "Porcentagem":
            return GeradorMatematico.gerar_porcentagem()
        elif modo == "Regra de Três":
            return GeradorMatematico.gerar_regra_tres()
        elif modo == "Equações":
            return GeradorMatematico.gerar_equacoes()
        elif modo == "Desafio Rápido":
            # Probabilidade: Sorteia uniformemente entre as 5 categorias
            modos_disponiveis = ["Tabuada", "Frações", "Porcentagem", "Regra de Três", "Equações"]
            sorteio = random.choice(modos_disponiveis)
            return GeradorMatematico.gerar(sorteio)
        else:
            return GeradorMatematico.gerar_tabuada()

    @staticmethod
    def gerar_tabuada():
        fator_x = random.randint(1, 10)
        fator_y = random.randint(1, 10)
        return {
            "pergunta": f"{fator_x} x {fator_y} = ?",
            "resposta": str(fator_x * fator_y)
        }

    @staticmethod
    def gerar_fracoes():
        # Para facilitar a digitação da resposta, mantemos denominadores iguais
        denominador = random.randint(2, 10)
        num1 = random.randint(1, denominador - 1)
        num2 = random.randint(1, denominador - 1)
        soma = num1 + num2
        
        # Se a soma for igual ou divisível pelo denominador, a resposta é um número inteiro
        if soma % denominador == 0:
            resposta = str(soma // denominador)
        else:
            resposta = f"{soma}/{denominador}"
            
        return {
            "pergunta": f"{num1}/{denominador} + {num2}/{denominador} = ?",
            "resposta": resposta
        }

    @staticmethod
    def gerar_porcentagem():
        # Cálculos percentuais exatos para o jogador responder mentalmente
        pct = random.choice([10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
        valor_base = random.randint(1, 20) * 10  # Gera valores de 10 a 200
        
        resultado = int((pct / 100) * valor_base)
        return {
            "pergunta": f"{pct}% de {valor_base} = ?",
            "resposta": str(resultado)
        }

    @staticmethod
    def gerar_regra_tres():
        """ 
        Garante que a razão seja inteira: Se A = B, C = X  -->  X = (B * C) / A 
        Criamos B como múltiplo de A para que o resultado X seja sempre inteiro.
        """
        multiplicador = random.randint(2, 10)
        A = random.randint(2, 10)
        B = A * multiplicador
        C = random.randint(2, 10)
        X = C * multiplicador
        
        return {
            "pergunta": f"Se {A} vale {B},\n{C} vale... ?",
            "resposta": str(X)
        }

    @staticmethod
    def gerar_equacoes():
        """ 
        Álgebra Linear Básica: Ax + B = C 
        O sistema sorteia X primeiro para garantir que a equação tenha solução exata.
        """
        A = random.randint(1, 5)
        X = random.randint(1, 10)
        B = random.randint(1, 20)
        C = (A * X) + B
        
        if A == 1:
            pergunta = f"x + {B} = {C}"
        else:
            pergunta = f"{A}x + {B} = {C}"
            
        return {
            "pergunta": pergunta,
            "resposta": str(X)
        }