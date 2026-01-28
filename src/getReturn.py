def getHeaders():
    return  {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
    }

def getConnection():
    import psycopg2
    return psycopg2.connect(
        dbname="postgres",
        user="meuusuario",
        password="minhasenha",
        host="localhost",  # ou outro host
        port="5432"
    )

def getUpdateDownload(url_pdf:str):
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