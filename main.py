from screens.game import TelaJogo
import customtkinter as ctk

# Paleta de Cores do GDD
COR_ROXO = "#7B2CBF"
COR_FUNDO = "#1E1E2E"
COR_BRANCO = "#F8F9FA"

class TelaMenu(ctk.CTkFrame):
    def __init__(self, master, trocar_tela_callback):
        super().__init__(master, fg_color="transparent")
        
        # Título
        self.label_titulo = ctk.CTkLabel(
            self, 
            text="BATALHA MATEMÁTICA", 
            font=("Arial", 36, "bold"),
            text_color=COR_ROXO
        )
        self.label_titulo.pack(pady=(100, 50))
        
        # Botão Jogar
        self.btn_jogar = ctk.CTkButton(
            self, 
            text="JOGAR", 
            fg_color=COR_ROXO,
            font=("Arial", 20, "bold"),
            height=50,
            width=200,
            command=lambda: trocar_tela_callback("jogo")
        )
        self.btn_jogar.pack(pady=10)

        # Botão Sair
        self.btn_sair = ctk.CTkButton(
            self, 
            text="SAIR", 
            fg_color="transparent",
            border_color=COR_ROXO,
            border_width=2,
            font=("Arial", 16, "bold"),
            height=40,
            width=200,
            command=master.destroy
        )
        self.btn_sair.pack(pady=10)

class BatalhaMatematicaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Batalha Matemática v1.0")
        self.geometry("900x600")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=COR_FUNDO)
        
        # Dicionário para armazenar as telas
        self.telas = {}
        
        # Inicializando as telas e passando a função de troca
        self.telas["menu"] = TelaMenu(self, self.mostrar_tela)
        self.telas["jogo"] = TelaJogo(self, self.mostrar_tela)
        
        # Inicia mostrando o menu
        self.mostrar_tela("menu")

    def mostrar_tela(self, nome_tela):
        # Esconde todas as telas
        for tela in self.telas.values():
            tela.pack_forget()
            
        # Mostra apenas a tela solicitada
        self.telas[nome_tela].pack(fill="both", expand=True)

if __name__ == "__main__":
    app = BatalhaMatematicaApp()
    app.mainloop()