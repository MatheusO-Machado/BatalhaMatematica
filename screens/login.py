# =============================================================================
# BATALHA MATEMÁTICA — View: Tela de Login
# =============================================================================
# Apresenta o formulário de login/cadastro.
# =============================================================================

import customtkinter as ctk
import random
from controllers.database import BancoDeDados
from screens.tema import *


class TelaLogin(ctk.CTkFrame):
    """Tela de entrada: login e cadastro de conta."""

    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color=BG_APP)
        self.trocar_tela = trocar_tela_callback
        self.modo_atual  = "login"   # "login" ou "cadastro"
        self._criar_fundo()
        self._construir()

    # ─── Fundo decorativo ─────────────────────────────────────────────────────

    def _criar_fundo(self):
        """Partículas matemáticas estáticas no fundo para atmosfera RPG."""
        for _ in range(30):
            sym  = random.choice(SIMBOLOS_FUNDO)
            size = random.randint(18, 72)
            px   = random.uniform(0.03, 0.97)
            py   = random.uniform(0.03, 0.97)
            # Evita centro da tela onde ficará o card
            if 0.25 < px < 0.75 and 0.15 < py < 0.85:
                continue
            ctk.CTkLabel(self, text=sym,
                         font=("Segoe UI Black", size, "bold"),
                         text_color=TEXTO3).place(relx=px, rely=py, anchor="center")

    # ─── Interface principal ──────────────────────────────────────────────────

    def _construir(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # ── Logo RPG ──────────────────────────────────────────────────────────
        ctk.CTkLabel(container, text="⚔️",
                     font=("Segoe UI", 54)).pack()
        ctk.CTkLabel(container, text="BATALHA",
                     font=F_TITLE, text_color=ROXO).pack()
        ctk.CTkLabel(container, text="MATEMÁTICA",
                     font=("Segoe UI Black", 26, "bold"),
                     text_color=TEXTO).pack()
        ctk.CTkLabel(container,
                     text="✦  Entre na Arena do Conhecimento  ✦",
                     font=F_SMALL, text_color=TEXTO2).pack(pady=(4, 24))

        # ── Card principal ────────────────────────────────────────────────────
        self.card = ctk.CTkFrame(
            container, fg_color=BG_CARD,
            border_color=BORDA, border_width=1,
            corner_radius=CORNER_L, width=420, height=370
        )
        self.card.pack()
        self.card.pack_propagate(False)

        inner = ctk.CTkFrame(self.card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=32, pady=28)

        # Usuário
        ctk.CTkLabel(inner, text="USUÁRIO", font=F_TINY,
                     text_color=TEXTO2).pack(anchor="w", pady=(0, 4))
        self.ent_user = ctk.CTkEntry(
            inner, font=F_BODY, height=44, corner_radius=CORNER,
            placeholder_text="⚔  Nome de herói",
            placeholder_text_color="#3A4060",
            fg_color=BG_INPUT, border_color=BORDA,
            border_width=1, text_color=TEXTO
        )
        self.ent_user.pack(fill="x", pady=(0, 12))

        # Senha
        ctk.CTkLabel(inner, text="SENHA", font=F_TINY,
                     text_color=TEXTO2).pack(anchor="w", pady=(0, 4))
        self.ent_senha = ctk.CTkEntry(
            inner, font=F_BODY, height=44, corner_radius=CORNER,
            placeholder_text="🔒  Palavra secreta", show="*",
            placeholder_text_color="#3A4060",
            fg_color=BG_INPUT, border_color=BORDA,
            border_width=1, text_color=TEXTO
        )
        self.ent_senha.pack(fill="x")
        self.ent_senha.bind("<Return>", lambda _: self._processar())

        # Mensagem de status
        self.lbl_msg = ctk.CTkLabel(inner, text="", font=F_SMALL,
                                     text_color=VERMELHO, height=20)
        self.lbl_msg.pack(fill="x", pady=(8, 8))

        # Botão principal
        self.btn_acao = ctk.CTkButton(
            inner, text="⚔  ENTRAR NA ARENA",
            font=F_H3, text_color=TEXTO,
            fg_color=ROXO, hover_color=ROXO_HOVER,
            height=46, corner_radius=CORNER,
            command=self._processar
        )
        self.btn_acao.pack(fill="x")

        # Botão secundário
        self.frame_sec = ctk.CTkFrame(inner, fg_color="transparent")
        self.frame_sec.pack(fill="x")

        self.btn_sec = ctk.CTkButton(
            self.frame_sec, text="✦  Criar Nova Conta",
            font=F_BODY, text_color=TEXTO,
            fg_color="transparent", hover_color=BG_CARD2,
            border_color=BORDA, border_width=1,
            height=40, corner_radius=CORNER,
            command=self._alternar
        )
        self.btn_sec.pack(fill="x", pady=(12, 0))

        # Botão voltar (fica oculto no modo login)
        self.btn_voltar = ctk.CTkButton(
            inner, text="← Voltar para o Login",
            font=("Segoe UI", 12, "underline"),
            text_color=TEXTO2,
            fg_color="transparent", hover_color=BG_CARD,
            command=self._alternar
        )

    # ─── Lógica de Alternância ────────────────────────────────────────────────

    def _alternar(self):
        """Alterna entre os modos login e cadastro, atualizando os rótulos."""
        self.lbl_msg.configure(text="")
        self.ent_senha.delete(0, "end")

        if self.modo_atual == "login":
            self.modo_atual = "cadastro"
            self.btn_acao.configure(text="✦  CRIAR CONTA DE HERÓI")
            self.frame_sec.pack_forget()
            self.btn_voltar.pack(pady=(10, 0))
            self.card.configure(height=370)
        else:
            self.modo_atual = "login"
            self.btn_acao.configure(text="⚔  ENTRAR NA ARENA")
            self.btn_voltar.pack_forget()
            self.frame_sec.pack(fill="x")
            self.card.configure(height=370)

    # ─── Processamento ────────────────────────────────────────────────────────

    def _processar(self):
        """
        LÓGICA BOOLEANA:
            Avalia (campo_vazio == True) → exibe erro.
            Avalia (login_valido == True) → navega para menu.
        """
        usuario = self.ent_user.get().strip()
        senha   = self.ent_senha.get().strip()

        # Proposição: campos preenchidos?
        if not usuario or not senha:
            self.lbl_msg.configure(
                text="⚠  Preencha todos os campos!", text_color=AMARELO)
            return

        if self.modo_atual == "cadastro":
            ok = BancoDeDados.cadastrar_usuario(usuario, senha)
            if ok:
                self.lbl_msg.configure(
                    text="✓  Conta criada! Faça login.", text_color=VERDE)
                self.ent_senha.delete(0, "end")
                self.after(1400, self._alternar)
            else:
                self.lbl_msg.configure(
                    text="✗  Este nome já existe. Tente outro.", text_color=VERMELHO)

        else:  # login
            uid = BancoDeDados.fazer_login(usuario, senha)
            if uid:
                # Proposição (login_ok == True): salva estado e navega
                self.master.usuario_logado_id   = uid
                self.master.usuario_logado_nome = usuario
                self.ent_user.delete(0, "end")
                self.ent_senha.delete(0, "end")
                self.lbl_msg.configure(text="")
                self.trocar_tela("menu")
            else:
                self.lbl_msg.configure(
                    text="✗  Usuário ou senha incorretos.", text_color=VERMELHO)
