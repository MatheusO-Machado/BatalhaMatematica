import customtkinter as ctk
from controllers.database import BancoDeDados

# Importe a nova tela de Login aqui no topo!
from screens.login import TelaLogin
from screens.menu import TelaMenu
from screens.selecao_modo import TelaSelecaoModo
from screens.game import TelaJogo
from screens.resultados import TelaResultados
from screens.ranking import TelaRanking
from screens.perfil import TelaPerfil
from screens.como_jogar import TelaComoJogar

class BatalhaMatematicaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Batalha Matemática v1.0")
        self.geometry("1000x650")
        self.configure(fg_color="#0B0C10")
        
        BancoDeDados.inicializar_banco()
        
        self.usuario_logado_id = None
        self.usuario_logado_nome = None

        self.telas = {}
        
        # Adicione a Tela de Login ao dicionário de telas
        self.telas["login"] = TelaLogin(self, self.mostrar_tela)
        self.telas["menu"] = TelaMenu(self, self.mostrar_tela)
        self.telas["selecao_modo"] = TelaSelecaoModo(self, self.mostrar_tela)
        self.telas["jogo"] = TelaJogo(self, self.mostrar_tela)
        self.telas["resultados"] = TelaResultados(self, self.mostrar_tela)
        self.telas["ranking"] = TelaRanking(self, self.mostrar_tela)
        self.telas["perfil"] = TelaPerfil(self, self.mostrar_tela)
        self.telas["como_jogar"] = TelaComoJogar(self, self.mostrar_tela)

        self.tela_atual = None
        
        # MUDANÇA IMPORTANTE: O jogo agora começa na tela de login!
        self.mostrar_tela("login")

    def mostrar_tela(self, nome_tela):
        if self.tela_atual is not None:
            self.tela_forget = self.tela_atual.pack_forget()
            
        self.tela_atual = self.telas[nome_tela]
        self.tela_atual.pack(fill="both", expand=True)
        
        if nome_tela == "ranking":
            self.tela_atual.atualizar_tela()
        # ADICIONE ESTAS DUAS LINHAS:
        elif nome_tela == "perfil":
            self.tela_atual.atualizar_tela()

if __name__ == "__main__":
    app = BatalhaMatematicaApp()
    app.mainloop()