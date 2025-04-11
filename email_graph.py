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
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, 'dataset')
DATASET_DIR = dataset_path

def extract_email_addresses(line):
    """
    Extrai endereços de email de uma linha de texto.
    
    Args:
        line: A linha de texto a ser analisada
        
    Returns:
        list: Lista de endereços de email encontrados na linha
    """
    # Expressão regular para encontrar endereços de email
    email_pattern = r'[\w][\w\.-]*@[\w\.-]+'
    emails = re.findall(email_pattern, line)
    
    # Filtrar emails que possam ter começado com um ponto (caso a regex ainda capture algum)
    valid_emails = [email for email in emails if not email.startswith('.')]
    
    return valid_emails

def process_email_file(file_path):
    """
    Processa um único arquivo de email e extrai o remetente e os destinatários.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de email
        
    Returns:
        tuple: (remetente, destinatários) onde:
            - remetente é o endereço de email do remetente
            - destinatários é uma lista de endereços de email dos destinatários
    """
    sender = None
    recipients = []
    
    try:
        # Abre o arquivo para leitura
        with open(file_path, 'r', encoding='latin1') as file:
            for line in file:
                # Remove espaços em branco no início e no final da linha
                line = line.strip()
                
                # Extrai o remetente
                if line.startswith('From:'):
                    sender_emails = extract_email_addresses(line)
                    if sender_emails:
                        sender = sender_emails[0].lower()
                
                # Extrai os destinatários (To, Cc, Bcc)
                elif line.startswith('To:'):
                    # Extrai os endereços de email
                    to_emails = extract_email_addresses(line)
                    # Adiciona os endereços de email à lista de destinatários
                    recipients.extend([email.lower() for email in to_emails])
                
                # Pula o resto do arquivo uma vez que processamos os cabeçalhos
                if line == '':
                    break
    
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")
        return None, []
    
    return sender, recipients

def build_email_graph():
    """
    Constrói um grafo direcionado ponderado a partir de dados de email.
    
    Returns:
        tuple: (grafo, todos_emails) onde:
            - grafo é um dicionário representando o grafo como uma lista de adjacência com pesos
            - todos_emails é um conjunto de todos os endereços de email (vértices)
    """
    # Grafo representado como uma lista de adjacência com pesos
    graph = defaultdict(lambda: defaultdict(int))
    
    # Conjunto para manter o controle de todos os endereços de email (vértices)
    all_emails = set()
    
    # Contador para acompanhamento do progresso
    total_emails_processed = 0
    
    # Processa todos os diretórios nomeados
    for named_directory in os.listdir(DATASET_DIR):
        # Cria o caminho completo para o diretório
        named_path = os.path.join(DATASET_DIR, named_directory)
        
        # Verifica se o caminho é um diretório
        if not os.path.isdir(named_path):
            # Se não for, pula para o próximo
            continue
        
        print(f"Processando diretório nomeado: {named_directory}")
        
        # Processa todas as pastas de email para este diretório nomeado
        for folder in os.listdir(named_path):
            # Cria o caminho completo para a pasta
            folder_path = os.path.join(named_path, folder)
            
            # Verifica se o caminho é uma pasta
            if not os.path.isdir(folder_path):
                # Se não for, pula para o próximo
                continue
            
            # Processa todos os arquivos de email nesta pasta
            for email_file in glob.glob(os.path.join(folder_path, '*')):
                # Verifica se o caminho é um arquivo
                if os.path.isfile(email_file):
                    # Processa o arquivo de email
                    sender, recipients = process_email_file(email_file)
                    
                    # Adiciona o remetente ao conjunto de todos os emails, se existir
                    if sender:
                        all_emails.add(sender)
                    
                    # Adiciona os destinatários ao conjunto de todos os emails, se existirem
                    if recipients:
                        all_emails.update(recipients)
                    
                    # Atualiza o grafo: incrementa o peso para cada aresta remetente->destinatário
                    # Apenas se tanto o remetente quanto os destinatários existirem
                    if sender and recipients:
                        for recipient in recipients:
                            # Adiciona aresta com peso 1 entre o remetente e o destinatário
                            graph[sender][recipient] += 1
                    
                    total_emails_processed += 1
                    
                    # Imprime o progresso a cada 1000 emails
                    if total_emails_processed % 1000 == 0:
                        print(f"Processados {total_emails_processed} emails...")
    
    print(f"Total de emails processados: {total_emails_processed}")
    print(f"Total de endereços de email únicos: {len(all_emails)}")
    
    return graph, all_emails

def save_adjacency_list(graph, file_name, all_emails=None):
    """
    Salva o grafo como uma lista de adjacência em um arquivo de texto.
    
    Esta função exporta a estrutura do grafo de emails para um arquivo texto formatado,
    onde cada linha representa uma conexão entre remetente e destinatário com seu respectivo peso.
    
    Args:
        grafo: Dicionário representando o grafo, onde as chaves são os remetentes
               e os valores são dicionários com destinatários como chaves e pesos como valores.
        nome_arquivo: Caminho do arquivo onde a lista de adjacência será salva.
        all_emails: Conjunto opcional de todos os endereços de email (vértices), incluindo nós isolados.
    """
    # Abre o arquivo no modo de escrita usando um gerenciador de contexto (with)
    with open(file_name, 'w') as file:
        # Escreve o cabeçalho do arquivo para documentar o formato
        file.write("# Lista de Adjacência do Grafo de Email\n")
        file.write("# Formato: remetente -> destinatário: peso\n\n")
        
        # Identifica todos os nós que precisam ser incluídos
        nodes_to_include = set(graph.keys())
        
        # Se all_emails foi fornecido, adiciona os nós isolados
        if all_emails:
            nodes_to_include.update(all_emails)
        
        # Ordena os nós em ordem alfabética para melhorar a legibilidade
        for node in sorted(nodes_to_include):
            file.write(f"Node: {node}\n")
            
            # Se o nó está no grafo (não é isolado), escreve suas conexões
            if node in graph:
                # Ordena os destinatários primeiro por peso (decrescente) e depois alfabeticamente
                sorted_recipients = sorted(
                    graph[node].items(),
                    key=lambda x: (-x[1], x[0])  # Ordena por peso (decrescente) e depois por destinatário (crescente)
                )
                
                # Escreve cada conexão com seu respectivo peso
                for recipient, weight in sorted_recipients:
                    file.write(f"  -> {recipient}: {weight}\n")
            
            # Adiciona uma linha em branco entre diferentes nós para melhor organização
            file.write("\n")

