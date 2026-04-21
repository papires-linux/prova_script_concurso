import requests
import logging
import src.getReturn as getReturn
from bs4 import BeautifulSoup


"""
Este script é responsável por buscar provas de concursos públicos de diferentes bancas examinadoras
no site pciconcursos.com.br, extrair os dados das tabelas HTML e inserir essas informações
no banco de dados PostgreSQL na tabela concursos_all.
"""


def fazer_busca_prova(banca:str):
    """
    Busca provas de uma banca examinadora específica no site pciconcursos.com.br.

    Itera pelas páginas numeradas (de 1 a 998) da URL da banca, encontra a tabela de provas,
    extrai os dados e insere no banco de dados. Para quando não encontra mais tabelas.

    Args:
        banca (str): Nome da banca examinadora (ex: 'fcc', 'vunesp').
    """
    
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
    """
    Insere os dados extraídos das provas no banco de dados PostgreSQL.

    Conecta ao banco, executa inserts na tabela concursos_all para cada item na lista de dados,
    confirma a transação e fecha a conexão.

    Args:
        dados (list): Lista de dicionários contendo os dados das provas.
        banca (str): Nome da banca (usado implicitamente, mas não diretamente na função).
    """
    # Conexão com o banco
    conn = getReturn.getConnection()
    cur = conn.cursor()

    # Inserção dos dados
    for item in dados:
        # print(f"Inserindo item: {item}")
        cur.execute("""
            INSERT INTO concursos_all (url, cargo, ano, orgao, instituicao, nivel)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item['URL'],
            item['cargo'],          
            item['Ano'],
            item['Órgão'],
            item['Organizadora'],
            ""
            # item['Nível']
        ))

    # Confirma e fecha
    conn.commit()
    cur.close()
    conn.close()

def getDados(tb_lista_provas):
    """
    Extrai os dados da tabela HTML de provas.

    Processa as linhas da tabela, obtém os cabeçalhos, e para cada linha de dados,
    cria um dicionário com as informações, incluindo URL do link na primeira coluna.

    Args:
        tb_lista_provas: Objeto BeautifulSoup da tabela HTML.

    Returns:
        list: Lista de dicionários com os dados extraídos.
    """
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



