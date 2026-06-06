import random

class GeradorMatematico:
    """
    =========================================================================
    MÓDULO DE GERAÇÃO PROCEDURAL (Análise Combinatória e Funções)
    =========================================================================
    Classe responsável por gerar todos os desafios matemáticos do jogo.
    Isolar esta lógica garante o princípio da Responsabilidade Única (SOLID).
    """
    
    @staticmethod
    def gerar_tabuada():
        fator_x = random.randint(1, 10)
        fator_y = random.randint(1, 10)
        
        pergunta = f"{fator_x} x {fator_y} = ?"
        resposta = str(fator_x * fator_y)
        
        return {"pergunta": pergunta, "resposta": resposta}

    @staticmethod
    def gerar_equacao_facil():
        # Já deixando um rascunho pronto para o Modo Equações do seu GDD!
        x = random.randint(1, 10)
        constante = random.randint(1, 10)
        resultado = x + constante
        
        pergunta = f"x + {constante} = {resultado}"
        resposta = str(x)
        
        return {"pergunta": pergunta, "resposta": resposta}