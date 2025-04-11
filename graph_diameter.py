#!/usr/bin/env python3
"""
Calculador de Diâmetro de Grafo

Este script calcula o diâmetro do grafo de emails, que é o caminho mais longo entre
quaisquer dois vértices no grafo. Retorna tanto o valor do diâmetro quanto o
caminho correspondente que representa esta distância máxima.

Por simplicidade, esta implementação ignora o fato de que o caminho mais curto entre
vértices em componentes conectados diferentes seria infinito.
"""

import time
import heapq
from email_graph import build_email_graph

def dijkstra_with_path(graph, start_node):
    """
    Executa o algoritmo de Dijkstra para encontrar os caminhos mais curtos do no_inicial para todos os outros vertices.
    Esta versão também mantém o registro dos caminhos reais.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        no_inicial: O vertice inicial
        
    Returns:
        tuple: (distancias, caminhos) onde:
            - distancias é um dicionário mapeando vertice -> distância mais curta a partir do no_inicial
            - caminhos é um dicionário mapeando vertice -> lista de vertices representando o caminho mais curto
    """
    # Obtém todos os vertices no grafo, incluindo aqueles que aparecem apenas como vizinhos
    all_nodes = set(graph.keys())
    for node in graph:
        for neighbor in graph[node]:
            all_nodes.add(neighbor)
    
    # Inicializa distâncias com infinito para todos os vertices, exceto o vertice inicial
    distances = {node: float('infinity') for node in all_nodes}
    distances[start_node] = 0
    
    # Inicializa dicionário de caminhos para armazenar o caminho mais curto para cada vertice
    paths = {node: [] for node in all_nodes}
    paths[start_node] = [start_node]
    
    # Fila de prioridade para o algoritmo de Dijkstra
    # Cada entrada é (distância, vertice)
    priority_queue = [(0, start_node)]
    
    # Processa os vertices em ordem crescente de distância
    while priority_queue:
        # Obtém o vertice com a menor distância
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Se já encontramos um caminho mais curto para este vertice, ignoramos
        if current_distance > distances[current_node]:
            continue
        
        # Verifica todos os vizinhos do vertice atual
        for neighbor, weight in graph.get(current_node, {}).items():
            # Calcula a distância para o vizinho através do vertice atual
            distance = current_distance + weight
            
            # Se encontramos um caminho mais curto para o vizinho, atualizamos
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Atualiza o caminho para o vizinho
                paths[neighbor] = paths[current_node] + [neighbor]
                # Adiciona o vizinho à fila de prioridade
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, paths

def calculate_graph_diameter(graph, all_emails=None):
    """
    Calcula o diâmetro do grafo, que é o caminho mais longo entre
    qualquer par de vértices.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        all_emails: Conjunto opcional de todos os endereços de email (vértices)
        
    Returns:
        tuple: (diametro, caminho, origem, destino) onde:
            - diametro é o valor do caminho mais longo mais curto
            - caminho é a lista de vertices representando este caminho
            - origem é o vertice inicial do caminho
            - destino é o vertice final do caminho
    """
    start_time = time.time()
    
    # Inicializa variáveis para rastrear a distância máxima e o caminho correspondente
    max_distance = 0
    max_path = []
    max_source = None
    max_target = None
    
    # Contador para acompanhamento do progresso
    total_active_nodes = len(graph)
    processed_nodes = 0
    
    if all_emails:
        print(f"Calculando diâmetro para um grafo com {total_active_nodes} vértices ativos (de um total de {len(all_emails)} endereços únicos)...")
    else:
        print(f"Calculando diâmetro para um grafo com {total_active_nodes} vértices...")
    
    # Para cada vertice no grafo, encontra os caminhos mais curtos para todos os outros vertices
    for source in graph:
        # Pula vertices sem arestas de saída
        if not graph[source]:
            processed_nodes += 1
            continue
            
        # Encontra os caminhos mais curtos desta origem para todos os outros vertices
        distances, paths = dijkstra_with_path(graph, source)
        
        # Encontra a distância finita máxima a partir desta origem
        for target, distance in distances.items():
            # Pula vertices inalcançáveis (distância infinita) e auto-loops
            if distance == float('infinity') or source == target:
                continue
                
            # Se esta distância for maior que nosso máximo atual, atualizamos
            if distance > max_distance:
                max_distance = distance
                max_path = paths[target]
                max_source = source
                max_target = target
        
        # Atualiza o progresso
        processed_nodes += 1
        if processed_nodes % 10 == 0 or processed_nodes == total_active_nodes:
            elapsed_time = time.time() - start_time
            print(f"Processados {processed_nodes}/{total_active_nodes} vertices ({processed_nodes/total_active_nodes*100:.1f}%) - Tempo decorrido: {elapsed_time:.2f}s")
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\nCálculo do diâmetro concluído em {execution_time:.2f} segundos")
    
    return max_distance, max_path, max_source, max_target

def print_diameter_results(diameter, path, source, target, execution_time, graph):
    """
    Imprime os resultados do cálculo do diâmetro.
    
    Args:
        diametro: O valor do diâmetro
        caminho: O caminho representando o diâmetro
        origem: O vertice de origem do caminho
        destino: O vertice de destino do caminho
        tempo_execucao: Tempo gasto para executar o cálculo
        grafo: O grafo representado como uma lista de adjacência
    """
    print("\n" + "="*80)
    print(f"RESULTADOS DO DIÂMETRO DO GRAFO")
    print("="*80)
    print(f"Diâmetro: {diameter}")
    print(f"vertice de origem: {source}")
    print(f"vertice de destino: {target}")
    print(f"Comprimento do caminho: {len(path)} vertices")
    print(f"Tempo de execução: {execution_time:.2f} segundos")
    print("\nCaminho:")
    print("-"*80)
    
    # Imprime o caminho com os pesos das arestas
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i+1]
        weight = graph[current][next_node]
        print(f"{i+1}. {current} -> {next_node} (peso: {weight})")
    
    print("="*80)

def main():
    """
    Função principal para executar o calculador de diâmetro do grafo.
    """
    start_time = time.time()
    
    # Constrói o grafo de emails
    print("Construindo grafo de emails...")
    graph, all_emails = build_email_graph()
    
    # Calcula o diâmetro do grafo
    print("Calculando diâmetro do grafo...")
    diameter, path, source, target = calculate_graph_diameter(graph, all_emails)
    
    # Calcula o tempo de execução
    execution_time = time.time() - start_time
    
    # Imprime os resultados
    print_diameter_results(diameter, path, source, target, execution_time, graph)

if __name__ == "__main__":
    main()
