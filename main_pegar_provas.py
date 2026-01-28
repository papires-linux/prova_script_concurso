import src.getReturn as getReturn
import src.dowload_pdf as dowload_pdf

def getListaProvasParaBaixar():
    # Conexão com o banco
    conn = getReturn.getConnection()
    # Cria o cursor
    cur = conn.cursor()
    # Executa a query
    cur.execute("SELECT url FROM concursos WHERE download = false")
    # Pega os resultados
    resultados = cur.fetchall()
    # Fecha tudo
    cur.close()
    conn.close()
    # Itera sobre os resultados
    return resultados

for row in getListaProvasParaBaixar():
    url_pdf = row[0]
    dowload_pdf.download_provas(url_pdf)