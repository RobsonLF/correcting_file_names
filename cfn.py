import os
import unicodedata
import re
import csv

def normalizar_nome_arquivo(nome):
    # Remove acentos
    nome = unicodedata.normalize('NFD', nome)
    nome = nome.encode('ascii', 'ignore').decode('utf-8')

    # Substitui espaços e hífens por "_"
    nome = nome.replace(" ", "_").replace("-", "_")

    # Remove caracteres especiais, mantendo letras, números, "_" e "."
    nome = re.sub(r'[^\w._]', '', nome)

    # Converte para minúsculas
    return nome.lower()

def renomear_arquivos_pasta(caminho_pasta):
    registros = []

    for nome_arquivo in os.listdir(caminho_pasta):
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

        if os.path.isfile(caminho_completo):
            novo_nome = normalizar_nome_arquivo(nome_arquivo)
            novo_caminho = os.path.join(caminho_pasta, novo_nome)

            registros.append((nome_arquivo, novo_nome))

            # Renomeia apenas se for diferente e não houver conflito
            if novo_caminho != caminho_completo and not os.path.exists(novo_caminho):
                os.rename(caminho_completo, novo_caminho)
                print(f'Renomeado: {nome_arquivo} → {novo_nome}')
            else:
                print(f'Skipped (conflito ou igual): {nome_arquivo}')

    # Gera CSV
    caminho_csv = os.path.join(caminho_pasta, 'renomeacoes.csv')
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['arquivo_original', 'arquivo_renomeado'])
        writer.writerows(registros)

    print(f'\nCSV gerado: {caminho_csv}')


renomear_arquivos_pasta()
# Exemplo de uso
# renomear_arquivos_pasta(r'C:\caminho\para\sua\pasta')


