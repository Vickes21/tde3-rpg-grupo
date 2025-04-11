#!/usr/bin/env python3
"""
Estatísticas do Grafo

Este script calcula e exibe várias estatísticas sobre o grafo de emails:
a. Número de vértices (ordem)
b. Número de arestas (tamanho)
c. Número de vértices isolados
d. Top 20 indivíduos com maior grau de saída
e. Top 20 indivíduos com maior grau de entrada
"""

from email_graph import (
    build_email_graph,
    get_graph_order,
    get_graph_size,
    get_isolated_vertices,
    get_top_out_degrees,
    get_top_in_degrees
)

def check_graph_order(graph, all_emails):
    """
    Verifica a ordem do grafo (número de vértices) usando múltiplos métodos.
    
    Args:
        graph: O grafo representado como uma lista de adjacência
        all_emails: Conjunto de todos os endereços de email no conjunto de dados
        
    Returns:
        dict: Dicionário com diferentes contagens de vértices para comparação
    """
    # Método 1: Usando o conjunto todos_emails
    order_from_all_emails = len(all_emails)
    
    # Método 2: Conta remetentes e destinatários únicos
    unique_senders = set(graph.keys())
    unique_recipients = set()
    for sender in graph:
        for recipient in graph[sender]:
            unique_recipients.add(recipient)
    
    unique_vertices = unique_senders | unique_recipients
    graph_order = len(unique_vertices)
    
    # Método 3: Conta vértices isolados e adiciona aos vértices com arestas
    isolated_count, isolated_vertices = get_isolated_vertices(graph, all_emails)
    vertices_with_edges = len(unique_vertices)
    order_with_isolated = vertices_with_edges + isolated_count
    
    # Retorna todas as contagens para comparação
    return {
        "order_from_all_emails": order_from_all_emails,
        "graph_order": graph_order,
        "order_with_isolated": order_with_isolated,
        "vertices_with_edges": vertices_with_edges,
        "isolated_vertices": isolated_count
    }

def display_graph_statistics():
    """
    Calcula e exibe várias estatísticas sobre o grafo de emails.
    
    Esta função constrói o grafo de emails e calcula diversas métricas
    importantes para análise, como número de vértices, arestas, vértices
    isolados e os vertices com maior grau de entrada e saída.
    """
    print("Construindo grafo de emails...")
    graph, all_emails = build_email_graph()
    
    print("\n=== ESTATÍSTICAS DO GRAFO ===\n")
    
    # Verifica a ordem do grafo usando múltiplos métodos
    order_verification = check_graph_order(graph, all_emails)
    
    print("Verificação do número de vértices (ordem):")
    print(f"  - Método 1 (todos_emails): {order_verification['order_from_all_emails']}")
    print(f"  - Método 2 (remetentes + destinatários): {order_verification['graph_order']}")
    print(f"  - Método 3 (com arestas + isolados): {order_verification['order_with_isolated']}")
    print(f"  - Vértices com arestas: {order_verification['vertices_with_edges']}")
    print(f"  - Vértices isolados: {order_verification['isolated_vertices']}")
    print()
    
    # a. Número de vértices (ordem)
    order = get_graph_order(graph, all_emails)
    print(f"a. Número de vértices (ordem): {order}")
    
    # b. Número de arestas (tamanho)
    size = get_graph_size(graph)
    print(f"b. Número de arestas (tamanho): {size}")
    
    # c. Número de vértices isolados
    isolated_count, isolated_vertices = get_isolated_vertices(graph, all_emails)
    print(f"c. Número de vértices isolados: {isolated_count}")
    
    # Imprime alguns exemplos de vértices isolados para verificação
    if isolated_count > 0:
        print(f"   Exemplos de vértices isolados (até 10):")
        for i, node in enumerate(list(isolated_vertices)[:10], 1):
            print(f"   {i}. {node}")
    
    # d. Top 20 indivíduos com maior grau de saída
    print("\nd. Top 20 indivíduos com maior grau de saída (número de emails enviados):")
    top_out = get_top_out_degrees(graph, 20)
    for i, (node, degree) in enumerate(top_out, 1):
        print(f"   {i:2d}. {node}: {degree}")
    
    # e. Top 20 indivíduos com maior grau de entrada
    print("\ne. Top 20 indivíduos com maior grau de entrada (número de emails recebidos):")
    top_in = get_top_in_degrees(graph, 20)
    for i, (node, degree) in enumerate(top_in, 1):
        print(f"   {i:2d}. {node}: {degree}")

if __name__ == "__main__":
    display_graph_statistics()