def get_graph_order(graph, all_emails):
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
    return len(all_emails)

def get_graph_size(graph):
    """
    Obtém o número de arestas no grafo (tamanho).
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        
    Returns:
        int: Número de arestas
    """
    # O tamanho do grafo é o número de arestas
    # Contamos todas as conexões no grafo
    size = 0
    for sender in graph:
        size += len(graph[sender])
    return size

def get_isolated_vertices(graph, all_emails):
    """
    Obtém o número de vértices isolados no grafo.
    Um vertice isolado não tem arestas de entrada ou saída.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        todos_emails: Conjunto de todos os endereços de email no conjunto de dados
        
    Returns:
        tuple: (num_isolados, vertices_isolados) onde:
            - num_isolados é o número de vértices isolados
            - vertices_isolados é um conjunto de vértices isolados
    """
    # Encontra todos os vértices que têm arestas de entrada ou saída
    vertices_with_edges = set(graph.keys())  # Vértices com arestas de saída
    
    # Adiciona vértices com arestas de entrada
    for sender in graph:
        for recipient in graph[sender]:
            vertices_with_edges.add(recipient)
    
    # Os vértices isolados são aqueles que não têm arestas de entrada ou saída
    isolated_vertices = all_emails - vertices_with_edges
    
    return len(isolated_vertices), isolated_vertices

def get_top_out_degrees(graph, n=20):
    """
    Obtém os N vértices com o maior grau de saída.
    O grau de saída é o número de arestas de saída de um vertice.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        n: Número de vértices principais a serem retornados
        
    Returns:
        list: Lista de tuplas (vertice, grau_saida) ordenada por grau_saida em ordem decrescente
    """
    # Calcula o grau de saída para cada vertice
    out_degrees = {}
    for sender in graph:
        out_degrees[sender] = len(graph[sender])
    
    # Ordena os vertices por grau de saída em ordem decrescente
    top_out_degrees = sorted(out_degrees.items(), key=lambda x: (-x[1], x[0]))
    
    # Retorna os N principais
    return top_out_degrees[:n]

def get_top_in_degrees(graph, n=20):
    """
    Obtém os N vértices com o maior grau de entrada.
    O grau de entrada é o número de arestas de entrada para um vertice.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        n: Número de vértices principais a serem retornados
        
    Returns:
        list: Lista de tuplas (vertice, grau_entrada) ordenada por grau_entrada em ordem decrescente
    """
    # Calcula o grau de entrada para cada vertice
    in_degrees = Counter()
    for sender in graph:
        for recipient in graph[sender]:
            in_degrees[recipient] += 1
    
    # Ordena os vertices por grau de entrada em ordem decrescente
    top_in_degrees = sorted(in_degrees.items(), key=lambda x: (-x[1], x[0]))
    
    # Retorna os N principais
    return top_in_degrees[:n]

def nodes_within_distance(graph, start_node, max_distance):
    """
    Encontra todos os vertices que estão dentro de uma distância especificada a partir de um vertice inicial.
    Usa o algoritmo de Dijkstra para encontrar os caminhos mais curtos.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        no_inicial: O vertice inicial
        distancia_maxima: Distância máxima (soma dos pesos ao longo do caminho)
        
    Returns:
        dict: Dicionário mapeando vertice -> distância a partir do no_inicial
              Inclui apenas vertices dentro da distancia_maxima
    """
    # Inicializa distâncias com infinito para todos os vertices
    distances = {start_node: 0}
    
    # Fila de prioridade para o algoritmo de Dijkstra
    # Cada entrada é (distância, vertice)
    priority_queue = [(0, start_node)]
    
    # vertices dentro da distância máxima
    nodes_within_dist = {}
    
    # Processa vertices em ordem crescente de distância
    while priority_queue:
        # Obtém o vertice com a menor distância
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Se já encontramos um caminho mais curto para este vertice, ignoramos
        if current_node in nodes_within_dist:
            continue
        
        # Adiciona este vertice ao resultado se estiver dentro da distância máxima
        if current_distance <= max_distance:
            nodes_within_dist[current_node] = current_distance
        else:
            # Se a distância atual exceder a distância máxima, podemos parar
            # porque todos os vertices subsequentes na fila de prioridade terão distâncias ainda maiores
            break
        
        # Verifica todos os vizinhos do vertice atual
        for neighbor, weight in graph.get(current_node, {}).items():
            # Calcula a distância para o vizinho através do vertice atual
            distance = current_distance + weight
            
            # Se o vizinho ainda não foi processado e a distância está dentro do limite
            if neighbor not in nodes_within_dist and distance <= max_distance:
                # Adiciona o vizinho à fila de prioridade
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return nodes_within_dist