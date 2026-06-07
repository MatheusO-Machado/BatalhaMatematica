class SistemaPontuacao:
    def __init__(self, dificuldade="Médio"):
        self.pontos_totais = 0
        self.combo_atual = 0
        self.combo_maximo = 0

        # O Segredo do Balanceamento: Multiplicadores de Dificuldade
        multiplicadores = {
            "Fácil": 1.0,    # Pontos normais
            "Médio": 1.5,    # 50% a mais de pontos
            "Difícil": 2.0,  # O dobro de pontos
            "Extremo": 3.0   # O triplo de pontos!
        }
        self.multiplicador_dif = multiplicadores.get(dificuldade, 1.0)

    def registrar_acerto(self, tempo_gasto):
        self.combo_atual += 1
        if self.combo_atual > self.combo_maximo:
            self.combo_maximo = self.combo_atual

        # 1. Pontuação Base da Questão
        pontos_base = 50 

        # 2. Bônus de Velocidade (Mais rápido = mais pontos)
        bonus_tempo = max(0, 30 - tempo_gasto) * 2

        # 3. Multiplicador de Combo (ex: Combo 5 = bônus de 50%)
        mult_combo = 1.0 + (self.combo_atual * 0.1)

        # 4. CÁLCULO FINAL DA RODADA (Aplicando o bônus de Dificuldade)
        pontos_ganhos = int((pontos_base + bonus_tempo) * mult_combo * self.multiplicador_dif)
        
        self.pontos_totais += pontos_ganhos

        return pontos_ganhos, mult_combo

    def registrar_erro(self):
        self.combo_atual = 0