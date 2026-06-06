import customtkinter as ctk
from screens.menu import TelaMenu
from screens.selecao_modo import TelaSelecaoModo
from screens.game import TelaJogo
from screens.resultados import TelaResultados

class BatalhaMatematicaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da Janela (Aumentei um pouco para caber os cartões)
        self.title("Batalha Matemática v1.0")
        self.geometry("1000x650")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#0B0C10")
        
        # Dicionário de Telas
        self.telas = {}
        
        # Inicializando todas as telas
        self.telas["menu"] = TelaMenu(self, self.mostrar_tela)
        self.telas["selecao_modo"] = TelaSelecaoModo(self, self.mostrar_tela)
        self.telas["jogo"] = TelaJogo(self, self.mostrar_tela)
        self.telas["resultados"] = TelaResultados(self, self.mostrar_tela)
        
        # Inicia mostrando o menu
        self.mostrar_tela("menu")

    def mostrar_tela(self, nome_tela):
        for tela in self.telas.values():
            tela.pack_forget()
            
        self.telas[nome_tela].pack(fill="both", expand=True)

if __name__ == "__main__":
    app = BatalhaMatematicaApp()
    app.mainloop()