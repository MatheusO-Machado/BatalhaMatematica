import customtkinter as ctk
from utils.pontuacao import SistemaPontuacao
from utils.geradores import GeradorMatematico

# Paleta baseada nas suas imagens
COR_ROXO = "#7B2CBF"
COR_FUNDO = "#0D0E15" 
COR_VERDE = "#38B000"
COR_VERMELHO = "#D90429"
COR_AMARELO = "#FFBE0B"
COR_AZUL = "#3A86FF"
COR_BRANCO = "#F8F9FA"

class TelaJogo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback
        
        # --- SISTEMAS E DADOS DA PARTIDA ---
        self.sistema_pontos = SistemaPontuacao()
        self.pergunta_atual = None
        self.timer_id = None
        
        self.limite_tempo = 30
        self.tempo_restante = 30
        self.tempo_total_partida = 0 # Guarda o tempo de toda a jogatina
        
        self.max_perguntas = 10
        self.pergunta_atual_index = 0
        self.acertos = 0 # Rastreador de desempenho
        
        # --- INTERFACE: CABEÇALHO ---
        self.frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_topo.pack(fill="x", padx=40, pady=(20, 10))
        
        self.label_info = ctk.CTkLabel(self.frame_topo, text="Questão 0 de 10", font=("Arial", 14), text_color="#A0A0A0")
        self.label_info.pack(side="left")
        
        self.label_tempo = ctk.CTkLabel(self.frame_topo, text="⏱ 30s", font=("Arial", 18, "bold"), text_color=COR_BRANCO)
        self.label_tempo.pack(side="right")
        
        # --- BARRA DE PROGRESSO ---
        self.barra_progresso = ctk.CTkProgressBar(self, width=800, height=10, fg_color="#1E1E2E", progress_color=COR_ROXO)
        self.barra_progresso.pack(padx=40, pady=(0, 20))
        self.barra_progresso.set(0) # Inicia vazia
        
        # --- INTERFACE: ÁREA CENTRAL ---
        self.frame_central = ctk.CTkFrame(self, fg_color="#151722", corner_radius=15)
        self.frame_central.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.label_titulo_modo = ctk.CTkLabel(self.frame_central, text="Tabuada", font=("Arial", 16), text_color="#A0A0A0")
        self.label_titulo_modo.pack(pady=(30, 0))
        
        self.label_pergunta = ctk.CTkLabel(self.frame_central, text="", font=("Arial", 64, "bold"), text_color=COR_BRANCO)
        self.label_pergunta.pack(pady=30)
        
        self.entrada_resposta = ctk.CTkEntry(
            self.frame_central, font=("Arial", 24), width=300, height=50, 
            justify="center", placeholder_text="Digite sua resposta...", 
            fg_color="#0D0E15", border_color="#2A2D3E"
        )
        self.entrada_resposta.pack(pady=10)
        self.entrada_resposta.bind("<Return>", lambda event: self.verificar_resposta())
        
        self.btn_responder = ctk.CTkButton(
            self.frame_central, text="⚡ Responder", fg_color="transparent", 
            border_color="#2A2D3E", border_width=2, text_color=COR_BRANCO,
            font=("Arial", 16, "bold"), hover_color="#2A2D3E", command=self.verificar_resposta
        )
        self.btn_responder.pack(pady=10)

        self.label_feedback = ctk.CTkLabel(self.frame_central, text="", font=("Arial", 18, "bold"))
        self.label_feedback.pack(pady=5)
        
        # --- RODAPÉ ---
        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.pack(fill="x", padx=40, pady=(0, 20))
        
        self.label_combo = ctk.CTkLabel(self.frame_rodape, text="🔥 Combo: 0", font=("Arial", 14), text_color="#A0A0A0")
        self.label_combo.pack(side="left", padx=20)
        
        self.label_pontos = ctk.CTkLabel(self.frame_rodape, text="⭐ Pontos: 0", font=("Arial", 14), text_color="#A0A0A0")
        self.label_pontos.pack(side="left")

        # Inicia o loop
        self.proxima_pergunta()

    def atualizar_tempo(self):
        # Contagem Regressiva e Registro do Tempo Total
        self.tempo_restante -= 1
        self.tempo_total_partida += 1 
        
        # Muda a cor para vermelho se faltar 5 segundos
        cor = COR_VERMELHO if self.tempo_restante <= 5 else COR_BRANCO
        self.label_tempo.configure(text=f"⏱ {self.tempo_restante}s", text_color=cor)
        
        if self.tempo_restante <= 0:
            self.tempo_esgotado()
        else:
            self.timer_id = self.after(1000, self.atualizar_tempo)

    def tempo_esgotado(self):
        self.entrada_resposta.configure(state="disabled")
        self.sistema_pontos.registrar_erro()
        self.atualizar_textos_rodape()
        
        resposta_correta = self.pergunta_atual["resposta"]
        self.label_feedback.configure(text=f"Tempo esgotado! Era {resposta_correta}.", text_color=COR_VERMELHO)
        
        self.after(1500, self.proxima_pergunta)

    def proxima_pergunta(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            
        if self.pergunta_atual_index >= self.max_perguntas:
            self.finalizar_partida()
            return
            
        self.pergunta_atual_index += 1
        
        # Atualiza a interface superior
        self.label_info.configure(text=f"Questão {self.pergunta_atual_index} de {self.max_perguntas}")
        progresso = self.pergunta_atual_index / self.max_perguntas
        self.barra_progresso.set(progresso)
            
        # Gera e exibe a nova pergunta
        self.pergunta_atual = GeradorMatematico.gerar_tabuada()
        self.label_pergunta.configure(text=self.pergunta_atual["pergunta"])
        
        # Reseta os campos
        self.entrada_resposta.configure(state="normal")
        self.entrada_resposta.delete(0, 'end') 
        self.entrada_resposta.focus()
        self.label_feedback.configure(text="")
        
        # Reseta o timer para 30
        self.tempo_restante = self.limite_tempo
        self.label_tempo.configure(text=f"⏱ {self.tempo_restante}s", text_color=COR_BRANCO)
        self.timer_id = self.after(1000, self.atualizar_tempo)

    def verificar_resposta(self):
        if self.entrada_resposta.cget("state") == "disabled":
            return
            
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        resposta_usuario = self.entrada_resposta.get().strip()
        resposta_correta = self.pergunta_atual["resposta"]
        self.entrada_resposta.configure(state="disabled")
        
        # Calcula quanto tempo o jogador gastou para responder (para o bônus do GDD)
        tempo_gasto = self.limite_tempo - self.tempo_restante
        
        if resposta_usuario == resposta_correta:
            self.acertos += 1
            pontos_ganhos, mult = self.sistema_pontos.registrar_acerto(tempo_gasto)
            self.label_feedback.configure(text=f"Correto! +{pontos_ganhos} pts", text_color=COR_VERDE)
        else:
            self.sistema_pontos.registrar_erro()
            self.label_feedback.configure(text=f"Incorreto! Era {resposta_correta}.", text_color=COR_VERMELHO)
            
        self.atualizar_textos_rodape()
        self.after(1500, self.proxima_pergunta)

    def atualizar_textos_rodape(self):
        self.label_pontos.configure(text=f"⭐ Pontos: {self.sistema_pontos.pontos_totais}")
        self.label_combo.configure(text=f"🔥 Combo: {self.sistema_pontos.combo_atual}")

    def finalizar_partida(self):
        # Destrói a interface de jogo atual
        self.frame_topo.destroy()
        self.barra_progresso.destroy()
        self.frame_central.destroy()
        self.frame_rodape.destroy()
        
        # Cálculos de Desempenho
        desempenho_pct = int((self.acertos / self.max_perguntas) * 100)
        
        # Frase Motivacional dinâmica
        if desempenho_pct == 100:
            frase = "Perfeito! Você é um mestre da matemática! 🏆"
        elif desempenho_pct >= 70:
            frase = "Muito bem! Seu raciocínio está afiado! 🚀"
        elif desempenho_pct >= 40:
            frase = "Bom trabalho! Continue praticando para melhorar! 💪"
        else:
            frase = "Não desista! A prática leva à perfeição! 🎯"
            
        # --- TELA DE RESULTADOS ---
        label_resultado = ctk.CTkLabel(self, text="RESULTADO FINAL", font=("Arial", 36, "bold"), text_color=COR_BRANCO)
        label_resultado.pack(pady=(40, 10))
        
        label_frase = ctk.CTkLabel(self, text=frase, font=("Arial", 20), text_color="#A0A0A0")
        label_frase.pack(pady=(0, 40))
        
        # Container para os cards estatísticos
        frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.criar_card_resultado(frame_cards, "Acertos", f"{self.acertos}/{self.max_perguntas}", COR_VERDE, 0)
        self.criar_card_resultado(frame_cards, "Desempenho", f"{desempenho_pct}%", COR_AZUL, 1)
        self.criar_card_resultado(frame_cards, "Tempo", f"{self.tempo_total_partida}s", COR_ROXO, 2)
        self.criar_card_resultado(frame_cards, "Pontos", f"{self.sistema_pontos.pontos_totais}", COR_AMARELO, 3)
        frame_cards.pack(pady=10)

        # Botão de Voltar ao Menu
        btn_voltar = ctk.CTkButton(
            self, text="Voltar ao Menu Principal", fg_color=COR_ROXO, 
            font=("Arial", 16, "bold"), width=250, height=50,
            command=self.voltar_menu
        )
        btn_voltar.pack(pady=40)

    def criar_card_resultado(self, master, titulo, valor, cor, coluna):
        # Método auxiliar para desenhar os "quadrados" de resultados
        card = ctk.CTkFrame(master, fg_color="#151722", border_color=cor, border_width=1, corner_radius=10, width=120, height=120)
        card.grid(row=0, column=coluna, padx=10)
        card.pack_propagate(False) # Mantém o tamanho fixo
        
        lbl_valor = ctk.CTkLabel(card, text=valor, font=("Arial", 28, "bold"), text_color=cor)
        lbl_valor.pack(pady=(30, 5))
        
        lbl_titulo = ctk.CTkLabel(card, text=titulo, font=("Arial", 12), text_color="#A0A0A0")
        lbl_titulo.pack()

    def voltar_menu(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.trocar_tela_callback("menu")