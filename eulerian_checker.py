#!/usr/bin/env python3
"""
Verificador de Ciclo Euleriano

Este script verifica se um grafo é Euleriano (possui um ciclo Euleriano).
Para um grafo direcionado ser Euleriano:
1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado
2. Para cada vertice, o grau de entrada deve ser igual ao grau de saída

Uso:
    python eulerian_checker.py
"""

from collections import defaultdict, Counter, deque
from email_graph import build_email_graph


def calculate_degrees(graph):
    """
    Calcula os graus de entrada e saída para todos os vértices do grafo.
    
    Args:
        graph: O grafo representado como uma lista de adjacência
        
    Returns:
        tuple: (active_vertices, in_degrees, out_degrees)
            - active_vertices: conjunto de vértices com grau não-zero
            - in_degrees: dicionário com graus de entrada
            - out_degrees: dicionário com graus de saída
    """
    active_vertices = set()
    in_degrees = Counter()
    out_degrees = {}
    
    # Calcula graus de entrada e identifica vértices ativos
    for sender in graph:
        active_vertices.add(sender)
        for recipient, weight in graph[sender].items():
            active_vertices.add(recipient)
            in_degrees[recipient] += weight
    
    # Calcula graus de saída
    for sender in graph:
        out_degrees[sender] = sum(graph[sender].values())
    
    return active_vertices, in_degrees, out_degrees


def find_unbalanced_vertices(active_vertices, in_degrees, out_degrees):
    """
    Encontra vértices onde o grau de entrada é diferente do grau de saída.
    
    Args:
        active_vertices: conjunto de vértices com grau não-zero
        in_degrees: dicionário com graus de entrada
        out_degrees: dicionário com graus de saída
        
    Returns:
        list: Lista de tuplas (node, in_degree, out_degree) para vértices desbalanceados
    """
    unbalanced = []
    for node in active_vertices:
        in_degree = in_degrees[node]
        out_degree = out_degrees.get(node, 0)
        
        if in_degree != out_degree:
            unbalanced.append((node, in_degree, out_degree))
    
    return unbalanced


