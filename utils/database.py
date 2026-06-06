import sqlite3
import hashlib
import os

# Define o nome do arquivo do banco de dados na raiz do projeto
DB_PATH = "batalha_matematica.db"

class BancoDeDados:
    """
    =========================================================================
    MOTOR DE PERSISTÊNCIA DE DADOS (SQLite)
    =========================================================================
    Gerencia usuários, criptografia de senhas, histórico de partidas 
    e geração de rankings utilizando linguagem SQL estruturada.
    =========================================================================
    """
    
    @staticmethod
    def _hash_senha(senha):
        """Aplica criptografia SHA-256 na senha para segurança."""
        return hashlib.sha256(senha.encode()).hexdigest()

    @staticmethod
    def inicializar_banco():
        """Cria as tabelas no banco de dados caso não existam."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Tabela 1: Usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                xp_total INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 1
            )
        ''')
        
        # Tabela 2: Partidas (Para os Rankings e Histórico)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                modo TEXT NOT NULL,
                pontos INTEGER NOT NULL,
                acertos INTEGER NOT NULL,
                tempo INTEGER NOT NULL,
                data DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    # --- SISTEMA DE LOGIN E CADASTRO ---
    @staticmethod
    def cadastrar_usuario(username, senha):
        """Registra um novo usuário. Retorna True se sucesso, False se usuário já existir."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        senha_criptografada = BancoDeDados._hash_senha(senha)
        
        try:
            cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', (username, senha_criptografada))
            conn.commit()
            sucesso = True
        except sqlite3.IntegrityError:
            sucesso = False # Usuário já existe
        finally:
            conn.close()
            
        return sucesso

    @staticmethod
    def fazer_login(username, senha):
        """Valida as credenciais. Retorna o ID do usuário se sucesso, ou None."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        senha_criptografada = BancoDeDados._hash_senha(senha)
        
        cursor.execute('SELECT id FROM usuarios WHERE username = ? AND senha = ?', (username, senha_criptografada))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return resultado[0] # Retorna o ID do usuário logado
        return None

    # --- SISTEMA DE PARTIDAS E RANKING ---
    @staticmethod
    def salvar_partida(usuario_id, modo, pontos, acertos, tempo):
        """Salva os dados da partida e adiciona XP ao perfil do jogador."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Salva o histórico da partida
        cursor.execute('''
            INSERT INTO partidas (usuario_id, modo, pontos, acertos, tempo) 
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, modo, pontos, acertos, tempo))
        
        # Atualiza o XP total do usuário (1 ponto = 1 XP)
        cursor.execute('''
            UPDATE usuarios SET xp_total = xp_total + ? WHERE id = ?
        ''', (pontos, usuario_id))
        
        conn.commit()
        conn.close()

    @staticmethod
    def obter_ranking_geral(limite=10):
        """Retorna os melhores jogadores baseados no XP total."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, xp_total, nivel 
            FROM usuarios 
            ORDER BY xp_total DESC 
            LIMIT ?
        ''', (limite,))
        
        ranking = cursor.fetchall()
        conn.close()
        return ranking

    @staticmethod
    def obter_ranking_modo(modo, limite=10):
        """Retorna as melhores pontuações em um modo específico."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.username, p.pontos, p.acertos, p.tempo 
            FROM partidas p
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.modo = ?
            ORDER BY p.pontos DESC, p.tempo ASC
            LIMIT ?
        ''', (modo, limite,))
        
        ranking = cursor.fetchall()
        conn.close()
        return ranking
    
    @staticmethod
    def obter_dados_perfil(usuario_id):
        """Retorna o username, xp_total e nível do usuário."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT username, xp_total, nivel FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado

    @staticmethod
    def obter_estatisticas_conquistas(usuario_id):
        """Calcula dados do histórico para o sistema de medalhas."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total de partidas jogadas
        cursor.execute('SELECT COUNT(*) FROM partidas WHERE usuario_id = ?', (usuario_id,))
        total_partidas = cursor.fetchone()[0]
        
        # Maior pontuação conquistada em uma única partida
        cursor.execute('SELECT MAX(pontos) FROM partidas WHERE usuario_id = ?', (usuario_id,))
        maior_pontuacao = cursor.fetchone()[0] or 0
        
        # Quantidade de partidas no modo Equações
        cursor.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id = ? AND modo = 'Equações'", (usuario_id,))
        partidas_equacoes = cursor.fetchone()[0]
        
        conn.close()
        return {
            "total_partidas": total_partidas,
            "maior_pontuacao": maior_pontuacao,
            "partidas_equacoes": partidas_equacoes
        }
    
    @staticmethod
    def obter_historico_recente(usuario_id, limite=5):
        """Busca as últimas partidas jogadas pelo usuário para o Perfil."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT modo, pontos, acertos, tempo 
            FROM partidas 
            WHERE usuario_id = ? 
            ORDER BY id DESC 
            LIMIT ?
        ''', (usuario_id, limite))
        historico = cursor.fetchall()
        conn.close()
        return historico