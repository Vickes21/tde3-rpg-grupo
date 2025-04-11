#!/usr/bin/env python3
"""
Construtor de Grafo de Emails

Este script constrói um grafo direcionado ponderado a partir de um conjunto de dados de emails.
- Os vértices são endereços de email
- As arestas representam emails enviados
- Os pesos das arestas representam a frequência de comunicação
- O grafo é salvo como uma lista de adjacência em um arquivo de texto
"""

import os
import re
from collections import defaultdict, Counter
import glob
import heapq

# Define o diretório do conjunto de dados
DATASET_DIR = "/home/hower/studies/2025/rpg/tde1-grupos/dataset"

def extrair_enderecos_email(linha):
    """
    Extrai endereços de email de uma linha de texto.
    
    Args:
        linha: A linha de texto a ser analisada
        
    Returns:
        list: Lista de endereços de email encontrados na linha
    """
    # Expressão regular para encontrar endereços de email
    padrao_email = r'[\w][\w\.-]*@[\w\.-]+'
    emails = re.findall(padrao_email, linha)
    
    # Filtrar emails que possam ter começado com um ponto (caso a regex ainda capture algum)
    emails_validos = [email for email in emails if not email.startswith('.')]
    
    return emails_validos

def processar_arquivo_email(caminho_arquivo):
    """
    Processa um único arquivo de email e extrai o remetente e os destinatários.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de email
        
    Returns:
        tuple: (remetente, destinatários) onde:
            - remetente é o endereço de email do remetente
            - destinatários é uma lista de endereços de email dos destinatários
    """
    remetente = None
    destinatarios = []
    
    try:
        # Abre o arquivo para leitura
        with open(caminho_arquivo, 'r', encoding='latin1') as arquivo:
            for linha in arquivo:
                # Remove espaços em branco no início e no final da linha
                linha = linha.strip()
                
                # Extrai o remetente
                if linha.startswith('From:'):
                    emails_remetente = extrair_enderecos_email(linha)
                    if emails_remetente:
                        remetente = emails_remetente[0].lower()
                
                # Extrai os destinatários (To, Cc, Bcc)
                elif linha.startswith('To:'):
                    # Extrai os endereços de email
                    emails_para = extrair_enderecos_email(linha)
                    # Adiciona os endereços de email à lista de destinatários
                    destinatarios.extend([email.lower() for email in emails_para])
                
                # Pula o resto do arquivo uma vez que processamos os cabeçalhos
                if linha == '':
                    break
    
    except Exception as e:
        print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")
        return None, []
    
    return remetente, destinatarios

def build_email_graph():
    """
    Constrói um grafo direcionado ponderado a partir de dados de email.
    
    Returns:
        tuple: (grafo, todos_emails) onde:
            - grafo é um dicionário representando o grafo como uma lista de adjacência com pesos
            - todos_emails é um conjunto de todos os endereços de email (vértices)
    """
    # Grafo representado como uma lista de adjacência com pesos
    grafo = defaultdict(lambda: defaultdict(int))
    
    # Conjunto para manter o controle de todos os endereços de email (vértices)
    todos_emails = set()
    
    # Contador para acompanhamento do progresso
    total_emails_processados = 0
    
    # Processa todos os diretórios nomeados
    for diretorio_nomeado in os.listdir(DATASET_DIR):
        # Cria o caminho completo para o diretório
        caminho_nomeado = os.path.join(DATASET_DIR, diretorio_nomeado)
        
        # Verifica se o caminho é um diretório
        if not os.path.isdir(caminho_nomeado):
            # Se não for, pula para o próximo
            continue
        
        print(f"Processando diretório nomeado: {diretorio_nomeado}")
        
        # Processa todas as pastas de email para este diretório nomeado
        for pasta in os.listdir(caminho_nomeado):
            # Cria o caminho completo para a pasta
            caminho_pasta = os.path.join(caminho_nomeado, pasta)
            
            # Verifica se o caminho é uma pasta
            if not os.path.isdir(caminho_pasta):
                # Se não for, pula para o próximo
                continue
            
            # Processa todos os arquivos de email nesta pasta
            for arquivo_email in glob.glob(os.path.join(caminho_pasta, '*')):
                # Verifica se o caminho é um arquivo
                if os.path.isfile(arquivo_email):
                    # Processa o arquivo de email
                    remetente, destinatarios = processar_arquivo_email(arquivo_email)
                    
                    # Adiciona o remetente ao conjunto de todos os emails, se existir
                    if remetente:
                        todos_emails.add(remetente)
                    
                    # Adiciona os destinatários ao conjunto de todos os emails, se existirem
                    if destinatarios:
                        todos_emails.update(destinatarios)
                    
                    # Atualiza o grafo: incrementa o peso para cada aresta remetente->destinatário
                    # Apenas se tanto o remetente quanto os destinatários existirem
                    if remetente and destinatarios:
                        for destinatario in destinatarios:
                            # Adiciona aresta com peso 1 entre o remetente e o destinatário
                            grafo[remetente][destinatario] += 1
                    
                    total_emails_processados += 1
                    
                    # Imprime o progresso a cada 1000 emails
                    if total_emails_processados % 1000 == 0:
                        print(f"Processados {total_emails_processados} emails...")
    
    print(f"Total de emails processados: {total_emails_processados}")
    print(f"Total de endereços de email únicos: {len(todos_emails)}")
    
    return grafo, todos_emails

