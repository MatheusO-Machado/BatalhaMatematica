# =============================================================================
# BATALHA MATEMÁTICA — Controller: Banco de Dados (Model / Camada de Dados)
# =============================================================================
# Responsável por toda a persistência de dados usando SQLite3.
# Segue o padrão Repository: encapsula todas as queries em métodos estáticos.
#
# MELHORIAS DESTA VERSÃO:
#   - Cada jogador recebe uma TAG ÚNICA estilo jogo (ex.: Heroi#4821)
#   - Tabela de conquistas desbloqueadas por jogador
#   - Tabela de progresso do Modo RPG (fase máxima alcançada)
#   - Rankings reorganizados e mais robustos
#
# MATEMÁTICA APLICADA:
#   - Criptografia SHA-256 (função hash) para senhas.
#   - Função escada de nível: nivel = (xp_total // 500) + 1
#   - Geração de TAG via análise combinatória (4 dígitos = 10^4 combinações)
# =============================================================================

import sqlite3
import hashlib
import os
import random

PASTA_DB   = "database"
CAMINHO_DB = os.path.join(PASTA_DB, "batalha_matematica.db")

# Nível mínimo para desbloquear o Modo RPG (Jornada do Herói)
NIVEL_DESBLOQUEIO_RPG = 10


class BancoDeDados:
    """Camada Model: gerencia conexão SQLite, usuários, partidas, conquistas."""

    # ─── Conexão ──────────────────────────────────────────────────────────────

    @staticmethod
    def _conectar():
        """Cria a pasta do banco se não existir e retorna a conexão."""
        os.makedirs(PASTA_DB, exist_ok=True)
        return sqlite3.connect(CAMINHO_DB)

    # ─── Criptografia ─────────────────────────────────────────────────────────

    @staticmethod
    def _hash_senha(senha: str) -> str:
        """
        Aplica a função hash SHA-256 na senha.

        MATEMÁTICA — Funções (Aplicação Obrigatória):
            h: Σ* → {0,1}^256
        Mapeia qualquer string para um valor de tamanho fixo (256 bits).
        Colisões são computacionalmente inviáveis (função injetora na prática).
        """
        return hashlib.sha256(senha.encode()).hexdigest()

    # ─── Geração de TAG única ─────────────────────────────────────────────────

    @staticmethod
    def _gerar_tag(cursor) -> str:
        """
        Gera uma tag numérica de 4 dígitos única (ex.: '4821').

        MATEMÁTICA — Análise Combinatória:
            O espaço de tags é Ω = {0000, ..., 9999}, com |Ω| = 10^4 = 10.000
            combinações possíveis (arranjo com repetição de 10 dígitos em 4 posições).
        Garante unicidade verificando pertinência no conjunto de tags já usadas.
        """
        while True:
            tag = f"{random.randint(0, 9999):04d}"
            cursor.execute("SELECT 1 FROM usuarios WHERE tag = ?", (tag,))
            if not cursor.fetchone():
                return tag

    # ─── Inicialização ────────────────────────────────────────────────────────

    @staticmethod
    def inicializar_banco():
        """Cria/atualiza as tabelas do banco de dados."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        # ── Tabela de Usuários ────────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    NOT NULL,
                tag         TEXT    UNIQUE,
                senha       TEXT    NOT NULL,
                xp_total    INTEGER DEFAULT 0,
                nivel       INTEGER DEFAULT 1,
                rpg_fase_max INTEGER DEFAULT 0,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ── Tabela de Partidas ────────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS partidas (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                modo       TEXT    NOT NULL,
                pontos     INTEGER NOT NULL,
                acertos    INTEGER NOT NULL,
                tempo      INTEGER NOT NULL,
                fase_rpg   INTEGER DEFAULT 0,
                data       DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        # ── Tabela de Conquistas ──────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS conquistas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id  INTEGER,
                chave       TEXT    NOT NULL,
                data        DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                UNIQUE (usuario_id, chave)
            )
        """)

        # ── Migração: adiciona colunas novas em bancos antigos ────────────────
        BancoDeDados._migrar_coluna(c, "usuarios", "tag", "TEXT")
        BancoDeDados._migrar_coluna(c, "usuarios", "rpg_fase_max", "INTEGER DEFAULT 0")
        BancoDeDados._migrar_coluna(c, "usuarios", "data_criacao", "DATETIME")
        BancoDeDados._migrar_coluna(c, "partidas", "fase_rpg", "INTEGER DEFAULT 0")

        # ── Atribui tags a usuários antigos que não têm ───────────────────────
        c.execute("SELECT id FROM usuarios WHERE tag IS NULL OR tag = ''")
        for (uid,) in c.fetchall():
            nova_tag = BancoDeDados._gerar_tag(c)
            c.execute("UPDATE usuarios SET tag = ? WHERE id = ?", (nova_tag, uid))

        # ── Recalcula nível de todos (função escada) ──────────────────────────
        # MATEMÁTICA — Função de Progressão: nivel = floor(xp/500) + 1
        c.execute("UPDATE usuarios SET nivel = (xp_total / 500) + 1")

        conn.commit()
        conn.close()

    @staticmethod
    def _migrar_coluna(cursor, tabela: str, coluna: str, tipo: str):
        """Adiciona uma coluna se ela ainda não existir (migração segura)."""
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [linha[1] for linha in cursor.fetchall()]
        if coluna not in colunas:
            try:
                cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")
            except sqlite3.OperationalError:
                pass

    # ─── Autenticação ─────────────────────────────────────────────────────────

    @staticmethod
    def cadastrar_usuario(username: str, senha: str) -> bool:
        """
        Registra novo usuário com senha hasheada e tag única.
        Retorna True se sucesso, False se nome já existir.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        # Verificação case-insensitive
        c.execute("SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?)", (username,))
        if c.fetchone():
            conn.close()
            return False

        try:
            tag = BancoDeDados._gerar_tag(c)
            c.execute(
                "INSERT INTO usuarios (username, tag, senha) VALUES (?, ?, ?)",
                (username, tag, BancoDeDados._hash_senha(senha))
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def fazer_login(username: str, senha: str):
        """Valida credenciais. Retorna ID do usuário ou None."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM usuarios WHERE LOWER(username)=LOWER(?) AND senha=?",
            (username, BancoDeDados._hash_senha(senha))
        )
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    @staticmethod
    def obter_tag(usuario_id: int) -> str:
        """Retorna a tag única do jogador (ex.: '4821')."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT tag FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row and row[0] else "0000"

    # ─── Partidas ─────────────────────────────────────────────────────────────

    @staticmethod
    def salvar_partida(usuario_id: int, modo: str, pontos: int,
                       acertos: int, tempo: int, fase_rpg: int = 0):
        """
        Salva partida e atualiza XP/Nível do jogador.

        MATEMÁTICA — Função de Progressão de Nível (escada):
            nivel(xp) = floor(xp / 500) + 1
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO partidas (usuario_id,modo,pontos,acertos,tempo,fase_rpg) VALUES (?,?,?,?,?,?)",
            (usuario_id, modo, pontos, acertos, tempo, fase_rpg)
        )

        c.execute("SELECT xp_total, rpg_fase_max FROM usuarios WHERE id=?", (usuario_id,))
        xp_atual, fase_max_atual = c.fetchone()

        novo_xp    = xp_atual + pontos
        novo_nivel = (novo_xp // 500) + 1  # Função escada

        # Atualiza fase máxima do RPG se superou o recorde
        nova_fase_max = max(fase_max_atual or 0, fase_rpg)

        c.execute(
            "UPDATE usuarios SET xp_total=?, nivel=?, rpg_fase_max=? WHERE id=?",
            (novo_xp, novo_nivel, nova_fase_max, usuario_id)
        )
        conn.commit()
        conn.close()

    # ─── Conquistas ───────────────────────────────────────────────────────────

    @staticmethod
    def desbloquear_conquista(usuario_id: int, chave: str) -> bool:
        """
        Registra uma conquista. Retorna True se foi NOVA (recém-desbloqueada),
        False se o jogador já a possuía.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO conquistas (usuario_id, chave) VALUES (?, ?)",
                (usuario_id, chave)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def obter_conquistas(usuario_id: int) -> set:
        """Retorna o CONJUNTO de chaves de conquistas do jogador (Teoria dos Conjuntos)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT chave FROM conquistas WHERE usuario_id = ?", (usuario_id,))
        chaves = {row[0] for row in c.fetchall()}   # set comprehension = conjunto
        conn.close()
        return chaves

    # ─── Progresso RPG ────────────────────────────────────────────────────────

    @staticmethod
    def obter_fase_max_rpg(usuario_id: int) -> int:
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT rpg_fase_max FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        return (row[0] or 0) if row else 0

    @staticmethod
    def rpg_desbloqueado(usuario_id: int) -> bool:
        """
        LÓGICA BOOLEANA: retorna (nivel >= NIVEL_DESBLOQUEIO_RPG).
        O Modo RPG só é liberado ao atingir o nível 10.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT nivel FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        nivel = (row[0] if row else 1)
        return nivel >= NIVEL_DESBLOQUEIO_RPG

    # ─── Rankings ─────────────────────────────────────────────────────────────

    @staticmethod
    def obter_ranking_geral(limite: int = 100):
        """Ranking global por XP. Retorna (username, tag, xp_total, nivel)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT username, tag, xp_total, nivel FROM usuarios ORDER BY xp_total DESC LIMIT ?",
            (limite,)
        )
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obter_ranking_rpg(limite: int = 100):
        """Ranking exclusivo do Modo RPG por fase máxima. (username, tag, fase_max, nivel)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT username, tag, rpg_fase_max, nivel
            FROM usuarios
            WHERE rpg_fase_max > 0
            ORDER BY rpg_fase_max DESC, xp_total DESC
            LIMIT ?
        """, (limite,))
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obter_ranking_modo(modo: str, limite: int = 100):
        """Melhores pontuações num modo. (username, tag, pontos, acertos, tempo)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT u.username, u.tag, p.pontos, p.acertos, p.tempo
            FROM partidas p JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.modo = ?
            ORDER BY p.pontos DESC, p.tempo ASC
            LIMIT ?
        """, (modo, limite))
        rows = c.fetchall()
        conn.close()
        return rows

    # ─── Perfil ───────────────────────────────────────────────────────────────

    @staticmethod
    def obter_dados_perfil(usuario_id: int):
        """Retorna (username, tag, xp_total, nivel, rpg_fase_max)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT username, tag, xp_total, nivel, rpg_fase_max FROM usuarios WHERE id=?",
            (usuario_id,)
        )
        row = c.fetchone()
        conn.close()
        return row

    @staticmethod
    def obter_estatisticas_conquistas(usuario_id: int) -> dict:
        """
        Reúne estatísticas agregadas do jogador para verificação de conquistas.
        TEORIA DOS CONJUNTOS: 'modos_distintos' é a cardinalidade do conjunto
        de modos já jogados pelo usuário.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id=?", (usuario_id,))
        total = c.fetchone()[0]

        c.execute("SELECT MAX(pontos) FROM partidas WHERE usuario_id=?", (usuario_id,))
        maior = c.fetchone()[0] or 0

        c.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id=? AND modo='Equações'", (usuario_id,))
        equacoes = c.fetchone()[0]

        # Total de acertos somados em todas as partidas
        c.execute("SELECT COALESCE(SUM(acertos),0) FROM partidas WHERE usuario_id=?", (usuario_id,))
        total_acertos = c.fetchone()[0]

        # Partidas perfeitas (10 acertos) — apenas modos clássicos (10 questões)
        c.execute("""SELECT COUNT(*) FROM partidas
                     WHERE usuario_id=? AND acertos>=10 AND modo!='Jornada RPG'""",
                  (usuario_id,))
        perfeitas = c.fetchone()[0]

        # Conjunto de modos distintos jogados (exclui RPG, que é à parte)
        c.execute("""SELECT COUNT(DISTINCT modo) FROM partidas
                     WHERE usuario_id=? AND modo!='Jornada RPG'""", (usuario_id,))
        modos_distintos = c.fetchone()[0]

        # XP e nível atuais
        c.execute("SELECT xp_total, nivel, rpg_fase_max FROM usuarios WHERE id=?", (usuario_id,))
        row = c.fetchone()
        xp_total = (row[0] if row else 0) or 0
        nivel    = (row[1] if row else 1) or 1
        fase_rpg = (row[2] if row else 0) or 0

        conn.close()
        return {
            "total_partidas":   total,
            "maior_pontuacao":  maior,
            "partidas_equacoes": equacoes,
            "total_acertos":    total_acertos,
            "partidas_perfeitas": perfeitas,
            "modos_distintos":  modos_distintos,
            "xp_total":         xp_total,
            "nivel":            nivel,
            "rpg_fase_max":     fase_rpg,
        }

    @staticmethod
    def obter_historico_recente(usuario_id: int, limite: int = 5):
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT modo, pontos, acertos, tempo FROM partidas
            WHERE usuario_id=? ORDER BY id DESC LIMIT ?
        """, (usuario_id, limite))
        rows = c.fetchall()
        conn.close()
        return rows# =============================================================================
# BATALHA MATEMÁTICA — Controller: Banco de Dados (Model / Camada de Dados)
# =============================================================================
# Responsável por toda a persistência de dados usando SQLite3.
# Segue o padrão Repository: encapsula todas as queries em métodos estáticos.
#
# MELHORIAS DESTA VERSÃO:
#   - Cada jogador recebe uma TAG ÚNICA estilo jogo (ex.: Heroi#4821)
#   - Tabela de conquistas desbloqueadas por jogador
#   - Tabela de progresso do Modo RPG (fase máxima alcançada)
#   - Rankings reorganizados e mais robustos
#
# MATEMÁTICA APLICADA:
#   - Criptografia SHA-256 (função hash) para senhas.
#   - Função escada de nível: nivel = (xp_total // 500) + 1
#   - Geração de TAG via análise combinatória (4 dígitos = 10^4 combinações)
# =============================================================================

import sqlite3
import hashlib
import os
import random

PASTA_DB   = "database"
CAMINHO_DB = os.path.join(PASTA_DB, "batalha_matematica.db")

# Nível mínimo para desbloquear o Modo RPG (Jornada do Herói)
NIVEL_DESBLOQUEIO_RPG = 10


class BancoDeDados:
    """Camada Model: gerencia conexão SQLite, usuários, partidas, conquistas."""

    # ─── Conexão ──────────────────────────────────────────────────────────────

    @staticmethod
    def _conectar():
        """Cria a pasta do banco se não existir e retorna a conexão."""
        os.makedirs(PASTA_DB, exist_ok=True)
        return sqlite3.connect(CAMINHO_DB)

    # ─── Criptografia ─────────────────────────────────────────────────────────

    @staticmethod
    def _hash_senha(senha: str) -> str:
        """
        Aplica a função hash SHA-256 na senha.

        MATEMÁTICA — Funções (Aplicação Obrigatória):
            h: Σ* → {0,1}^256
        Mapeia qualquer string para um valor de tamanho fixo (256 bits).
        Colisões são computacionalmente inviáveis (função injetora na prática).
        """
        return hashlib.sha256(senha.encode()).hexdigest()

    # ─── Geração de TAG única ─────────────────────────────────────────────────

    @staticmethod
    def _gerar_tag(cursor) -> str:
        """
        Gera uma tag numérica de 4 dígitos única (ex.: '4821').

        MATEMÁTICA — Análise Combinatória:
            O espaço de tags é Ω = {0000, ..., 9999}, com |Ω| = 10^4 = 10.000
            combinações possíveis (arranjo com repetição de 10 dígitos em 4 posições).
        Garante unicidade verificando pertinência no conjunto de tags já usadas.
        """
        while True:
            tag = f"{random.randint(0, 9999):04d}"
            cursor.execute("SELECT 1 FROM usuarios WHERE tag = ?", (tag,))
            if not cursor.fetchone():
                return tag

    # ─── Inicialização ────────────────────────────────────────────────────────

    @staticmethod
    def inicializar_banco():
        """Cria/atualiza as tabelas do banco de dados."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        # ── Tabela de Usuários ────────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    NOT NULL,
                tag         TEXT    UNIQUE,
                senha       TEXT    NOT NULL,
                xp_total    INTEGER DEFAULT 0,
                nivel       INTEGER DEFAULT 1,
                rpg_fase_max INTEGER DEFAULT 0,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ── Tabela de Partidas ────────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS partidas (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                modo       TEXT    NOT NULL,
                pontos     INTEGER NOT NULL,
                acertos    INTEGER NOT NULL,
                tempo      INTEGER NOT NULL,
                fase_rpg   INTEGER DEFAULT 0,
                data       DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        # ── Tabela de Conquistas ──────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS conquistas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id  INTEGER,
                chave       TEXT    NOT NULL,
                data        DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                UNIQUE (usuario_id, chave)
            )
        """)

        # ── Migração: adiciona colunas novas em bancos antigos ────────────────
        BancoDeDados._migrar_coluna(c, "usuarios", "tag", "TEXT")
        BancoDeDados._migrar_coluna(c, "usuarios", "rpg_fase_max", "INTEGER DEFAULT 0")
        BancoDeDados._migrar_coluna(c, "usuarios", "data_criacao", "DATETIME")
        BancoDeDados._migrar_coluna(c, "partidas", "fase_rpg", "INTEGER DEFAULT 0")

        # ── Atribui tags a usuários antigos que não têm ───────────────────────
        c.execute("SELECT id FROM usuarios WHERE tag IS NULL OR tag = ''")
        for (uid,) in c.fetchall():
            nova_tag = BancoDeDados._gerar_tag(c)
            c.execute("UPDATE usuarios SET tag = ? WHERE id = ?", (nova_tag, uid))

        # ── Recalcula nível de todos (função escada) ──────────────────────────
        # MATEMÁTICA — Função de Progressão: nivel = floor(xp/500) + 1
        c.execute("UPDATE usuarios SET nivel = (xp_total / 500) + 1")

        conn.commit()
        conn.close()

    @staticmethod
    def _migrar_coluna(cursor, tabela: str, coluna: str, tipo: str):
        """Adiciona uma coluna se ela ainda não existir (migração segura)."""
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [linha[1] for linha in cursor.fetchall()]
        if coluna not in colunas:
            try:
                cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")
            except sqlite3.OperationalError:
                pass

    # ─── Autenticação ─────────────────────────────────────────────────────────

    @staticmethod
    def cadastrar_usuario(username: str, senha: str) -> bool:
        """
        Registra novo usuário com senha hasheada e tag única.
        Retorna True se sucesso, False se nome já existir.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        # Verificação case-insensitive
        c.execute("SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?)", (username,))
        if c.fetchone():
            conn.close()
            return False

        try:
            tag = BancoDeDados._gerar_tag(c)
            c.execute(
                "INSERT INTO usuarios (username, tag, senha) VALUES (?, ?, ?)",
                (username, tag, BancoDeDados._hash_senha(senha))
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def fazer_login(username: str, senha: str):
        """Valida credenciais. Retorna ID do usuário ou None."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM usuarios WHERE LOWER(username)=LOWER(?) AND senha=?",
            (username, BancoDeDados._hash_senha(senha))
        )
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    @staticmethod
    def obter_tag(usuario_id: int) -> str:
        """Retorna a tag única do jogador (ex.: '4821')."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT tag FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row and row[0] else "0000"

    # ─── Partidas ─────────────────────────────────────────────────────────────

    @staticmethod
    def salvar_partida(usuario_id: int, modo: str, pontos: int,
                       acertos: int, tempo: int, fase_rpg: int = 0):
        """
        Salva partida e atualiza XP/Nível do jogador.

        MATEMÁTICA — Função de Progressão de Nível (escada):
            nivel(xp) = floor(xp / 500) + 1
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO partidas (usuario_id,modo,pontos,acertos,tempo,fase_rpg) VALUES (?,?,?,?,?,?)",
            (usuario_id, modo, pontos, acertos, tempo, fase_rpg)
        )

        c.execute("SELECT xp_total, rpg_fase_max FROM usuarios WHERE id=?", (usuario_id,))
        xp_atual, fase_max_atual = c.fetchone()

        novo_xp    = xp_atual + pontos
        novo_nivel = (novo_xp // 500) + 1  # Função escada

        # Atualiza fase máxima do RPG se superou o recorde
        nova_fase_max = max(fase_max_atual or 0, fase_rpg)

        c.execute(
            "UPDATE usuarios SET xp_total=?, nivel=?, rpg_fase_max=? WHERE id=?",
            (novo_xp, novo_nivel, nova_fase_max, usuario_id)
        )
        conn.commit()
        conn.close()

    # ─── Conquistas ───────────────────────────────────────────────────────────

    @staticmethod
    def desbloquear_conquista(usuario_id: int, chave: str) -> bool:
        """
        Registra uma conquista. Retorna True se foi NOVA (recém-desbloqueada),
        False se o jogador já a possuía.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO conquistas (usuario_id, chave) VALUES (?, ?)",
                (usuario_id, chave)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def obter_conquistas(usuario_id: int) -> set:
        """Retorna o CONJUNTO de chaves de conquistas do jogador (Teoria dos Conjuntos)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT chave FROM conquistas WHERE usuario_id = ?", (usuario_id,))
        chaves = {row[0] for row in c.fetchall()}   # set comprehension = conjunto
        conn.close()
        return chaves

    # ─── Progresso RPG ────────────────────────────────────────────────────────

    @staticmethod
    def obter_fase_max_rpg(usuario_id: int) -> int:
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT rpg_fase_max FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        return (row[0] or 0) if row else 0

    @staticmethod
    def rpg_desbloqueado(usuario_id: int) -> bool:
        """
        LÓGICA BOOLEANA: retorna (nivel >= NIVEL_DESBLOQUEIO_RPG).
        O Modo RPG só é liberado ao atingir o nível 10.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT nivel FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        nivel = (row[0] if row else 1)
        return nivel >= NIVEL_DESBLOQUEIO_RPG

    # ─── Rankings ─────────────────────────────────────────────────────────────

    @staticmethod
    def obter_ranking_geral(limite: int = 100):
        """Ranking global por XP. Retorna (username, tag, xp_total, nivel)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT username, tag, xp_total, nivel FROM usuarios ORDER BY xp_total DESC LIMIT ?",
            (limite,)
        )
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obter_ranking_rpg(limite: int = 100):
        """Ranking exclusivo do Modo RPG por fase máxima. (username, tag, fase_max, nivel)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT username, tag, rpg_fase_max, nivel
            FROM usuarios
            WHERE rpg_fase_max > 0
            ORDER BY rpg_fase_max DESC, xp_total DESC
            LIMIT ?
        """, (limite,))
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obter_ranking_modo(modo: str, limite: int = 100):
        """Melhores pontuações num modo. (username, tag, pontos, acertos, tempo)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT u.username, u.tag, p.pontos, p.acertos, p.tempo
            FROM partidas p JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.modo = ?
            ORDER BY p.pontos DESC, p.tempo ASC
            LIMIT ?
        """, (modo, limite))
        rows = c.fetchall()
        conn.close()
        return rows

    # ─── Perfil ───────────────────────────────────────────────────────────────

    @staticmethod
    def obter_dados_perfil(usuario_id: int):
        """Retorna (username, tag, xp_total, nivel, rpg_fase_max)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT username, tag, xp_total, nivel, rpg_fase_max FROM usuarios WHERE id=?",
            (usuario_id,)
        )
        row = c.fetchone()
        conn.close()
        return row

    @staticmethod
    def obter_estatisticas_conquistas(usuario_id: int) -> dict:
        """
        Reúne estatísticas agregadas do jogador para verificação de conquistas.
        TEORIA DOS CONJUNTOS: 'modos_distintos' é a cardinalidade do conjunto
        de modos já jogados pelo usuário.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id=?", (usuario_id,))
        total = c.fetchone()[0]

        c.execute("SELECT MAX(pontos) FROM partidas WHERE usuario_id=?", (usuario_id,))
        maior = c.fetchone()[0] or 0

        c.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id=? AND modo='Equações'", (usuario_id,))
        equacoes = c.fetchone()[0]

        # Total de acertos somados em todas as partidas
        c.execute("SELECT COALESCE(SUM(acertos),0) FROM partidas WHERE usuario_id=?", (usuario_id,))
        total_acertos = c.fetchone()[0]

        # Partidas perfeitas (10 acertos) — apenas modos clássicos (10 questões)
        c.execute("""SELECT COUNT(*) FROM partidas
                     WHERE usuario_id=? AND acertos>=10 AND modo!='Jornada RPG'""",
                  (usuario_id,))
        perfeitas = c.fetchone()[0]

        # Conjunto de modos distintos jogados (exclui RPG, que é à parte)
        c.execute("""SELECT COUNT(DISTINCT modo) FROM partidas
                     WHERE usuario_id=? AND modo!='Jornada RPG'""", (usuario_id,))
        modos_distintos = c.fetchone()[0]

        # XP e nível atuais
        c.execute("SELECT xp_total, nivel, rpg_fase_max FROM usuarios WHERE id=?", (usuario_id,))
        row = c.fetchone()
        xp_total = (row[0] if row else 0) or 0
        nivel    = (row[1] if row else 1) or 1
        fase_rpg = (row[2] if row else 0) or 0

        conn.close()
        return {
            "total_partidas":   total,
            "maior_pontuacao":  maior,
            "partidas_equacoes": equacoes,
            "total_acertos":    total_acertos,
            "partidas_perfeitas": perfeitas,
            "modos_distintos":  modos_distintos,
            "xp_total":         xp_total,
            "nivel":            nivel,
            "rpg_fase_max":     fase_rpg,
        }

    @staticmethod
    def obter_historico_recente(usuario_id: int, limite: int = 5):
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT modo, pontos, acertos, tempo FROM partidas
            WHERE usuario_id=? ORDER BY id DESC LIMIT ?
        """, (usuario_id, limite))
        rows = c.fetchall()
        conn.close()
        return rows# =============================================================================
