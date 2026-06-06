import os

# Estrutura do seu GDD
pastas = [
    "assets/icones", "assets/avatares", "assets/sons", "assets/fundos",
    "dados", "perguntas", "screens", "utils"
]

arquivos = [
    "dados/ranking.json", "dados/conquistas.json",
    "perguntas/tabuada.json", "perguntas/fracoes.json", 
    "perguntas/porcentagem.json", "perguntas/regra_tres.json",
    "screens/menu.py", "screens/game.py", "screens/ranking.py", "screens/manual.py",
    "utils/pontuacao.py", "utils/xp.py", "utils/conquistas.py",
    "main.py", ".gitignore"
]

# Criando as pastas
for pasta in pastas:
    os.makedirs(pasta, exist_ok=True)

# Criando os arquivos vazios
for arquivo in arquivos:
    with open(arquivo, 'a') as f:
        pass

print("Estrutura do Batalha Matemática criada com sucesso! Pode começar a codar.")
