class SistemaPontuacao:
    def __init__(self):
        self.pontos_totais = 0
        self.combo_atual = 0

    def registrar_acerto(self, tempo_segundos):
        pontos_base = 100
        
        # 1. Calcula o Bônus de Velocidade
        if tempo_segundos <= 3:
            bonus_velocidade = 100
        elif tempo_segundos <= 6:
            bonus_velocidade = 70
        elif tempo_segundos <= 10:
            bonus_velocidade = 40
        else:
            bonus_velocidade = 20
            
        # 2. Atualiza o Combo
        self.combo_atual += 1
        
        # 3. Aplica o Multiplicador
        multiplicador = 1.0
        if self.combo_atual >= 10:
            multiplicador = 2.0
        elif self.combo_atual >= 5:
            multiplicador = 1.5
        elif self.combo_atual >= 3:
            multiplicador = 1.2
            
        # 4. Fórmula Final: (Base + Bônus) * Multiplicador
        pontos_ganhos = int((pontos_base + bonus_velocidade) * multiplicador)
        self.pontos_totais += pontos_ganhos
        
        return pontos_ganhos, multiplicador

    def registrar_erro(self):
        # Quebra o combo se o jogador errar
        self.combo_atual = 0