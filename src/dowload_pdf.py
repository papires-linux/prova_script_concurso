import requests
import src.getReturn as getReturn
from bs4 import BeautifulSoup

def download_pdf(nome_arquivo:str, url:str, filename:str, destino:str):
    response = requests.get(url)
    if response.status_code == 200:
        path_end = f"{destino}/{nome_arquivo}__{filename}.pdf" 
        print(path_end)
        with open(path_end, 'wb') as file:
            file.write(response.content)
        print(f"Download completo! {url}")


def download_provas(url: str):
    headers = getReturn.getHeaders()

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Garante que a resposta foi bem-sucedida
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    download_section = soup.find('ul', class_="pdf_download")
    file_base_name = url.split("/")[-1]

    if not download_section:
        print("Seção de downloads não encontrada na página.")
        return

    links = download_section.find_all('a')

    if len(links) >= 1:
        prova_url = links[0].get('href')
        if prova_url:
            download_pdf(file_base_name, prova_url, "prova", 'pdf')
        else:
            print("Link da prova não encontrado.")
    else:
        print("Sem download de prova.")

    if len(links) >= 2:
        gabarito_url = links[1].get('href')
        if gabarito_url:
            download_pdf(file_base_name, gabarito_url, "gabarito", 'pdf')
        else:
            print("Link do gabarito não encontrado.")
    else:
        print("Sem download de gabarito.")

    getReturn.getUpdateDownload(url)