def save_adjacency_list(grafo, nome_arquivo):
    """
    Salva o grafo como uma lista de adjacência em um arquivo de texto.
    
    Esta função exporta a estrutura do grafo de emails para um arquivo texto formatado,
    onde cada linha representa uma conexão entre remetente e destinatário com seu respectivo peso.
    
    Args:
        grafo: Dicionário representando o grafo, onde as chaves são os remetentes
               e os valores são dicionários com destinatários como chaves e pesos como valores.
        nome_arquivo: Caminho do arquivo onde a lista de adjacência será salva.
    """
    # Abre o arquivo no modo de escrita usando um gerenciador de contexto (with)
    with open(nome_arquivo, 'w') as arquivo:
        # Escreve o cabeçalho do arquivo para documentar o formato
        arquivo.write("# Lista de Adjacência do Grafo de Email\n")
        arquivo.write("# Formato: remetente -> destinatário: peso\n\n")
        
        # Ordena os remetentes em ordem alfabética para melhorar a legibilidade
        for remetente in sorted(grafo.keys()):
            arquivo.write(f"Node: {remetente}\n")
            
            # Ordena os destinatários primeiro por peso (decrescente) e depois alfabeticamente
            destinatarios_ordenados = sorted(
                grafo[remetente].items(),
                key=lambda x: (-x[1], x[0])  # Ordena por peso (decrescente) e depois por destinatário (crescente)
            )
            
            # Escreve cada conexão com seu respectivo peso
            for destinatario, peso in destinatarios_ordenados:
                arquivo.write(f"  -> {destinatario}: {peso}\n")
            
            # Adiciona uma linha em branco entre diferentes remetentes para melhor organização
            arquivo.write("\n")

def get_graph_order(grafo, todos_emails):
    """
    Obtém o número de vértices no grafo (ordem).
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        todos_emails: Conjunto de todos os endereços de email no conjunto de dados
        
    Returns:
        int: Número de vértices
    """
    # A ordem do grafo é o número de vértices
    # Isso inclui todos os endereços de email, mesmo aqueles que não aparecem no grafo
    return len(todos_emails)

def get_graph_size(grafo):
    """
    Obtém o número de arestas no grafo (tamanho).
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        
    Returns:
        int: Número de arestas
    """
    # O tamanho do grafo é o número de arestas
    # Contamos todas as conexões no grafo
    tamanho = 0
    for remetente in grafo:
        tamanho += len(grafo[remetente])
    return tamanho

