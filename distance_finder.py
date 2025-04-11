#!/usr/bin/env python3
"""
Distance Finder

This script finds all vertices within a specified distance D from a node N in the email graph.
It uses Dijkstra's algorithm to efficiently find the shortest paths, making it suitable for
graphs with thousands of vertices and edges.
"""

# Importação das bibliotecas necessárias
import sys          # Para acessar argumentos da linha de comando e funções do sistema
import time         # Para medir o tempo de execução do algoritmo
from collections import defaultdict  # Para criar dicionários com valores padrão
from email_graph import build_email_graph, nodes_within_distance  # Importa funções do módulo email_graph

def find_vertices_within_distance(graph, start_node, max_distance):
    """
    Find all vertices within a specified distance from a starting node.
    
    Args:
        graph: The graph represented as an adjacency list
        start_node: The starting node (email address)
        max_distance: Maximum distance (sum of weights along the path)
        
    Returns:
        dict: Dictionary mapping node -> distance from start_node
              Only includes vertices within max_distance
    """
    # Registra o tempo de início para medir a performance
    start_time = time.time()
    
    # Chama a implementação do algoritmo de Dijkstra do módulo email_graph.py
    # Esta função encontra todos os vértices (endereços de email) que estão a uma distância
    # menor ou igual a max_distance do vértice inicial (start_node)
    result = nodes_within_distance(graph, start_node, max_distance)
    
    # Registra o tempo de término e calcula a duração da execução
    end_time = time.time()
    
    # Retorna o resultado (dicionário de vértices e suas distâncias) e o tempo de execução
    return result, end_time - start_time

def print_results(result, execution_time, start_node, max_distance):
    """
    Print the results of the distance search.
    
    Args:
        result: Dictionary mapping node -> distance from start_node
        execution_time: Time taken to execute the search
        start_node: The starting node
        max_distance: Maximum distance used for the search
    """
    # Imprime cabeçalho com informações sobre a busca realizada
    print(f"\nVertices within distance {max_distance} from {start_node}:")
    print(f"Found {len(result)} vertices in {execution_time:.4f} seconds\n")
    
    # Ordena os resultados por distância (do mais próximo ao mais distante)
    # sorted() retorna uma lista de tuplas (vértice, distância) ordenada pela distância
    sorted_results = sorted(result.items(), key=lambda x: x[1])
    
    # Imprime os resultados em formato de tabela
    # Cria uma tabela com 40 colunas para o vértice e 10 colunas para a distância
    # :<40 e :<10.2f são formatadores de string que alinham o texto à esquerda
    print(f"{'Node':<40} {'Distance':<10}")
    print("-" * 50)
    
    # Itera sobre cada vértice e sua distância, formatando a saída
    for node, distance in sorted_results:
        print(f"{node:<40} {distance:<10.2f}")

def main():
    """
    Main function to run the distance finder.
    """
    # Verifica se foram fornecidos os argumentos corretos na linha de comando
    if len(sys.argv) != 3:
        # Se não, exibe instruções de uso e encerra o programa
        print("Usage: python distance_finder.py <start_node> <max_distance>")
        print("Example: python distance_finder.py john.doe@example.com 10")
        return
    
    # Extrai e processa os argumentos da linha de comando
    # Converte o endereço de email para minúsculas para garantir consistência
    start_node = sys.argv[1].lower()
    try:
        # Tenta converter o segundo argumento para um número de ponto flutuante
        max_distance = float(sys.argv[2])
    except ValueError:
        # Se a conversão falhar, exibe mensagem de erro e encerra o programa
        print("Error: max_distance must be a number")
        return
    
    # Informa ao usuário que o grafo está sendo construído
    print("Building email graph...")
    # Constrói o grafo de emails a partir dos dados do dataset
    # graph: dicionário que representa o grafo como lista de adjacência
    # all_emails: conjunto de todos os endereços de email no dataset
    graph, all_emails = build_email_graph()
    
    # Verifica se o vértice inicial existe no grafo
    if start_node not in all_emails:
        # Se não existir, exibe mensagem de erro e encerra o programa
        print(f"Error: Start node '{start_node}' not found in the graph")
        return
    
    # Informa ao usuário que a busca está sendo realizada
    print(f"Finding vertices within distance {max_distance} from {start_node}...")
    # Executa a busca por vértices dentro da distância especificada
    result, execution_time = find_vertices_within_distance(graph, start_node, max_distance)
    
    # Imprime os resultados da busca
    print_results(result, execution_time, start_node, max_distance)

# Verifica se este arquivo está sendo executado diretamente (não importado como módulo)
if __name__ == "__main__":
    # Se sim, executa a função principal
    main()
