import customtkinter as ctk
from utils.database import BancoDeDados

# Paleta de Cores Premium
COR_FUNDO = "#0B0C10" 
COR_ROXO = "#8A2BE2"
COR_BRANCO = "#FFFFFF"
COR_VERMELHO = "#D90429"
COR_VERDE = "#38B000"

class TelaLogin(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=COR_FUNDO)
        self.trocar_tela_callback = trocar_tela_callback
        
        self.modo_atual = "login" # Pode ser "login" ou "cadastro"

        # Painel Centralizado
        self.painel = ctk.CTkFrame(self, fg_color="#12131C", border_color="#1A1C29", border_width=2, corner_radius=20, width=400, height=500)
        self.painel.place(relx=0.5, rely=0.5, anchor="center")
        self.painel.pack_propagate(False) # Mantém o tamanho fixo

        # Cabeçalho
        self.label_icone = ctk.CTkLabel(self.painel, text="⚡", font=("Arial", 40))
        self.label_icone.pack(pady=(30, 10))
        
        self.label_titulo = ctk.CTkLabel(self.painel, text="A C E S S O", font=("Arial", 24, "bold"), text_color=COR_BRANCO)
        self.label_titulo.pack(pady=(0, 30))

        # Entradas de Texto (Inputs)
        self.entrada_usuario = ctk.CTkEntry(
            self.painel, font=("Arial", 16), width=280, height=45, 
            placeholder_text="Usuário", fg_color="#0B0C10", border_color="#2A2D3E"
        )
        self.entrada_usuario.pack(pady=(0, 15))

        self.entrada_senha = ctk.CTkEntry(
            self.painel, font=("Arial", 16), width=280, height=45, 
            placeholder_text="Senha", show="*", fg_color="#0B0C10", border_color="#2A2D3E" # show="*" oculta a senha
        )
        self.entrada_senha.pack(pady=(0, 5))

        # Feedback visual (Mensagens de erro ou sucesso)
        self.label_mensagem = ctk.CTkLabel(self.painel, text="", font=("Arial", 12), text_color=COR_VERMELHO)
        self.label_mensagem.pack(pady=(0, 15))

        # Botão Principal de Ação
        self.btn_acao = ctk.CTkButton(
            self.painel, text="ENTRAR", font=("Arial", 16, "bold"), fg_color=COR_ROXO, hover_color="#A349FF",
            width=280, height=45, corner_radius=10, command=self.processar_acao
        )
        self.btn_acao.pack(pady=(0, 20))

        # Alternador de Modo (Login <-> Cadastro)
        self.btn_alternar = ctk.CTkButton(
            self.painel, text="Não tem uma conta? Cadastre-se", font=("Arial", 12, "underline"), 
            fg_color="transparent", text_color="#A0A0A0", hover_color="#12131C", command=self.alternar_modo
        )
        self.btn_alternar.pack()

    def alternar_modo(self):
        """Troca os textos da interface dependendo se o usuário quer logar ou criar conta"""
        self.label_mensagem.configure(text="") # Limpa mensagens antigas
        
        if self.modo_atual == "login":
            self.modo_atual = "cadastro"
            self.label_titulo.configure(text="C A D A S T R O")
            self.btn_acao.configure(text="CRIAR CONTA")
            self.btn_alternar.configure(text="Já possui conta? Faça Login")
        else:
            self.modo_atual = "login"
            self.label_titulo.configure(text="A C E S S O")
            self.btn_acao.configure(text="ENTRAR")
            self.btn_alternar.configure(text="Não tem uma conta? Cadastre-se")

    def processar_acao(self):
        """Executa a chamada ao Banco de Dados dependendo do modo atual"""
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()

        # Validação básica
        if not usuario or not senha:
            self.label_mensagem.configure(text="Preencha todos os campos!", text_color=COR_VERMELHO)
            return

        if self.modo_atual == "cadastro":
            sucesso = BancoDeDados.cadastrar_usuario(usuario, senha)
            if sucesso:
                self.label_mensagem.configure(text="Conta criada! Faça login.", text_color=COR_VERDE)
                self.entrada_senha.delete(0, 'end')
                self.alternar_modo() # Volta para a tela de login
            else:
                self.label_mensagem.configure(text="Nome de usuário já existe.", text_color=COR_VERMELHO)
                
        elif self.modo_atual == "login":
            usuario_id = BancoDeDados.fazer_login(usuario, senha)
            if usuario_id:
                # Salva os dados na Sessão Global (no master / main.py)
                self.master.usuario_logado_id = usuario_id
                self.master.usuario_logado_nome = usuario
                
                # Limpa os campos para segurança e avança para o Menu
                self.entrada_usuario.delete(0, 'end')
                self.entrada_senha.delete(0, 'end')
                self.label_mensagem.configure(text="")
                
                self.trocar_tela_callback("menu")
            else:
                self.label_mensagem.configure(text="Usuário ou senha incorretos.", text_color=COR_VERMELHO)