#!/usr/bin/env python3
"""
Verificador de Ciclo Euleriano

Este script verifica se um grafo é Euleriano (possui um ciclo Euleriano).
Para um grafo direcionado ser Euleriano:
1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado
2. Para cada nó, o grau de entrada deve ser igual ao grau de saída

Uso:
    python eulerian_checker.py
"""

from collections import defaultdict, Counter
from email_graph import build_email_graph

def check_eulerian(graph):
    """
    Verifica se o grafo é Euleriano (possui um ciclo Euleriano).
    
    Para um grafo direcionado ser Euleriano:
    1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado
    2. Para cada nó, o grau de entrada deve ser igual ao grau de saída
    
    Args:
        graph: O grafo representado como uma lista de adjacência
        
    Returns:
        bool: True se o grafo é Euleriano, False caso contrário
        list: Lista de condições que não foram satisfeitas (vazia se Euleriano)
    """
    # Obtém todos os vértices que têm arestas de entrada ou saída
    active_vertices = set()
    
    # Calcula o grau de entrada para cada nó
    in_degrees = Counter()
    for sender in graph:
        active_vertices.add(sender)
        for recipient, weight in graph[sender].items():
            active_vertices.add(recipient)
            in_degrees[recipient] += weight
    
    # Calcula o grau de saída para cada nó
    out_degrees = {}
    for sender in graph:
        out_degrees[sender] = sum(graph[sender].values())
    
    # Verifica condição 2: grau de entrada igual ao grau de saída para todos os vértices
    unbalanced_vertices = []
    for node in active_vertices:
        in_degree = in_degrees[node]
        out_degree = out_degrees.get(node, 0)
        
        if in_degree != out_degree:
            unbalanced_vertices.append((node, in_degree, out_degree))
    
    # Verifica condição 1: todos os vértices com grau não-zero pertencem a um único componente fortemente conectado
    # Usaremos o algoritmo de Kosaraju para encontrar componentes fortemente conectados
    
    # Passo 1: Realiza DFS e armazena vértices em ordem de tempo de finalização
    visited = set()
    finishing_order = []
    
    def dfs_first_pass(node):
        """Realiza a primeira passagem DFS para o algoritmo de Kosaraju."""
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
    visited = set()
    components = []
    
    def dfs_second_pass(node, component):
        """Realiza a segunda passagem DFS para o algoritmo de Kosaraju."""
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
    
    # Verifica se há mais de um componente fortemente conectado com vértices de grau não-zero
    non_zero_components = []
    for component in components:
        has_non_zero = False
        for node in component:
            if in_degrees[node] > 0 or out_degrees.get(node, 0) > 0:
                has_non_zero = True
                break
        if has_non_zero:
            non_zero_components.append(component)
    
    # Prepara a lista de condições não satisfeitas
    unsatisfied_conditions = []
    
    if len(non_zero_components) > 1:
        unsatisfied_conditions.append(f"O grafo tem {len(non_zero_components)} componentes fortemente conectados em vez de 1")
    
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
        print("\nUm ciclo Euleriano é um caminho que percorre cada aresta exatamente uma vez e retorna ao nó inicial.")
        print("Isso significa que você pode traçar o grafo inteiro sem levantar o lápis e voltar ao ponto de partida.")
    else:
        print("O grafo NÃO é Euleriano.")
        print("\nCondições não satisfeitas:")
        for condition in unsatisfied_conditions:
            print(f"- {condition}")
        
        print("\nExplicação das condições para um grafo direcionado ser Euleriano:")
        print("1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado.")
        print("   Isso significa que você pode alcançar qualquer nó a partir de qualquer outro nó no grafo.")
        print("2. Para cada nó, o grau de entrada deve ser igual ao grau de saída.")
        print("   Isso significa que cada nó deve ter o mesmo número de arestas de entrada e saída.")
    
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
