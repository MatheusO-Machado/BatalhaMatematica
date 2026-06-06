import customtkinter as ctk
import json
import random
from utils.pontuacao import SistemaPontuacao 

# Paleta de cores
COR_ROXO = "#7B2CBF"
COR_FUNDO = "#1E1E2E"
COR_VERDE = "#38B000"
COR_VERMELHO = "#D90429"
COR_AMARELO = "#FFBE0B"

class TelaJogo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color="transparent")
        self.trocar_tela_callback = trocar_tela_callback
        
        # Sistemas do Jogo
        self.perguntas = self.carregar_perguntas()
        self.sistema_pontos = SistemaPontuacao() # Inicializa o sistema de pontos
        
        self.pergunta_atual = None
        self.tempo_decorrido = 0
        self.timer_id = None
        
        # --- INTERFACE ---
        # Frame superior para agrupar Pontos, Título e Tempo na mesma linha
        self.frame_topo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_topo.pack(fill="x", padx=20, pady=(20, 0))
        
        self.label_pontos = ctk.CTkLabel(self.frame_topo, text="Pontos: 0", font=("Arial", 20, "bold"), text_color=COR_BRANCO if 'COR_BRANCO' in globals() else "#F8F9FA")
        self.label_pontos.pack(side="left")
        
        self.label_titulo = ctk.CTkLabel(self.frame_topo, text="MODO TABUADA", font=("Arial", 24, "bold"), text_color=COR_ROXO)
        self.label_titulo.pack(side="left", expand=True)
        
        self.label_tempo = ctk.CTkLabel(self.frame_topo, text="Tempo: 0s", font=("Arial", 20, "bold"), text_color=COR_AMARELO)
        self.label_tempo.pack(side="right")
        
        # Elementos Centrais
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

    def carregar_perguntas(self):
        try:
            with open("perguntas/tabuada.json", "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            return [{"pergunta": "ERRO", "resposta": "0"}]

    def atualizar_tempo(self):
        self.tempo_decorrido += 1
        self.label_tempo.configure(text=f"Tempo: {self.tempo_decorrido}s")
        self.timer_id = self.after(1000, self.atualizar_tempo)

    def proxima_pergunta(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            
        self.pergunta_atual = random.choice(self.perguntas)
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
        
        if resposta_usuario == resposta_correta:
            # Chama o sistema de pontuação
            pontos_ganhos, multiplicador = self.sistema_pontos.registrar_acerto(self.tempo_decorrido)
            
            # Atualiza a interface
            self.label_pontos.configure(text=f"Pontos: {self.sistema_pontos.pontos_totais}")
            
            texto_combo = f"🔥 Combo {self.sistema_pontos.combo_atual}x" if self.sistema_pontos.combo_atual > 1 else ""
            if multiplicador > 1.0:
                texto_combo += f" (Multiplicador {multiplicador}x)"
            self.label_combo.configure(text=texto_combo)

            self.label_feedback.configure(text=f"✔️ +{pontos_ganhos} pts", text_color=COR_VERDE)
            self.after(1500, self.proxima_pergunta)
        else:
            # Reseta o combo
            self.sistema_pontos.registrar_erro()
            self.label_combo.configure(text="")
            
            self.label_feedback.configure(text="❌ INCORRETO! O combo foi zerado.", text_color=COR_VERMELHO)
            self.timer_id = self.after(1000, self.atualizar_tempo)
            self.entrada_resposta.delete(0, 'end')

    def voltar_menu(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.trocar_tela_callback("menu")