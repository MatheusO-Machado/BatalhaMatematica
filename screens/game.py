import customtkinter as ctk
import random
from utils.pontuacao import SistemaPontuacao

COR_ROXO = "#7B2CBF"
COR_FUNDO = "#1E1E2E"
COR_VERDE = "#38B000"
COR_VERMELHO = "#D90429"
COR_AMARELO = "#FFBE0B"
COR_BRANCO = "#F8F9FA"

class TelaJogo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color="transparent")
        self.trocar_tela_callback = trocar_tela_callback
        
        self.sistema_pontos = SistemaPontuacao()
        self.pergunta_atual = None
        self.tempo_decorrido = 0
        self.timer_id = None
        
        # --- INTERFACE ---
        self.frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_topo.pack(fill="x", padx=20, pady=(20, 0))
        
        self.label_pontos = ctk.CTkLabel(self.frame_topo, text="Pontos: 0", font=("Arial", 20, "bold"), text_color=COR_BRANCO)
        self.label_pontos.pack(side="left")
        
        self.label_titulo = ctk.CTkLabel(self.frame_topo, text="MODO TABUADA", font=("Arial", 24, "bold"), text_color=COR_ROXO)
        self.label_titulo.pack(side="left", expand=True)
        
        self.label_tempo = ctk.CTkLabel(self.frame_topo, text="Tempo: 0s", font=("Arial", 20, "bold"), text_color=COR_AMARELO)
        self.label_tempo.pack(side="right")
        
        self.label_combo = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"), text_color=COR_AMARELO)
        self.label_combo.pack(pady=(10, 0))

        self.label_pergunta = ctk.CTkLabel(self, text="", font=("Arial", 54, "bold"))
        self.label_pergunta.pack(pady=30)
        
        self.entrada_resposta = ctk.CTkEntry(self, font=("Arial", 24), width=150, justify="center")
        self.entrada_resposta.pack(pady=10)
        self.entrada_resposta.bind("<Return>", lambda event: self.verificar_resposta())
        
        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 18, "bold"))
        self.label_feedback.pack(pady=10)
        
        self.btn_responder = ctk.CTkButton(self, text="RESPONDER", fg_color=COR_ROXO, font=("Arial", 16, "bold"), command=self.verificar_resposta)
        self.btn_responder.pack(pady=10)
        
        self.btn_voltar = ctk.CTkButton(self, text="VOLTAR", fg_color="transparent", border_color=COR_ROXO, border_width=2, command=self.voltar_menu)
        self.btn_voltar.pack(pady=20)

        self.proxima_pergunta()

    def gerar_pergunta_tabuada(self):
        """
        =========================================================================
        REQUISITO DA DISCIPLINA: Conjuntos e Funções / Análise Combinatória
        =========================================================================
        Em vez de ler de um banco de dados estático, geramos perguntas de forma 
        processual. 
        
        1. Conjuntos: Definimos o Domínio da nossa função sorteando elementos de 
           dois conjuntos finitos: A = {1, 2, ..., 10} e B = {1, 2, ..., 10}.
        2. Combinatória: O número total de arranjos possíveis com repetição para 
           este modo é 10 * 10 = 100 permutações diferentes de perguntas.
        3. Funções: Aplicamos a função f(x, y) = x * y para encontrar a Imagem (resultado).
        =========================================================================
        """
        fator_x = random.randint(1, 10)
        fator_y = random.randint(1, 10)
        
        pergunta = f"{fator_x} x {fator_y} = ?"
        resposta = str(fator_x * fator_y) # A resposta real computada no momento
        
        return {"pergunta": pergunta, "resposta": resposta}

    def atualizar_tempo(self):
        self.tempo_decorrido += 1
        self.label_tempo.configure(text=f"Tempo: {self.tempo_decorrido}s")
        self.timer_id = self.after(1000, self.atualizar_tempo)

    def proxima_pergunta(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            
        # Geração Procedural da Pergunta
        self.pergunta_atual = self.gerar_pergunta_tabuada()
        self.label_pergunta.configure(text=self.pergunta_atual["pergunta"])
        
        self.entrada_resposta.delete(0, 'end') 
        self.label_feedback.configure(text="")
        
        self.tempo_decorrido = 0
        self.label_tempo.configure(text="Tempo: 0s")
        self.timer_id = self.after(1000, self.atualizar_tempo)

    def verificar_resposta(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        resposta_usuario = self.entrada_resposta.get().strip()
        resposta_correta = self.pergunta_atual["resposta"]
        
        """
        =========================================================================
        REQUISITO DA DISCIPLINA: Uso de Lógica Booleana e Controle de Fluxo
        =========================================================================
        Aqui aplicamos Lógica Booleana para validar a entrada do usuário.
        Temos a proposição P: (resposta_usuario == resposta_correta).
        
        - Se P for Verdadeiro (True): O fluxo entra na condição de acerto,
          computando XP e Pontuação via funções matemáticas.
        - Se P for Falso (False): O fluxo entra na condição de erro, zerando
          os combos do jogador e pulando para a próxima pergunta.
        =========================================================================
        """
        if resposta_usuario == resposta_correta:
            pontos_ganhos, multiplicador = self.sistema_pontos.registrar_acerto(self.tempo_decorrido)
            self.label_pontos.configure(text=f"Pontos: {self.sistema_pontos.pontos_totais}")
            
            texto_combo = f"🔥 Combo {self.sistema_pontos.combo_atual}x" if self.sistema_pontos.combo_atual > 1 else ""
            if multiplicador > 1.0:
                texto_combo += f" ({multiplicador}x)"
            self.label_combo.configure(text=texto_combo)

            self.label_feedback.configure(text=f"✔️ +{pontos_ganhos} pts", text_color=COR_VERDE)
            
            # P