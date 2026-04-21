import os
import psycopg2
    

"""
Este módulo contém funções utilitárias para obter cabeçalhos HTTP, conexão com o banco de dados PostgreSQL
e atualizar o status de download de provas no banco.
"""

def getHeaders():
    """
    Retorna um dicionário com cabeçalhos HTTP para simular um navegador.

    Returns:
        dict: Dicionário contendo o User-Agent.
    """
    return  {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
    }

def getConnection():
    """
    Estabelece e retorna uma conexão com o banco de dados PostgreSQL.

    Returns:
        psycopg2.connection: Objeto de conexão com o banco.
    """

    return psycopg2.connect(
        dbname   = os.getenv('DATABASE_NAME',"postgres"),
        user     = os.getenv('DATABASE_USER',"postgres"),
        password = os.getenv('DATABASE_PASSWORD',"mysecretpassword"),
        host     = os.getenv('DATABASE_HOST',"localhost"),  # ou outro host
        port     = os.getenv('DATABASE_PORT',"5432")
    )

def getUpdateDownload(url_pdf:str):
    """
    Atualiza o status de download para True na tabela concursos para a URL especificada.

    Args:
        url_pdf (str): URL do PDF da prova a ser marcada como baixada.
    """
    conn = getConnection()
    cur = conn.cursor()
    QUERY_SQL = f"""
        update concursos 
        set download=true
        where url = '{url_pdf}'
    """
    cur.execute(QUERY_SQL)
    conn.commit()
    cur.close()
    conn.close()