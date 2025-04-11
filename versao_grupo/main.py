from email_graph import DirectedWeightedGraph
from email_parser import build_graph_from_emails
import os
import time

def main():
    # Caminho para a base de dados Enron
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.abspath(os.path.join(current_dir, 'Amostra Enron - 2016'))
    print(dataset_path)
    
    print("Construindo grafo a partir dos emails...")
    start_time = time.time()
    
    # Constrói o grafo a partir dos emails
    graph = DirectedWeightedGraph()
    graph = build_graph_from_emails(graph, dataset_path)
    
    print(f"Grafo construído em {time.time() - start_time:.2f} segundos")
    
    # Salva a lista de adjacências no arquivo
    print("Salvando lista de adjacências...")
    graph.save_adjacency_list("adjacency_list.txt")
    print("Lista de adjacências salva em 'adjacency_list.txt'")
    
    # Tarefa 2: Extrai informações gerais
    print("\n--- INFORMAÇÕES GERAIS DO GRAFO ---")
    print(f"a. Número de vértices (ordem): {graph.get_order()}")
    print(f"b. Número de arestas (tamanho): {graph.get_size()}")
    print(f"c. Número de vértices isolados: {len(graph.get_isolated_vertices())}")
    
    # Top 20 indivíduos por grau de saída
    print("\nd. Top 20 indivíduos por grau de saída:")
    for i, (email, degree) in enumerate(graph.get_top_out_degrees(), 1):
        print(f"   {i}. {email}: {degree}")
    
    # Top 20 indivíduos por grau de entrada
    print("\ne. Top 20 indivíduos por grau de entrada:")
    for i, (email, degree) in enumerate(graph.get_top_in_degrees(), 1):
        print(f"   {i}. {email}: {degree}")
    
    # Tarefa 3: Verifica se o grafo é Euleriano
    print("\n--- VERIFICAÇÃO DE GRAFO EULERIANO ---")
    is_eulerian, conditions = graph.is_eulerian()
    print(f"O grafo é Euleriano? {is_eulerian}")
    if not is_eulerian:
        print("Condições não satisfeitas:")
        for condition in conditions[:10]:  # Mostra apenas as 10 primeiras condições para não sobrecarregar a saída
            print(f"  - {condition}")
        if len(conditions) > 10:
            print(f"  ... e mais {len(conditions) - 10} condições.")
    
    # Tarefa 4: Exemplo de obtenção de vértices dentro de uma distância
    print("\n--- VERTICES DENTRO DE UMA DISTÂNCIA D ---")
    if graph.vertices:
        example_vertex = "hoytm@hughesluce.com"
        max_distance = 10
        print(f"Vértices dentro da distância {max_distance} do vértice {example_vertex}:")
        vertices_within_distance = graph.get_vertices_within_distance(example_vertex, max_distance)
        for i, (vertex, distance) in enumerate(vertices_within_distance[:20], 1):  # Mostra apenas os 20 primeiros para não sobrecarregar a saída
            print(f"   {i}. {vertex}: {distance}")
        if len(vertices_within_distance) > 20:
            print(f"   ... e mais {len(vertices_within_distance) - 20} vértices.")
    
    # Tarefa 5: Calcula o diâmetro
    print("\n--- DIÂMETRO DO GRAFO ---")
    print("Calculando o diâmetro...")
    start_time = time.time()
    diameter, path = graph.get_diameter()
    print(f"Diâmetro calculado em {time.time() - start_time:.2f} segundos")
    print(f"Diâmetro do grafo: {diameter}")
    print(f"Caminho: {path}")

if __name__ == "__main__":
    main()
