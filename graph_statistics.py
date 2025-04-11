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

def verificar_ordem_grafo(grafo, todos_emails):
    """
    Verifica a ordem do grafo (número de vértices) usando múltiplos métodos.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        todos_emails: Conjunto de todos os endereços de email no conjunto de dados
        
    Returns:
        dict: Dicionário com diferentes contagens de vértices para comparação
    """
    # Método 1: Usando o conjunto todos_emails
    ordem_de_todos_emails = len(todos_emails)
    
    # Método 2: Conta remetentes e destinatários únicos
    remetentes_unicos = set(grafo.keys())
    destinatarios_unicos = set()
    for remetente in grafo:
        for destinatario in grafo[remetente]:
            destinatarios_unicos.add(destinatario)
    
    vertices_unicos = remetentes_unicos | destinatarios_unicos
    ordem_do_grafo = len(vertices_unicos)
    
    # Método 3: Conta vértices isolados e adiciona aos vértices com arestas
    qtd_isolados, vertices_isolados = get_isolated_vertices(grafo, todos_emails)
    vertices_com_arestas = len(vertices_unicos)
    ordem_de_isolados = vertices_com_arestas + qtd_isolados
    
    # Retorna todas as contagens para comparação
    return {
        "ordem_de_todos_emails": ordem_de_todos_emails,
        "ordem_do_grafo": ordem_do_grafo,
        "ordem_de_isolados": ordem_de_isolados,
        "vertices_com_arestas": vertices_com_arestas,
        "vertices_isolados": qtd_isolados
    }

def exibir_estatisticas_grafo():
    """
    Calcula e exibe várias estatísticas sobre o grafo de emails.
    
    Esta função constrói o grafo de emails e calcula diversas métricas
    importantes para análise, como número de vértices, arestas, vértices
    isolados e os nós com maior grau de entrada e saída.
    """
    print("Construindo grafo de emails...")
    grafo, todos_emails = build_email_graph()
    
    print("\n=== ESTATÍSTICAS DO GRAFO ===\n")
    
    # Verifica a ordem do grafo usando múltiplos métodos
    verificacao_ordem = verificar_ordem_grafo(grafo, todos_emails)
    
    print("Verificação do número de vértices (ordem):")
    print(f"  - Método 1 (todos_emails): {verificacao_ordem['ordem_de_todos_emails']}")
    print(f"  - Método 2 (remetentes + destinatários): {verificacao_ordem['ordem_do_grafo']}")
    print(f"  - Método 3 (com arestas + isolados): {verificacao_ordem['ordem_de_isolados']}")
    print(f"  - Vértices com arestas: {verificacao_ordem['vertices_com_arestas']}")
    print(f"  - Vértices isolados: {verificacao_ordem['vertices_isolados']}")
    print()
    
    # a. Número de vértices (ordem)
    ordem = get_graph_order(grafo, todos_emails)
    print(f"a. Número de vértices (ordem): {ordem}")
    
    # b. Número de arestas (tamanho)
    tamanho = get_graph_size(grafo)
    print(f"b. Número de arestas (tamanho): {tamanho}")
    
    # c. Número de vértices isolados
    qtd_isolados, vertices_isolados = get_isolated_vertices(grafo, todos_emails)
    print(f"c. Número de vértices isolados: {qtd_isolados}")
    
    # Imprime alguns exemplos de vértices isolados para verificação
    if qtd_isolados > 0:
        print(f"   Exemplos de vértices isolados (até 10):")
        for i, no in enumerate(list(vertices_isolados)[:10], 1):
            print(f"   {i}. {no}")
    
    # d. Top 20 indivíduos com maior grau de saída
    print("\nd. Top 20 indivíduos com maior grau de saída (número de emails enviados):")
    top_saida = get_top_out_degrees(grafo, 20)
    for i, (no, grau) in enumerate(top_saida, 1):
        print(f"   {i:2d}. {no}: {grau}")
    
    # e. Top 20 indivíduos com maior grau de entrada
    print("\ne. Top 20 indivíduos com maior grau de entrada (número de emails recebidos):")
    top_entrada = get_top_in_degrees(grafo, 20)
    for i, (no, grau) in enumerate(top_entrada, 1):
        print(f"   {i:2d}. {no}: {grau}")

if __name__ == "__main__":
    exibir_estatisticas_grafo()
