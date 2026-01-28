import requests
#import psycopg2
import src.getReturn as getReturn

from bs4 import BeautifulSoup

def fazer_busca_prova(banca:str):
    headers = getReturn.getHeaders()
    url_source = f"https://www.pciconcursos.com.br/provas/{banca}"

    for i in range(1,999):
        if i == 1:
            url = url_source
        else:
            url = f"{url_source}/{i}"
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, 'html.parser')
        tb_lista_provas = soup.find('table',  id="lista_provas")
        if tb_lista_provas:
            print(f"Tabela encontrada! {url}")
            dados = getDados(tb_lista_provas)
            #print(dados)
            insert_psql(dados, banca)
        else:
            print(f"Tabela não encontrada.")
            exit()

def insert_psql(dados:list, banca:str):
  # Conexão com o banco
  conn = getReturn.getConnection()
  cur = conn.cursor()

  # Inserção dos dados
  for item in dados:
      cur.execute("""
          INSERT INTO concursos_all (url, cargo, ano, orgao, instituicao, nivel)
          VALUES (%s, %s, %s, %s, %s, %s)
      """, (
          item['URL'],
          item['cargo'],          
          item['Ano'],
          item['Órgão'],
          item['Instituição'],
          item['Nível']
      ))

  # Confirma e fecha
  conn.commit()
  cur.close()
  conn.close()

def getDados(tb_lista_provas):
    linhas = tb_lista_provas.find_all('tr')
    cabecalhos = [cell.get_text(strip=True) for cell in linhas[0].find_all(['th', 'td'])]
    cabecalhos[0] = 'URL'

    dados = []
    for linha in linhas[1:]:
        colunas = linha.find_all(['td', 'th'])
        if colunas:
            linha_dados = {}
            for i, cell in enumerate(colunas):
                if i >= len(cabecalhos):
                    continue  # Evita erro se tiver mais colunas do que cabeçalhos
                texto = cell.get_text(strip=True)
                if i == 0:
                    texto=cell.find('a')['href']
                    linha_dados['cargo'] = cell.get_text(strip=True)
                linha_dados[cabecalhos[i]] = texto
            dados.append(linha_dados)
    return dados

# fazer_busca_prova('fcc')
# fazer_busca_prova('CEBRASPE')
fazer_busca_prova('vunesp')
#fazer_busca_prova('fgv')



# 
# CREATE TABLE concursos_all (
#     id SERIAL PRIMARY KEY,
#     url TEXT,
#     cargo TEXT,
#     ano VARCHAR(4),
#     orgao TEXT,
#     instituicao TEXT,
#     nivel TEXT
# );