def get_isolated_vertices(grafo, todos_emails):
    """
    Obtém o número de vértices isolados no grafo.
    Um nó isolado não tem arestas de entrada ou saída.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        todos_emails: Conjunto de todos os endereços de email no conjunto de dados
        
    Returns:
        tuple: (num_isolados, vertices_isolados) onde:
            - num_isolados é o número de vértices isolados
            - vertices_isolados é um conjunto de vértices isolados
    """
    # Encontra todos os vértices que têm arestas de entrada ou saída
    vertices_com_arestas = set(grafo.keys())  # Vértices com arestas de saída
    
    # Adiciona vértices com arestas de entrada
    for remetente in grafo:
        for destinatario in grafo[remetente]:
            vertices_com_arestas.add(destinatario)
    
    # Os vértices isolados são aqueles que não têm arestas de entrada ou saída
    vertices_isolados = todos_emails - vertices_com_arestas
    
    return len(vertices_isolados), vertices_isolados

def get_top_out_degrees(grafo, n=20):
    """
    Obtém os N vértices com o maior grau de saída.
    O grau de saída é o número de arestas de saída de um nó.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        n: Número de vértices principais a serem retornados
        
    Returns:
        list: Lista de tuplas (nó, grau_saida) ordenada por grau_saida em ordem decrescente
    """
    # Calcula o grau de saída para cada nó
    graus_saida = {}
    for remetente in grafo:
        graus_saida[remetente] = len(grafo[remetente])
    
    # Ordena os nós por grau de saída em ordem decrescente
    top_graus_saida = sorted(graus_saida.items(), key=lambda x: (-x[1], x[0]))
    
    # Retorna os N principais
    return top_graus_saida[:n]

def get_top_in_degrees(grafo, n=20):
    """
    Obtém os N vértices com o maior grau de entrada.
    O grau de entrada é o número de arestas de entrada para um nó.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        n: Número de vértices principais a serem retornados
        
    Returns:
        list: Lista de tuplas (nó, grau_entrada) ordenada por grau_entrada em ordem decrescente
    """
    # Calcula o grau de entrada para cada nó
    graus_entrada = Counter()
    for remetente in grafo:
        for destinatario in grafo[remetente]:
            graus_entrada[destinatario] += 1
    
    # Ordena os nós por grau de entrada em ordem decrescente
    top_graus_entrada = sorted(graus_entrada.items(), key=lambda x: (-x[1], x[0]))
    
    # Retorna os N principais
    return top_graus_entrada[:n]

def nodes_within_distance(grafo, no_inicial, distancia_maxima):
    """
    Encontra todos os nós que estão dentro de uma distância especificada a partir de um nó inicial.
    Usa o algoritmo de Dijkstra para encontrar os caminhos mais curtos.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        no_inicial: O nó inicial
        distancia_maxima: Distância máxima (soma dos pesos ao longo do caminho)
        
    Returns:
        dict: Dicionário mapeando nó -> distância a partir do no_inicial
              Inclui apenas nós dentro da distancia_maxima
    """
    # Inicializa distâncias com infinito para todos os nós
    distancias = {no_inicial: 0}
    
    # Fila de prioridade para o algoritmo de Dijkstra
    # Cada entrada é (distância, nó)
    fila_prioridade = [(0, no_inicial)]
    
    # Nós dentro da distância máxima
    nos_dentro_distancia = {}
    
    # Processa nós em ordem crescente de distância
    while fila_prioridade:
        # Obtém o nó com a menor distância
        distancia_atual, no_atual = heapq.heappop(fila_prioridade)
        
        # Se já encontramos um caminho mais curto para este nó, ignoramos
        if no_atual in nos_dentro_distancia:
            continue
        
        # Adiciona este nó ao resultado se estiver dentro da distância máxima
        if distancia_atual <= distancia_maxima:
            nos_dentro_distancia[no_atual] = distancia_atual
        else:
            # Se a distância atual exceder a distância máxima, podemos parar
            # porque todos os nós subsequentes na fila de prioridade terão distâncias ainda maiores
            break
        
        # Verifica todos os vizinhos do nó atual
        for vizinho, peso in grafo.get(no_atual, {}).items():
            # Calcula a distância para o vizinho através do nó atual
            distancia = distancia_atual + peso
            
            # Se o vizinho ainda não foi processado e a distância está dentro do limite
            if vizinho not in nos_dentro_distancia and distancia <= distancia_maxima:
                # Adiciona o vizinho à fila de prioridade
                heapq.heappush(fila_prioridade, (distancia, vizinho))
    
    return nos_dentro_distancia