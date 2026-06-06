import random

class GeradorMatematico:
    @staticmethod
    def gerar(modo, dificuldade="Médio"):

        """
        =====================================================================
        APLICAÇÃO MATEMÁTICA: ANÁLISE COMBINATÓRIA E ESTRUTURAS DISCRETAS
        =====================================================================
        Este método atua como um gerador de instâncias de problemas matemáticos.
        
        1. MODELAGEM: Cada modo de jogo (Tabuada, Frações, etc.) é tratado como um
           subconjunto de operações distintas dentro do domínio da matemática.
           
        2. ANÁLISE COMBINATÓRIA: Para evitar a trivialidade (repetição direta),
           utilizamos a permutação de elementos aleatórios dentro de ranges 
           específicos definidos pela variável 'dificuldade'. Isso garante que 
           o espaço amostral de possíveis questões seja vasto o suficiente 
           para proporcionar uma experiência única a cada rodada.
           
        3. CONTROLE BOOLEANO: A dificuldade altera os limites (ranges) dos 
           números gerados, aplicando uma função booleana interna que restringe 
           ou expande o domínio dos operandos.
        =====================================================================
        """
        
        # 1. Configura a escala de números com base na dificuldade
        if dificuldade == "Fácil":
            min_val, max_val = 1, 5
        elif dificuldade == "Médio":
            min_val, max_val = 2, 12
        elif dificuldade == "Difícil":
            min_val, max_val = 5, 25
        else: # Extremo
            min_val, max_val = 15, 99

        # 2. Gera a pergunta de acordo com o modo
        if modo == "Tabuada":
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            return {"pergunta": f"{a} x {b}", "resposta": str(a * b)}

        elif modo == "Frações":
            # Para não complicar a digitação, o jogo pede a resolução do inteiro da fração
            den = random.randint(2, 10)
            num = den * random.randint(min_val, max_val)
            return {"pergunta": f"{num} / {den}", "resposta": str(int(num/den))}

        elif modo == "Porcentagem":
            # Fáceis são números redondos, Difíceis são números quebrados
            pct = random.choice([10, 20, 25, 50]) if dificuldade in ["Fácil", "Médio"] else random.randint(1, 99)
            val = random.randint(1, 10) * 10 if dificuldade in ["Fácil", "Médio"] else random.randint(10, 500)
            resp = int((pct / 100) * val)
            return {"pergunta": f"{pct}% de {val}", "resposta": str(resp)}

        elif modo == "Regra de Três":
            a = random.randint(2, max_val)
            b = random.randint(2, 10) * a
            c = random.randint(2, max_val)
            resp = int((b * c) / a)
            return {"pergunta": f"{a} ➔ {b}\n{c} ➔ x", "resposta": str(resp)}

        elif modo == "Equações":
            x = random.randint(min_val, max_val)
            a = random.randint(1, 5)
            b = random.randint(1, 20)
            c = (a * x) + b
            if a == 1:
                return {"pergunta": f"x + {b} = {c}", "resposta": str(x)}
            return {"pergunta": f"{a}x + {b} = {c}", "resposta": str(x)}

        elif modo == "Desafio Rápido":
            modos_base = ["Tabuada", "Porcentagem", "Equações"]
            return GeradorMatematico.gerar(random.choice(modos_base), dificuldade)

        return {"pergunta": "2 + 2", "resposta": "4"}