# BATALHA MATEMÁTICA — Controller: Banco de Dados (Model / Camada de Dados)
# =============================================================================
# Responsável por toda a persistência de dados usando SQLite3.
# Segue o padrão Repository: encapsula todas as queries em métodos estáticos.
#
# MELHORIAS DESTA VERSÃO:
#   - Cada jogador recebe uma TAG ÚNICA estilo jogo (ex.: Heroi#4821)
#   - Tabela de conquistas desbloqueadas por jogador
#   - Tabela de progresso do Modo RPG (fase máxima alcançada)
#   - Rankings reorganizados e mais robustos
#
# MATEMÁTICA APLICADA:
#   - Criptografia SHA-256 (função hash) para senhas.
#   - Função escada de nível: nivel = (xp_total // 500) + 1
#   - Geração de TAG via análise combinatória (4 dígitos = 10^4 combinações)
# =============================================================================

import sqlite3
import hashlib
import os
import random

PASTA_DB   = "database"
CAMINHO_DB = os.path.join(PASTA_DB, "batalha_matematica.db")

# Nível mínimo para desbloquear o Modo RPG (Jornada do Herói)
NIVEL_DESBLOQUEIO_RPG = 10


class BancoDeDados:
    """Camada Model: gerencia conexão SQLite, usuários, partidas, conquistas."""

    # ─── Conexão ──────────────────────────────────────────────────────────────

    @staticmethod
    def _conectar():
        """Cria a pasta do banco se não existir e retorna a conexão."""
        os.makedirs(PASTA_DB, exist_ok=True)
        return sqlite3.connect(CAMINHO_DB)

    # ─── Criptografia ─────────────────────────────────────────────────────────

    @staticmethod
    def _hash_senha(senha: str) -> str:
        """
        Aplica a função hash SHA-256 na senha.

        MATEMÁTICA — Funções (Aplicação Obrigatória):
            h: Σ* → {0,1}^256
        Mapeia qualquer string para um valor de tamanho fixo (256 bits).
        Colisões são computacionalmente inviáveis (função injetora na prática).
        """
        return hashlib.sha256(senha.encode()).hexdigest()

    # ─── Geração de TAG única ─────────────────────────────────────────────────

    @staticmethod
    def _gerar_tag(cursor) -> str:
        """
        Gera uma tag numérica de 4 dígitos única (ex.: '4821').

        MATEMÁTICA — Análise Combinatória:
            O espaço de tags é Ω = {0000, ..., 9999}, com |Ω| = 10^4 = 10.000
            combinações possíveis (arranjo com repetição de 10 dígitos em 4 posições).
        Garante unicidade verificando pertinência no conjunto de tags já usadas.
        """
        while True:
            tag = f"{random.randint(0, 9999):04d}"
            cursor.execute("SELECT 1 FROM usuarios WHERE tag = ?", (tag,))
            if not cursor.fetchone():
                return tag

    # ─── Inicialização ────────────────────────────────────────────────────────

    @staticmethod
    def inicializar_banco():
        """Cria/atualiza as tabelas do banco de dados."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        # ── Tabela de Usuários ────────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    NOT NULL,
                tag         TEXT    UNIQUE,
                senha       TEXT    NOT NULL,
                xp_total    INTEGER DEFAULT 0,
                nivel       INTEGER DEFAULT 1,
                rpg_fase_max INTEGER DEFAULT 0,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ── Tabela de Partidas ────────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS partidas (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                modo       TEXT    NOT NULL,
                pontos     INTEGER NOT NULL,
                acertos    INTEGER NOT NULL,
                tempo      INTEGER NOT NULL,
                fase_rpg   INTEGER DEFAULT 0,
                data       DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)

        # ── Tabela de Conquistas ──────────────────────────────────────────────
        c.execute("""
            CREATE TABLE IF NOT EXISTS conquistas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id  INTEGER,
                chave       TEXT    NOT NULL,
                data        DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                UNIQUE (usuario_id, chave)
            )
        """)

        # ── Migração: adiciona colunas novas em bancos antigos ────────────────
        BancoDeDados._migrar_coluna(c, "usuarios", "tag", "TEXT")
        BancoDeDados._migrar_coluna(c, "usuarios", "rpg_fase_max", "INTEGER DEFAULT 0")
        BancoDeDados._migrar_coluna(c, "usuarios", "data_criacao", "DATETIME")
        BancoDeDados._migrar_coluna(c, "partidas", "fase_rpg", "INTEGER DEFAULT 0")

        # ── Atribui tags a usuários antigos que não têm ───────────────────────
        c.execute("SELECT id FROM usuarios WHERE tag IS NULL OR tag = ''")
        for (uid,) in c.fetchall():
            nova_tag = BancoDeDados._gerar_tag(c)
            c.execute("UPDATE usuarios SET tag = ? WHERE id = ?", (nova_tag, uid))

        # ── Recalcula nível de todos (função escada) ──────────────────────────
        # MATEMÁTICA — Função de Progressão: nivel = floor(xp/500) + 1
        c.execute("UPDATE usuarios SET nivel = (xp_total / 500) + 1")

        conn.commit()
        conn.close()

    @staticmethod
    def _migrar_coluna(cursor, tabela: str, coluna: str, tipo: str):
        """Adiciona uma coluna se ela ainda não existir (migração segura)."""
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [linha[1] for linha in cursor.fetchall()]
        if coluna not in colunas:
            try:
                cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}")
            except sqlite3.OperationalError:
                pass

    # ─── Autenticação ─────────────────────────────────────────────────────────

    @staticmethod
    def cadastrar_usuario(username: str, senha: str) -> bool:
        """
        Registra novo usuário com senha hasheada e tag única.
        Retorna True se sucesso, False se nome já existir.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        # Verificação case-insensitive
        c.execute("SELECT id FROM usuarios WHERE LOWER(username) = LOWER(?)", (username,))
        if c.fetchone():
            conn.close()
            return False

        try:
            tag = BancoDeDados._gerar_tag(c)
            c.execute(
                "INSERT INTO usuarios (username, tag, senha) VALUES (?, ?, ?)",
                (username, tag, BancoDeDados._hash_senha(senha))
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def fazer_login(username: str, senha: str):
        """Valida credenciais. Retorna ID do usuário ou None."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM usuarios WHERE LOWER(username)=LOWER(?) AND senha=?",
            (username, BancoDeDados._hash_senha(senha))
        )
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    @staticmethod
    def obter_tag(usuario_id: int) -> str:
        """Retorna a tag única do jogador (ex.: '4821')."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT tag FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        return row[0] if row and row[0] else "0000"

    # ─── Partidas ─────────────────────────────────────────────────────────────

    @staticmethod
    def salvar_partida(usuario_id: int, modo: str, pontos: int,
                       acertos: int, tempo: int, fase_rpg: int = 0):
        """
        Salva partida e atualiza XP/Nível do jogador.

        MATEMÁTICA — Função de Progressão de Nível (escada):
            nivel(xp) = floor(xp / 500) + 1
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO partidas (usuario_id,modo,pontos,acertos,tempo,fase_rpg) VALUES (?,?,?,?,?,?)",
            (usuario_id, modo, pontos, acertos, tempo, fase_rpg)
        )

        c.execute("SELECT xp_total, rpg_fase_max FROM usuarios WHERE id=?", (usuario_id,))
        xp_atual, fase_max_atual = c.fetchone()

        novo_xp    = xp_atual + pontos
        novo_nivel = (novo_xp // 500) + 1  # Função escada

        # Atualiza fase máxima do RPG se superou o recorde
        nova_fase_max = max(fase_max_atual or 0, fase_rpg)

        c.execute(
            "UPDATE usuarios SET xp_total=?, nivel=?, rpg_fase_max=? WHERE id=?",
            (novo_xp, novo_nivel, nova_fase_max, usuario_id)
        )
        conn.commit()
        conn.close()

    # ─── Conquistas ───────────────────────────────────────────────────────────

    @staticmethod
    def desbloquear_conquista(usuario_id: int, chave: str) -> bool:
        """
        Registra uma conquista. Retorna True se foi NOVA (recém-desbloqueada),
        False se o jogador já a possuía.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO conquistas (usuario_id, chave) VALUES (?, ?)",
                (usuario_id, chave)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def obter_conquistas(usuario_id: int) -> set:
        """Retorna o CONJUNTO de chaves de conquistas do jogador (Teoria dos Conjuntos)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT chave FROM conquistas WHERE usuario_id = ?", (usuario_id,))
        chaves = {row[0] for row in c.fetchall()}   # set comprehension = conjunto
        conn.close()
        return chaves

    # ─── Progresso RPG ────────────────────────────────────────────────────────

    @staticmethod
    def obter_fase_max_rpg(usuario_id: int) -> int:
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT rpg_fase_max FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        return (row[0] or 0) if row else 0

    @staticmethod
    def rpg_desbloqueado(usuario_id: int) -> bool:
        """
        LÓGICA BOOLEANA: retorna (nivel >= NIVEL_DESBLOQUEIO_RPG).
        O Modo RPG só é liberado ao atingir o nível 10.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("SELECT nivel FROM usuarios WHERE id = ?", (usuario_id,))
        row = c.fetchone()
        conn.close()
        nivel = (row[0] if row else 1)
        return nivel >= NIVEL_DESBLOQUEIO_RPG

    # ─── Rankings ─────────────────────────────────────────────────────────────

    @staticmethod
    def obter_ranking_geral(limite: int = 100):
        """Ranking global por XP. Retorna (username, tag, xp_total, nivel)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT username, tag, xp_total, nivel FROM usuarios ORDER BY xp_total DESC LIMIT ?",
            (limite,)
        )
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obter_ranking_rpg(limite: int = 100):
        """Ranking exclusivo do Modo RPG por fase máxima. (username, tag, fase_max, nivel)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT username, tag, rpg_fase_max, nivel
            FROM usuarios
            WHERE rpg_fase_max > 0
            ORDER BY rpg_fase_max DESC, xp_total DESC
            LIMIT ?
        """, (limite,))
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obter_ranking_modo(modo: str, limite: int = 100):
        """Melhores pontuações num modo. (username, tag, pontos, acertos, tempo)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT u.username, u.tag, p.pontos, p.acertos, p.tempo
            FROM partidas p JOIN usuarios u ON p.usuario_id = u.id
            WHERE p.modo = ?
            ORDER BY p.pontos DESC, p.tempo ASC
            LIMIT ?
        """, (modo, limite))
        rows = c.fetchall()
        conn.close()
        return rows

    # ─── Perfil ───────────────────────────────────────────────────────────────

    @staticmethod
    def obter_dados_perfil(usuario_id: int):
        """Retorna (username, tag, xp_total, nivel, rpg_fase_max)."""
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute(
            "SELECT username, tag, xp_total, nivel, rpg_fase_max FROM usuarios WHERE id=?",
            (usuario_id,)
        )
        row = c.fetchone()
        conn.close()
        return row

    @staticmethod
    def obter_estatisticas_conquistas(usuario_id: int) -> dict:
        """
        Reúne estatísticas agregadas do jogador para verificação de conquistas.
        TEORIA DOS CONJUNTOS: 'modos_distintos' é a cardinalidade do conjunto
        de modos já jogados pelo usuário.
        """
        conn = BancoDeDados._conectar()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id=?", (usuario_id,))
        total = c.fetchone()[0]

        c.execute("SELECT MAX(pontos) FROM partidas WHERE usuario_id=?", (usuario_id,))
        maior = c.fetchone()[0] or 0

        c.execute("SELECT COUNT(*) FROM partidas WHERE usuario_id=? AND modo='Equações'", (usuario_id,))
        equacoes = c.fetchone()[0]

        # Total de acertos somados em todas as partidas
        c.execute("SELECT COALESCE(SUM(acertos),0) FROM partidas WHERE usuario_id=?", (usuario_id,))
        total_acertos = c.fetchone()[0]

        # Partidas perfeitas (10 acertos) — apenas modos clássicos (10 questões)
        c.execute("""SELECT COUNT(*) FROM partidas
                     WHERE usuario_id=? AND acertos>=10 AND modo!='Jornada RPG'""",
                  (usuario_id,))
        perfeitas = c.fetchone()[0]

        # Conjunto de modos distintos jogados (exclui RPG, que é à parte)
        c.execute("""SELECT COUNT(DISTINCT modo) FROM partidas
                     WHERE usuario_id=? AND modo!='Jornada RPG'""", (usuario_id,))
        modos_distintos = c.fetchone()[0]

        # XP e nível atuais
        c.execute("SELECT xp_total, nivel, rpg_fase_max FROM usuarios WHERE id=?", (usuario_id,))
        row = c.fetchone()
        xp_total = (row[0] if row else 0) or 0
        nivel    = (row[1] if row else 1) or 1
        fase_rpg = (row[2] if row else 0) or 0

        conn.close()
        return {
            "total_partidas":   total,
            "maior_pontuacao":  maior,
            "partidas_equacoes": equacoes,
            "total_acertos":    total_acertos,
            "partidas_perfeitas": perfeitas,
            "modos_distintos":  modos_distintos,
            "xp_total":         xp_total,
            "nivel":            nivel,
            "rpg_fase_max":     fase_rpg,
        }

    @staticmethod
    def obter_historico_recente(usuario_id: int, limite: int = 5):
        conn = BancoDeDados._conectar()
        c = conn.cursor()
        c.execute("""
            SELECT modo, pontos, acertos, tempo FROM partidas
            WHERE usuario_id=? ORDER BY id DESC LIMIT ?
        """, (usuario_id, limite))
        rows = c.fetchall()
        conn.close()
        return rows