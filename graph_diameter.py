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

def dijkstra_com_caminho(grafo, no_inicial):
    """
    Executa o algoritmo de Dijkstra para encontrar os caminhos mais curtos do no_inicial para todos os outros nós.
    Esta versão também mantém o registro dos caminhos reais.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        no_inicial: O nó inicial
        
    Returns:
        tuple: (distancias, caminhos) onde:
            - distancias é um dicionário mapeando nó -> distância mais curta a partir do no_inicial
            - caminhos é um dicionário mapeando nó -> lista de nós representando o caminho mais curto
    """
    # Obtém todos os nós no grafo, incluindo aqueles que aparecem apenas como vizinhos
    todos_nos = set(grafo.keys())
    for no in grafo:
        for vizinho in grafo[no]:
            todos_nos.add(vizinho)
    
    # Inicializa distâncias com infinito para todos os nós, exceto o nó inicial
    distancias = {no: float('infinity') for no in todos_nos}
    distancias[no_inicial] = 0
    
    # Inicializa dicionário de caminhos para armazenar o caminho mais curto para cada nó
    caminhos = {no: [] for no in todos_nos}
    caminhos[no_inicial] = [no_inicial]
    
    # Fila de prioridade para o algoritmo de Dijkstra
    # Cada entrada é (distância, nó)
    fila_prioridade = [(0, no_inicial)]
    
    # Processa os nós em ordem crescente de distância
    while fila_prioridade:
        # Obtém o nó com a menor distância
        distancia_atual, no_atual = heapq.heappop(fila_prioridade)
        
        # Se já encontramos um caminho mais curto para este nó, ignoramos
        if distancia_atual > distancias[no_atual]:
            continue
        
        # Verifica todos os vizinhos do nó atual
        for vizinho, peso in grafo.get(no_atual, {}).items():
            # Calcula a distância para o vizinho através do nó atual
            distancia = distancia_atual + peso
            
            # Se encontramos um caminho mais curto para o vizinho, atualizamos
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                # Atualiza o caminho para o vizinho
                caminhos[vizinho] = caminhos[no_atual] + [vizinho]
                # Adiciona o vizinho à fila de prioridade
                heapq.heappush(fila_prioridade, (distancia, vizinho))
    
    return distancias, caminhos

def calcular_diametro_grafo(grafo):
    """
    Calcula o diâmetro do grafo, que é o caminho mais longo entre
    qualquer par de vértices.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        
    Returns:
        tuple: (diametro, caminho, origem, destino) onde:
            - diametro é o valor do caminho mais longo mais curto
            - caminho é a lista de nós representando este caminho
            - origem é o nó inicial do caminho
            - destino é o nó final do caminho
    """
    tempo_inicio = time.time()
    
    # Inicializa variáveis para rastrear a distância máxima e o caminho correspondente
    distancia_maxima = 0
    caminho_maximo = []
    origem_maxima = None
    destino_maximo = None
    
    # Contador para acompanhamento do progresso
    total_nos = len(grafo)
    nos_processados = 0
    
    print(f"Calculando diâmetro para um grafo com {total_nos} nós...")
    
    # Para cada nó no grafo, encontra os caminhos mais curtos para todos os outros nós
    for origem in grafo:
        # Pula nós sem arestas de saída
        if not grafo[origem]:
            nos_processados += 1
            continue
            
        # Encontra os caminhos mais curtos desta origem para todos os outros nós
        distancias, caminhos = dijkstra_com_caminho(grafo, origem)
        
        # Encontra a distância finita máxima a partir desta origem
        for destino, distancia in distancias.items():
            # Pula nós inalcançáveis (distância infinita) e auto-loops
            if distancia == float('infinity') or origem == destino:
                continue
                
            # Se esta distância for maior que nosso máximo atual, atualizamos
            if distancia > distancia_maxima:
                distancia_maxima = distancia
                caminho_maximo = caminhos[destino]
                origem_maxima = origem
                destino_maximo = destino
        
        # Atualiza o progresso
        nos_processados += 1
        if nos_processados % 10 == 0 or nos_processados == total_nos:
            tempo_decorrido = time.time() - tempo_inicio
            print(f"Processados {nos_processados}/{total_nos} nós ({nos_processados/total_nos*100:.1f}%) - Tempo decorrido: {tempo_decorrido:.2f}s")
    
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    
    print(f"\nCálculo do diâmetro concluído em {tempo_execucao:.2f} segundos")
    
    return distancia_maxima, caminho_maximo, origem_maxima, destino_maximo

def imprimir_resultados_diametro(diametro, caminho, origem, destino, tempo_execucao, grafo):
    """
    Imprime os resultados do cálculo do diâmetro.
    
    Args:
        diametro: O valor do diâmetro
        caminho: O caminho representando o diâmetro
        origem: O nó de origem do caminho
        destino: O nó de destino do caminho
        tempo_execucao: Tempo gasto para executar o cálculo
        grafo: O grafo representado como uma lista de adjacência
    """
    print("\n" + "="*80)
    print(f"RESULTADOS DO DIÂMETRO DO GRAFO")
    print("="*80)
    print(f"Diâmetro: {diametro}")
    print(f"Nó de origem: {origem}")
    print(f"Nó de destino: {destino}")
    print(f"Comprimento do caminho: {len(caminho)} nós")
    print(f"Tempo de execução: {tempo_execucao:.2f} segundos")
    print("\nCaminho:")
    print("-"*80)
    
    # Imprime o caminho com os pesos das arestas
    for i in range(len(caminho) - 1):
        atual = caminho[i]
        proximo = caminho[i+1]
        peso = grafo[atual][proximo]
        print(f"{i+1}. {atual} -> {proximo} (peso: {peso})")
    
    print("="*80)

def main():
    """
    Função principal para executar o calculador de diâmetro do grafo.
    """
    tempo_inicio = time.time()
    
    # Constrói o grafo de emails
    print("Construindo grafo de emails...")
    grafo, todos_emails = build_email_graph()
    
    # Calcula o diâmetro do grafo
    print("Calculando diâmetro do grafo...")
    diametro, caminho, origem, destino = calcular_diametro_grafo(grafo)
    
    # Calcula o tempo de execução
    tempo_execucao = time.time() - tempo_inicio
    
    # Imprime os resultados
    imprimir_resultados_diametro(diametro, caminho, origem, destino, tempo_execucao, grafo)

if __name__ == "__main__":
    main()
