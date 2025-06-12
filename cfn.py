import os
import unicodedata
import re
import csv

def normalizar_nome_arquivo(nome):
    nome = unicodedata.normalize('NFD', nome)
    nome = nome.encode('ascii', 'ignore').decode('utf-8')

    nome = nome.replace(" ", "_").replace("-","_")
    nome = re.sub(r'[^\w._]', '', nome)

    return nome.lower()

def renomear_arquivos_pasta(caminho_pasta):
    registros = []
    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        if os.path.isfile(caminho_completo):
            novo_nome = normalizar_nome_arquivo(nome_arquivo)
            novo_caminho = os.path.join(caminho_pasta, novo_nome)
            registros.append((nome_arquivo, novo_nome))
            if novo_caminho != caminho_completo and not os.path.exists(novo_caminho):
                os.rename(caminho_completo, novo_caminho)
                print(f'Renomeado: {nome_arquivo} → {novo_nome}')
            else:
                print(f'Skipped (Conflito ou igual): {nome_arquivo}')

    caminho_csv = os.path.join(caminho_pasta,'Lista.csv')
    with open(caminho_csv,'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['arquivo_original', 'arquivo_renomeado'])
        writer.writerows(registros)
    print(f'\nCSV gerado: {caminho_csv}')

