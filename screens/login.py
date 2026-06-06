import customtkinter as ctk
import random
from utils.database import BancoDeDados

COR_FUNDO_APP = "#0A0D14"       
COR_CARD = "#12151E"            
COR_BORDAS = "#222738"          
COR_INPUT_BG = "#0A0D14"        
COR_TEXTO_PRINCIPAL = "#FFFFFF" 
COR_TEXTO_SECUNDARIO = "#7E849E"
COR_BOTAO_PRIMARIO = "#1A1D29"  
COR_BOTAO_HOVER = "#2A2F42"     
COR_VERMELHO = "#D90429"
COR_VERDE = "#38B000"

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.trocar_tela_callback = trocar_tela_callback
        
        self.modo_atual = "login"

        # 1. FUNDO DECORATIVO
        self.criar_fundo_decorativo()

        # 2. CONTAINER PRINCIPAL
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.48, anchor="center")

        # --- CABEÇALHO DO APP ---
        self.label_icone = ctk.CTkLabel(self.main_container, text="🎮", font=("Arial", 46))
        self.label_icone.pack(pady=(0, 15))
        
        self.label_titulo_app = ctk.CTkLabel(self.main_container, text="Matemática", font=("Arial", 36, "bold"), text_color=COR_TEXTO_PRINCIPAL)
        self.label_titulo_app.pack()
        
        self.label_subtitulo = ctk.CTkLabel(self.main_container, text="✨ Entre na arena do conhecimento ✨", font=("Arial", 14), text_color=COR_TEXTO_SECUNDARIO)
        self.label_subtitulo.pack(pady=(0, 30))

        # --- CARD DE LOGIN ---
        self.card = ctk.CTkFrame(self.main_container, fg_color=COR_CARD, border_color=COR_BORDAS, border_width=1, corner_radius=15, width=420)
        self.card.pack()
        self.card.pack_propagate(False) 
        
        # Altura encurtada devido à remoção dos elementos extras
        self.card.configure(height=360)

        self.inner_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.inner_frame.pack(fill="both", expand=True, padx=35, pady=30)

        # --- INPUT: USUÁRIO ---
        self.lbl_user = ctk.CTkLabel(self.inner_frame, text="Usuário", font=("Arial", 12, "bold"), text_color=COR_TEXTO_SECUNDARIO)
        self.lbl_user.pack(anchor="w", pady=(0, 5))
        
        self.entrada_usuario = ctk.CTkEntry(
            self.inner_frame, font=("Arial", 14), height=45, corner_radius=8,
            placeholder_text="👤   Digite seu nome de usuário", placeholder_text_color="#4F5569",
            fg_color=COR_INPUT_BG, border_color=COR_BORDAS, border_width=1, text_color=COR_TEXTO_PRINCIPAL
        )
        self.entrada_usuario.pack(fill="x", pady=(0, 15))

        # --- INPUT: SENHA ---
        self.lbl_senha = ctk.CTkLabel(self.inner_frame, text="Senha", font=("Arial", 12, "bold"), text_color=COR_TEXTO_SECUNDARIO)
        self.lbl_senha.pack(anchor="w", pady=(0, 5))
        
        self.entrada_senha = ctk.CTkEntry(
            self.inner_frame, font=("Arial", 14), height=45, corner_radius=8, show="*",
            placeholder_text="🔒   Digite sua senha", placeholder_text_color="#4F5569",
            fg_color=COR_INPUT_BG, border_color=COR_BORDAS, border_width=1, text_color=COR_TEXTO_PRINCIPAL
        )
        self.entrada_senha.pack(fill="x")

        # --- MENSAGEM DE ERRO/SUCESSO ---
        self.label_mensagem = ctk.CTkLabel(self.inner_frame, text="", font=("Arial", 12), text_color=COR_VERMELHO, height=20)
        self.label_mensagem.pack(fill="x", pady=(10, 10))

        # --- BOTÃO PRINCIPAL AÇÃO ---
        self.btn_acao = ctk.CTkButton(
            self.inner_frame, text="Entrar", font=("Arial", 15, "bold"), text_color=COR_TEXTO_PRINCIPAL,
            fg_color=COR_BOTAO_PRIMARIO, hover_color=COR_BOTAO_HOVER, height=45, corner_radius=8,
            command=self.processar_acao
        )
        self.btn_acao.pack(fill="x")

        self.frame_botoes_secundarios = ctk.CTkFrame(self.inner_frame, fg_color="transparent")
        
        self.btn_criar_conta = ctk.CTkButton(
            self.frame_botoes_secundarios, text="Criar Conta", font=("Arial", 13, "bold"), text_color=COR_TEXTO_PRINCIPAL,
            fg_color="transparent", hover_color=COR_BOTAO_HOVER, border_color=COR_BORDAS, border_width=1, height=40, corner_radius=8,
            command=self.alternar_modo
        )
        # O botão agora preenche todo o espaço horizontal, mantendo a simetria
        self.btn_criar_conta.pack(fill="x", pady=(15, 0))

        self.frame_botoes_secundarios.pack(fill="x") 

        # --- BOTÃO VOLTAR AO LOGIN ---
        self.btn_voltar_login = ctk.CTkButton(
            self.inner_frame, text="← Voltar para o Login", font=("Arial", 12, "underline"), text_color=COR_TEXTO_SECUNDARIO,
            fg_color="transparent", hover_color=COR_CARD, command=self.alternar_modo
        )

    def criar_fundo_decorativo(self):
        elementos = ["7", "3", "9", "2", "4", "1", "+", "-", "x", "∑", "θ", "√n", "∞", "∫"]
        for _ in range(25): 
            texto = random.choice(elementos)
            tamanho = random.randint(20, 70)
            
            pos_x = random.uniform(0.05, 0.95)
            pos_y = random.uniform(0.05, 0.95)
            if 0.3 < pos_x < 0.7 and 0.2 < pos_y < 0.8:
                continue 

            lbl = ctk.CTkLabel(self, text=texto, font=("Arial", tamanho, "bold"), text_color="#141824")
            lbl.place(relx=pos_x, rely=pos_y, anchor="center")

    def alternar_modo(self):
        self.label_mensagem.configure(text="")
        self.entrada_senha.delete(0, 'end')
        
        if self.modo_atual == "login":
            self.modo_atual = "cadastro"
            self.label_titulo_app.configure(text="Criar Conta")
            self.label_subtitulo.configure(text="✨ Junte-se à arena do conhecimento ✨")
            self.btn_acao.configure(text="Cadastrar Nova Conta")
            
            self.frame_botoes_secundarios.pack_forget()
            
            self.btn_voltar_login.pack(pady=(15, 0))
            self.card.configure(height=360) 
            
        else:
            self.modo_atual = "login"
            self.label_titulo_app.configure(text="Matemática")
            self.label_subtitulo.configure(text="✨ Entre na arena do conhecimento ✨")
            self.btn_acao.configure(text="Entrar")
            
            self.btn_voltar_login.pack_forget()
            
            self.frame_botoes_secundarios.pack(fill="x")
            self.card.configure(height=360)

    def processar_acao(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()

        if not usuario or not senha:
            self.label_mensagem.configure(text="Preencha todos os campos!", text_color=COR_VERMELHO)
            return

        if self.modo_atual == "cadastro":
            sucesso = BancoDeDados.cadastrar_usuario(usuario, senha)
            if sucesso:
                self.label_mensagem.configure(text="Conta criada! Faça login.", text_color=COR_VERDE)
                self.entrada_senha.delete(0, 'end')
                self.after(1500, self.alternar_modo)
            else:
                self.label_mensagem.configure(text="Este nome de usuário já existe.", text_color=COR_VERMELHO)
                
        elif self.modo_atual == "login":
            usuario_id = BancoDeDados.fazer_login(usuario, senha)
            if usuario_id:
                self.master.usuario_logado_id = usuario_id
                self.master.usuario_logado_nome = usuario
                
                self.entrada_usuario.delete(0, 'end')
                self.entrada_senha.delete(0, 'end')
                self.label_mensagem.configure(text="")
                
                self.trocar_tela_callback("menu")
            else:
                self.label_mensagem.configure(text="Usuário ou senha incorretos.", text_color=COR_VERMELHO)