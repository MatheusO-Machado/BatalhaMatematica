import sqlite3
import hashlib
import os

PASTA_DB = "database"
CAMINHO_DB = os.path.join(PASTA_DB, "batalha_matematica.db")

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
    def _conectar():
        """Cria a pasta do banco se não existir e retorna a conexão."""
        if not os.path.exists(PASTA_DB):
            os.makedirs(PASTA_DB)
        return sqlite3.connect(CAMINHO_DB)

    @staticmethod
    def _hash_senha(senha):
        """Aplica criptografia SHA-256 na senha para segurança."""
        return hashlib.sha256(senha.encode()).hexdigest()

    @staticmethod
    def inicializar_banco():
        """Cria as tabelas no banco de dados caso não existam."""
        conn = BancoDeDados._conectar()
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

        # --- A MÁGICA DA SINCRONIZAÇÃO ACONTECE AQUI ---
        # Recalcula e corrige o nível de TODOS os usuários cadastrados
        # com base no XP total toda vez que o jogo for aberto.
        cursor.execute('UPDATE usuarios SET nivel = (xp_total / 500) + 1')
        
        conn.commit()
        conn.close()
    
    # --- SISTEMA DE LOGIN E CADASTRO (Corrigido Case-Sensitive) ---
    @staticmethod
    def cadastrar_usuario(username, senha):
        """Registra um novo usuário. Retorna True se sucesso, False se usuário já existir."""
        conn = BancoDeDados._conectar()
        cursor = conn.cursor()
        senha_criptografada = BancoDeDados._hash_senha(senha)
        
        # Filtro Inteligente: Verifica se o nome já existe ignorando maiúsculas e minúsculas
        cursor.execute('SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?)', (username,))
        if cursor.fetchone():
            conn.close()
            return False # Bloqueia o cadastro, pois o usuário já existe
            
        try:
            cursor.execute('INSERT INTO usuarios (username, senha) VALUES (?, ?)', (username, senha_criptografada))
            conn.commit()
            sucesso = True
        except sqlite3.IntegrityError:
            sucesso = False
        finally:
            conn.close()
            
        return sucesso

    @staticmethod
    def fazer_login(username, senha):
        """Valida as credenciais. Retorna o ID do usuário se sucesso, ou None."""
        conn = BancoDeDados._conectar()
        cursor = conn.cursor()
        senha_criptografada = BancoDeDados._hash_senha(senha)
        
        # Permite que o usuário faça login mesmo que digite "matheus" em vez de "Matheus"
        cursor.execute('SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?) AND senha = ?', (username, senha_criptografada))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return resultado[0]
        return None

    # --- SISTEMA DE PARTIDAS E RANKING ---
    @staticmethod
    def salvar_partida(usuario_id, modo, pontos, acertos, tempo):
        """Salva os dados da partida e calcula a evolução de Nível."""
        conn = BancoDeDados._conectar()
        cursor = conn.cursor()
        
        # 1. Salva o histórico da partida
        cursor.execute('''
            INSERT INTO partidas (usuario_id, modo, pontos, acertos, tempo) 
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, modo, pontos, acertos, tempo))
        
        # 2. Resgata o XP atual do banco
        cursor.execute('SELECT xp_total FROM usuarios WHERE id = ?', (usuario_id,))
        xp_atual = cursor.fetchone()[0]
        
        # 3. Matemática de Gamificação: Atualiza XP e calcula o novo Nível
        novo_xp = xp_atual + pontos
        # Fórmula: A cada 500 XP, sobe 1 nível (usando divisão inteira)
        novo_nivel = (novo_xp // 500) + 1 
        
        # 4. Atualiza o perfil do jogador com o novo XP e o novo Nível!
        cursor.execute('''
            UPDATE usuarios SET xp_total = ?, nivel = ? WHERE id = ?
        ''', (novo_xp, novo_nivel, usuario_id))
        
        conn.commit()
        conn.close()

    @staticmethod
    def obter_ranking_geral(limite=10):
        """Retorna os melhores jogadores baseados no XP total."""
        conn = BancoDeDados._conectar()
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
        conn = BancoDeDados._conectar()
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
        conn = BancoDeDados._conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT username, xp_total, nivel FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado

    @staticmethod
    def obter_estatisticas_conquistas(usuario_id):
        """Calcula dados do histórico para o sistema de medalhas."""
        conn = BancoDeDados._conectar()
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
        conn = BancoDeDados._conectar()
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