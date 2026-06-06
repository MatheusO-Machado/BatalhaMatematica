import customtkinter as ctk
import random
from utils.pontuacao import SistemaPontuacao
from utils.geradores import GeradorMatematico

# Paleta de Cores Premium (Dark Theme)
COR_FUNDO = "#0B0C10" 
COR_ROXO = "#8A2BE2"
COR_VERDE = "#38B000"
COR_VERMELHO = "#D90429"
COR_AMARELO = "#FFBE0B"
COR_AZUL = "#3A86FF"
COR_BRANCO = "#F8F9FA"

class BotaoAcao(ctk.CTkButton):
    """Botão com animação de levitação para a tela de jogo"""
    def __init__(self, master, cor_base, cor_hover, **kwargs):
        super().__init__(master, fg_color=cor_base, hover_color=cor_hover, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(cursor="hand2")
        self.pack_configure(pady=(15, 25))

    def on_leave(self, event):
        self.pack_configure(pady=20)

class TelaJogo(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback
        self.modo_atual = "Tabuada"
        
        self.sistema_pontos = SistemaPontuacao()
        self.pergunta_atual = None
        self.timer_id = None
        self.limite_tempo = 30
        self.tempo_restante = 30
        self.tempo_total_partida = 0 
        self.max_perguntas = 10
        self.pergunta_atual_index = 0
        self.acertos = 0 
        
        # Cria o fundo imersivo uma única vez
        self.criar_fundo_decorativo()
        
        # Container principal que segura a partida (facilita na hora de apagar tudo)
        self.container_jogo = ctk.CTkFrame(self, fg_color="transparent")
        self.container_jogo.pack(expand=True, fill="both")
        
        self.construir_interface_jogo()

    def criar_fundo_decorativo(self):
        """Fundo estilo Matrix, mas muito mais escuro para não distrair"""
        simbolos = ["+", "-", "x", "÷", "=", "∑", "π", "√", "∞", "∫", "x²", "f(x)"]
        cores_fundo = ["#0E0F14", "#101218"]
        
        for _ in range(40):
            simbolo = random.choice(simbolos)
            tamanho = random.randint(16, 60)
            cor = random.choice(cores_fundo)
            
            pos_x = random.uniform(0.02, 0.98)
            pos_y = random.uniform(0.02, 0.98)
            
            # Deixa o meio livre para a pergunta
            if 0.2 < pos_x < 0.8 and 0.2 < pos_y < 0.8:
                continue 

            ctk.CTkLabel(self, text=simbolo, font=("Arial", tamanho, "bold"), text_color=cor).place(relx=pos_x, rely=pos_y, anchor="center")

    def construir_interface_jogo(self):
        # Limpa apenas a interface do jogo (mantém o fundo)
        for widget in self.container_jogo.winfo_children():
            widget.destroy()

        # --- CABEÇALHO ---
        self.frame_topo = ctk.CTkFrame(self.container_jogo, fg_color="transparent")
        self.frame_topo.pack(fill="x", padx=60, pady=(30, 10))
        
        self.btn_sair = ctk.CTkButton(
            self.frame_topo, text="✖ Abandonar", font=("Arial", 14, "bold"), 
            fg_color="transparent", hover_color="#2A0808", text_color="#D90429", 
            width=60, border_color="#D90429", border_width=1, corner_radius=8, command=self.voltar_selecao
        )
        self.btn_sair.pack(side="left")
        
        # Bloco de Informação Centralizado
        frame_status = ctk.CTkFrame(self.frame_topo, fg_color="#12131C", corner_radius=10)
        frame_status.pack(side="left", padx=30, expand=True)
        
        self.label_info = ctk.CTkLabel(frame_status, text="Questão 0 de 10", font=("Arial", 14, "bold"), text_color="#A0A0A0")
        self.label_info.pack(side="left", padx=20, pady=5)
        
        self.label_tempo = ctk.CTkLabel(self.frame_topo, text="⏱ 30s", font=("Arial", 22, "bold"), text_color=COR_BRANCO)
        self.label_tempo.pack(side="right")
        
        # --- BARRA DE PROGRESSO ---
        self.barra_progresso = ctk.CTkProgressBar(self.container_jogo, width=800, height=8, fg_color="#1A1C29", progress_color=COR_ROXO)
        self.barra_progresso.pack(padx=60, pady=(0, 20))
        self.barra_progresso.set(0)
        
        # --- CARD PRINCIPAL (A Pergunta) ---
        self.frame_central = ctk.CTkFrame(self.container_jogo, fg_color="#12131C", border_color="#1A1C29", border_width=2, corner_radius=25, width=700, height=400)
        self.frame_central.pack(pady=10)
        self.frame_central.pack_propagate(False) # Mantém o tamanho do card fixo
        
        # Título do Modo com Linha Neon
       # Truque do Python para criar espaçamento entre as letras
        texto_espacado = " ".join(self.modo_atual.upper())
        self.label_titulo_modo = ctk.CTkLabel(self.frame_central, text=texto_espacado, font=("Arial", 18, "bold"), text_color="#A0A0A0")
        self.label_titulo_modo.pack(pady=(30, 5))
        ctk.CTkFrame(self.frame_central, fg_color=COR_ROXO, width=50, height=3, corner_radius=5).pack()
        
        self.label_pergunta = ctk.CTkLabel(self.frame_central, text="", font=("Arial", 80, "bold"), text_color=COR_BRANCO)
        self.label_pergunta.pack(expand=True)
        
        self.entrada_resposta = ctk.CTkEntry(
            self.frame_central, font=("Arial", 32, "bold"), width=350, height=65, 
            justify="center", placeholder_text="Resposta...", text_color=COR_AMARELO,
            fg_color="#0B0C10", border_color="#2A2D3E", border_width=2, corner_radius=15
        )
        self.entrada_resposta.pack(pady=10)
        self.entrada_resposta.bind("<Return>", lambda event: self.verificar_resposta())
        
        self.btn_responder = BotaoAcao(
            self.frame_central, cor_base=COR_ROXO, cor_hover="#A349FF",
            text="⚡ CONFIRMAR", text_color=COR_BRANCO, font=("Arial", 18, "bold"), 
            width=350, height=55, corner_radius=15, command=self.verificar_resposta
        )
        self.btn_responder.pack(pady=20)

        # --- RODAPÉ DE PONTUAÇÃO ---
        self.frame_rodape = ctk.CTkFrame(self.container_jogo, fg_color="transparent")
        self.frame_rodape.pack(fill="x", padx=60, pady=(20, 0))
        
        self.label_feedback = ctk.CTkLabel(self.frame_rodape, text="", font=("Arial", 22, "bold"))
        self.label_feedback.pack(side="top", pady=(0, 10))

        # Caixas de Combo e Pontos estilo HUD de jogo
        self.caixa_combo = ctk.CTkFrame(self.frame_rodape, fg_color="#12131C", corner_radius=8)
        self.caixa_combo.pack(side="left", padx=(0, 10))
        self.label_combo = ctk.CTkLabel(self.caixa_combo, text="🔥 Combo: 0", font=("Arial", 16, "bold"), text_color="#A0A0A0")
        self.label_combo.pack(padx=15, pady=8)
        
        self.caixa_pontos = ctk.CTkFrame(self.frame_rodape, fg_color="#12131C", corner_radius=8)
        self.caixa_pontos.pack(side="left")
        self.label_pontos = ctk.CTkLabel(self.caixa_pontos, text="⭐ Pontos: 0", font=("Arial", 16, "bold"), text_color=COR_AMARELO)
        self.label_pontos.pack(padx=15, pady=8)

    def configurar_modo(self, modo_selecionado):
        self.modo_atual = modo_selecionado
        self.sistema_pontos = SistemaPontuacao()
        self.pergunta_atual_index = 0
        self.acertos = 0
        self.tempo_total_partida = 0
        
        self.construir_interface_jogo()
        self.atualizar_textos_rodape()
        self.proxima_pergunta()

    def atualizar_tempo(self):
        self.tempo_restante -= 1
        self.tempo_total_partida += 1 
        
        cor = COR_VERMELHO if self.tempo_restante <= 5 else COR_BRANCO
        self.label_tempo.configure(text=f"⏱ {self.tempo_restante}s", text_color=cor)
        
        if self.tempo_restante <= 0:
            self.tempo_esgotado()
        else:
            self.timer_id = self.after(1000, self.atualizar_tempo)

    def piscar_caixa_texto(self, cor):
        self.entrada_resposta.configure(border_color=cor)
        self.after(800, lambda: self.entrada_resposta.configure(border_color="#2A2D3E"))

    def tempo_esgotado(self):
        self.entrada_resposta.configure(state="disabled")
        self.piscar_caixa_texto(COR_VERMELHO)
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
        self.label_info.configure(text=f"Questão {self.pergunta_atual_index} de {self.max_perguntas}")
        self.barra_progresso.set(self.pergunta_atual_index / self.max_perguntas)
            
        self.pergunta_atual = GeradorMatematico.gerar(self.modo_atual)
        self.label_pergunta.configure(text=self.pergunta_atual["pergunta"])
        
        self.entrada_resposta.configure(state="normal", border_color="#2A2D3E")
        self.entrada_resposta.delete(0, 'end') 
        self.entrada_resposta.focus()
        self.label_feedback.configure(text="")
        
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
        
        tempo_gasto = self.limite_tempo - self.tempo_restante
        
        if resposta_usuario == resposta_correta:
            self.acertos += 1
            self.piscar_caixa_texto(COR_VERDE) 
            pontos_ganhos, mult = self.sistema_pontos.registrar_acerto(tempo_gasto)
            
            # Efeito especial de feedback
            texto_extra = "🔥" if mult > 1.0 else "✨"
            self.label_feedback.configure(text=f"CORRETO! {texto_extra} +{pontos_ganhos} pts", text_color=COR_VERDE)
        else:
            self.sistema_pontos.registrar_erro()
            self.piscar_caixa_texto(COR_VERMELHO) 
            self.label_feedback.configure(text=f"INCORRETO! O certo era {resposta_correta}.", text_color=COR_VERMELHO)
            
        self.atualizar_textos_rodape()
        self.after(1500, self.proxima_pergunta)

    def atualizar_textos_rodape(self):
        self.label_pontos.configure(text=f"⭐ Pontos: {self.sistema_pontos.pontos_totais}")
        
        # Se o combo passar de 3, muda a cor para laranja neon para dar sensação de poder
        cor_combo = "#FF4500" if self.sistema_pontos.combo_atual >= 3 else "#A0A0A0"
        self.label_combo.configure(text=f"🔥 Combo: {self.sistema_pontos.combo_atual}x", text_color=cor_combo)

    
    # TELA FINAL PREMIUM 
    def finalizar_partida(self):
        # 1. Para os relógios do jogo
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
            
        # 2. Empacota os dados gerados pelo jogador
        estatisticas = {
            "modo": self.modo_atual,
            "acertos": self.acertos,
            "max_perguntas": self.max_perguntas,
            "tempo": self.tempo_total_partida,
            "pontos": self.sistema_pontos.pontos_totais
        }
        
        # 3. Envia os dados para a Tela de Resultados e faz a troca
        tela_resultados = self.master.telas["resultados"]
        tela_resultados.configurar_resultados(estatisticas)
        self.trocar_tela_callback("resultados")

    def criar_card_stat(self, master, titulo, valor, cor, coluna):
        card = ctk.CTkFrame(master, fg_color="#1A1F2E", corner_radius=15, width=120, height=110)
        card.grid(row=0, column=coluna, padx=10)
        card.pack_propagate(False) 
        
        ctk.CTkLabel(card, text=valor, font=("Arial", 26, "bold"), text_color=cor).pack(pady=(25, 5))
        ctk.CTkLabel(card, text=titulo, font=("Arial", 13), text_color="#A0A0A0").pack()

    def voltar_selecao(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.trocar_tela_callback("selecao_modo")