def find_strongly_connected_components(graph, active_vertices):
    """
    Encontra componentes fortemente conectados usando o algoritmo de Kosaraju.
    
    Args:
        graph: O grafo representado como uma lista de adjacência
        active_vertices: conjunto de vértices com grau não-zero
        
    Returns:
        list: Lista de componentes fortemente conectados (cada componente é uma lista de vértices)
    """
    # Passo 1: Realiza DFS e armazena vértices em ordem de tempo de finalização
    visited = set()
    finishing_order = []
    
    def dfs_first_pass(node):
        visited.add(node)
        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                dfs_first_pass(neighbor)
        finishing_order.append(node)
    
    # Executa DFS em todos os vértices
    for node in active_vertices:
        if node not in visited:
            dfs_first_pass(node)
    
    # Passo 2: Cria o grafo transposto (inverte todas as arestas)
    transposed_graph = defaultdict(dict)
    for sender in graph:
        for recipient, weight in graph[sender].items():
            transposed_graph[recipient][sender] = weight
    
    # Passo 3: Realiza DFS no grafo transposto em ordem de tempo de finalização
    visited.clear()
    components = []
    
    def dfs_second_pass(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in transposed_graph.get(node, {}):
            if neighbor not in visited:
                dfs_second_pass(neighbor, component)
    
    # Processa vértices em ordem inversa de tempo de finalização
    for node in reversed(finishing_order):
        if node not in visited:
            component = []
            dfs_second_pass(node, component)
            components.append(component)
    
    return components


def filter_non_zero_components(components, in_degrees, out_degrees):
    """
    Filtra componentes que contêm pelo menos um vértice com grau não-zero.
    
    Args:
        components: Lista de componentes fortemente conectados
        in_degrees: dicionário com graus de entrada
        out_degrees: dicionário com graus de saída
        
    Returns:
        list: Lista de componentes com pelo menos um vértice de grau não-zero
    """
    non_zero_components = []
    
    for component in components:
        for node in component:
            if in_degrees[node] > 0 or out_degrees.get(node, 0) > 0:
                non_zero_components.append(component)
                break
    
    return non_zero_components


def check_eulerian(graph):
    """
    Verifica se o grafo é Euleriano (possui um ciclo Euleriano).
    
    Para um grafo direcionado ser Euleriano:
    1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado
    2. Para cada vertice, o grau de entrada deve ser igual ao grau de saída
    
    Args:
        graph: O grafo representado como uma lista de adjacência
        
    Returns:
        bool: True se o grafo é Euleriano, False caso contrário
        list: Lista de condições que não foram satisfeitas (vazia se Euleriano)
    """
    # Calcula graus e identifica vértices ativos
    active_vertices, in_degrees, out_degrees = calculate_degrees(graph)
    
    # Verifica condição 2: grau de entrada igual ao grau de saída
    unbalanced_vertices = find_unbalanced_vertices(active_vertices, in_degrees, out_degrees)
    
    # Verifica condição 1: todos os vértices com grau não-zero pertencem a um único componente
    components = find_strongly_connected_components(graph, active_vertices)
    non_zero_components = filter_non_zero_components(components, in_degrees, out_degrees)
    
    # Prepara a lista de condições não satisfeitas
    unsatisfied_conditions = []
    
    if len(non_zero_components) > 1:
        unsatisfied_conditions.append(f"O grafo possui {len(non_zero_components)} componentes fortemente conectados, quando deveria ter apenas 1 para ser Euleriano. Isso significa que existem grupos de vértices isolados entre si, impossibilitando um ciclo completo.")
    
    if unbalanced_vertices:
        unsatisfied_conditions.append(f"Existem {len(unbalanced_vertices)} vértices onde grau de entrada != grau de saída")
        # Inclui detalhes para até 5 vértices desbalanceados como exemplos
        for i, (node, in_deg, out_deg) in enumerate(unbalanced_vertices[:5]):
            unsatisfied_conditions.append(f"  Exemplo {i+1}: {node} (grau de entrada: {in_deg}, grau de saída: {out_deg})")
        if len(unbalanced_vertices) > 5:
            unsatisfied_conditions.append(f"  ... e mais {len(unbalanced_vertices) - 5} vértices desbalanceados")
    
    return len(unsatisfied_conditions) == 0, unsatisfied_conditions


def check_eulerian_cycle(graph):
    """
    Verifica se o grafo tem um ciclo Euleriano e imprime os resultados.
    
    Args:
        graph: O grafo representado como uma lista de adjacência
        
    Returns:
        bool: True se o grafo é Euleriano, False caso contrário
        list: Lista de condições que não foram satisfeitas
    """
    is_eulerian, unsatisfied_conditions = check_eulerian(graph)
    
    if is_eulerian:
        print("O grafo é Euleriano (possui um ciclo Euleriano).")
        print("\nUm ciclo Euleriano é um caminho que percorre cada aresta exatamente uma vez e retorna ao vertice inicial.")
        print("Isso significa que você pode traçar o grafo inteiro sem levantar o lápis e voltar ao ponto de partida.")
    else:
        print("O grafo NÃO é Euleriano.")
        print("\nCondições não satisfeitas:")
        for condition in unsatisfied_conditions:
            print(f"- {condition}")
        
        print("\nExplicação das condições para um grafo direcionado ser Euleriano:")
        print("1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado.")
        print("   Isso significa que você pode alcançar qualquer vertice a partir de qualquer outro vertice no grafo.")
        print("2. Para cada vertice, o grau de entrada deve ser igual ao grau de saída.")
        print("   Isso significa que cada vertice deve ter o mesmo número de arestas de entrada e saída.")
    
    return is_eulerian, unsatisfied_conditions


def main():
    """Função principal para executar o verificador de ciclo Euleriano."""
    # Constrói o grafo de emails
    print("Construindo grafo de emails...")
    graph, all_emails = build_email_graph()
    
    if graph:
        print(f"Grafo construído com sucesso com {len(graph)} vértices.")
        # Verifica se o grafo é Euleriano
        check_eulerian_cycle(graph)
    else:
        print("Falha ao construir o grafo.")


if __name__ == "__main__":
    main()
