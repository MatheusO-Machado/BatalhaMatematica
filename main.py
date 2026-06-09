# =============================================================================
# BATALHA MATEMÁTICA — Ponto de Entrada da Aplicação
# Disciplina: Matemática Computacional Aplicada — 2026/1
# =============================================================================
# Padrão MVC:
#   main.py  →  Controlador raiz. Instancia todas as telas e gerencia a
#               navegação entre elas via dicionário de telas.
# =============================================================================

import customtkinter as ctk
from controllers.database import BancoDeDados

from screens.login       import TelaLogin
from screens.menu        import TelaMenu
from screens.selecao_modo import TelaSelecaoModo
from screens.game        import TelaJogo
from screens.resultados  import TelaResultados
from screens.ranking     import TelaRanking
from screens.perfil      import TelaPerfil
from screens.como_jogar  import TelaComoJogar
from screens.rpg         import TelaRPG


class BatalhaMatematicaApp(ctk.CTk):
    """
    Classe principal da aplicação.
    Gerencia o ciclo de vida das telas usando um dicionário como roteador.
    """

    def __init__(self):
        super().__init__()

        # ── Configuração da janela ────────────────────────────────────────────
        self.title("⚔️ Batalha Matemática RPG v2.0")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(fg_color="#080A12")

        # Centralizar na tela
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"1100x680+{(sw-1100)//2}+{(sh-680)//2}")

        # ── Inicializa banco de dados ─────────────────────────────────────────
        BancoDeDados.inicializar_banco()

        # ── Estado do jogador logado ──────────────────────────────────────────
        self.usuario_logado_id   = None
        self.usuario_logado_nome = None

        # ── Registro de todas as telas (Views) ────────────────────────────────
        self.telas = {
            "login":        TelaLogin(self, self.mostrar_tela),
            "menu":         TelaMenu(self, self.mostrar_tela),
            "selecao_modo": TelaSelecaoModo(self, self.mostrar_tela),
            "jogo":         TelaJogo(self, self.mostrar_tela),
            "resultados":   TelaResultados(self, self.mostrar_tela),
            "ranking":      TelaRanking(self, self.mostrar_tela),
            "perfil":       TelaPerfil(self, self.mostrar_tela),
            "como_jogar":   TelaComoJogar(self, self.mostrar_tela),
            "rpg":          TelaRPG(self, self.mostrar_tela),
        }

        self.tela_atual = None
        self.mostrar_tela("login")  # Sempre inicia no login

    def mostrar_tela(self, nome_tela: str):
        """
        Roteador de telas. Esconde a tela atual e exibe a solicitada.
        Chama métodos de atualização quando necessário (ex.: ranking, perfil).
        """
        if self.tela_atual is not None:
            self.tela_atual.pack_forget()

        self.tela_atual = self.telas[nome_tela]
        self.tela_atual.pack(fill="both", expand=True)

        # Telas que precisam recarregar dados ao serem exibidas
        if nome_tela in ("ranking", "perfil"):
            self.tela_atual.atualizar_tela()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = BatalhaMatematicaApp()
    app.mainloop()
