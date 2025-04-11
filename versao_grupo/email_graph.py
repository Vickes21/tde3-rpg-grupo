import os
import re
import heapq
from collections import deque

class DirectedWeightedGraph:
    def __init__(self):
        # Grafo representado como uma lista de adjacência com pesos
        self.adjacency_list = defaultdict(lambda: defaultdict(int))
        self.vertices = set()     # Conjunto de todos os vértices (endereços de email)
    
    def add_vertex(self, vertex):
        """Adiciona um novo vértice ao grafo se ele não existir."""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency_list[vertex] = {}
    
    def add_edge(self, sender, recipient):
        """Adiciona uma aresta do remetente para o destinatário e incrementa o peso."""
        # Adiciona vértices se eles não existirem
        self.add_vertex(sender)
        self.add_vertex(recipient)
        
        # Atualiza o peso da aresta (frequência)
        if recipient in self.adjacency_list[sender]:
            self.adjacency_list[sender][recipient] += 1
        else:
            self.adjacency_list[sender][recipient] = 1
    
    def save_adjacency_list(self, filename):
        """Salva a lista de adjacências em um arquivo."""
        with open(filename, 'w', encoding='utf-8') as file:
            for vertex in sorted(self.adjacency_list.keys()):
                file.write(f"{vertex}:")
                for neighbor, weight in sorted(self.adjacency_list[vertex].items()):
                    file.write(f" {neighbor}({weight})")
                file.write("\n")
    
    def get_order(self):
        """Retorna o número de vértices (ordem do grafo)."""
        return len(self.vertices)
    
    def get_size(self):
        """Retorna o número de arestas (tamanho do grafo)."""
        edge_count = 0
        for vertex in self.adjacency_list:
            edge_count += len(self.adjacency_list[vertex])
        return edge_count
    
    def get_isolated_vertices(self):
        """Retorna uma lista de vértices isolados (sem arestas de entrada ou saída)."""
        isolated = []
        for vertex in self.vertices:
            has_outgoing = len(self.adjacency_list[vertex]) > 0
            has_incoming = any(vertex in self.adjacency_list[v] for v in self.vertices)
            if not has_outgoing and not has_incoming:
                isolated.append(vertex)
        return isolated
    
    def get_out_degrees(self):
        """Retorna um dicionário com vértice como chave e grau de saída como valor."""
        out_degrees = {}
        for vertex in self.vertices:
            out_degrees[vertex] = len(self.adjacency_list[vertex].values())
        return out_degrees
    
    def get_in_degrees(self):
        """Retorna um dicionário com vértice como chave e grau de entrada como valor."""
        in_degrees = {vertex: 0 for vertex in self.vertices}
        for vertex in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[vertex].items():
                in_degrees[neighbor] += weight
        return in_degrees
    
    def get_top_out_degrees(self, n=20):
        """Retorna os n vértices com maior grau de saída."""
        out_degrees = self.get_out_degrees()
        return sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def get_top_in_degrees(self, n=20):
        """Retorna os n vértices com maior grau de entrada."""
        in_degrees = self.get_in_degrees()
        return sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:n]
    
    def is_eulerian(self):
        """
        Verifica se o grafo é Euleriano.
        Um grafo direcionado é Euleriano se:
        1. Todos os vértices têm graus de entrada e saída iguais
        2. Todos os vértices com grau não zero estão em um mesmo componente fortemente conexo
        
        Retorna:
            bool: True se o grafo é Euleriano, False caso contrário
            list: Lista de condições não satisfeitas se o grafo não for Euleriano
        """
        conditions_not_met = []
        
        # Verifica se todos os vértices têm graus de entrada e saída iguais
        in_degrees = self.get_in_degrees()
        out_degrees = self.get_out_degrees()
        
        for vertex in self.vertices:
            if in_degrees[vertex] != out_degrees[vertex]:
                conditions_not_met.append(f"Vértice {vertex} tem grau de entrada {in_degrees[vertex]} e grau de saída {out_degrees[vertex]}")
        
        # Verifica se todos os vértices com grau não zero estão em um mesmo componente fortemente conexo
        if not conditions_not_met:
            non_zero_vertices = [v for v in self.vertices if in_degrees[v] > 0 or out_degrees[v] > 0]
            if non_zero_vertices:
                # Verifica se todos os vértices não zero são fortemente conectados
                scc = self.get_strongly_connected_components()
                non_zero_scc = [component for component in scc if any(v in component for v in non_zero_vertices)]
                
                if len(non_zero_scc) > 1:
                    conditions_not_met.append("O grafo possui múltiplos componentes fortemente conectados com vértices de grau não zero")
        
        return (len(conditions_not_met) == 0), conditions_not_met
    
    def get_strongly_connected_components(self):
        """
        Encontra todos os componentes fortemente conectados no grafo.
        
        Retorna:
            list: Lista de conjuntos, onde cada conjunto contém vértices em um componente fortemente conectado
        """
        # Passo 1: Realizar DFS e registrar tempos de término (ordem)
        visited = set()
        finish_order = []
        
        def dfs_finish(vertex):
            visited.add(vertex)
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    dfs_finish(neighbor)
            finish_order.append(vertex)
        
        for vertex in self.vertices:
            if vertex not in visited:
                dfs_finish(vertex)
        
        # Passo 2: Criar grafo reverso
        reversed_graph = DirectedWeightedGraph()
        for vertex in self.vertices:
            reversed_graph.add_vertex(vertex)
        
        for vertex in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[vertex].items():
                reversed_graph.add_edge(neighbor, vertex)
        
        # Passo 3: Realizar DFS no grafo reverso na ordem dos tempos de término
        visited.clear()
        components = []
        
        def dfs_component(vertex, component):
            visited.add(vertex)
            component.add(vertex)
            for neighbor in reversed_graph.adjacency_list[vertex]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)
        
        for vertex in reversed(finish_order):
            if vertex not in visited:
                component = set()
                dfs_component(vertex, component)
                components.append(component)
        
        return components
    
    def get_vertices_within_distance(self, start_vertex, max_distance):
        """
        Encontra todos os vértices dentro de uma certa distância do vértice inicial.
        Usa o algoritmo de Dijkstra para encontrar os caminhos mais curtos.
        
        Args:
            start_vertex: O vértice inicial
            max_distance: A distância máxima a considerar
            
        Retorna:
            list: Lista de tuplas (vértice, distância) para vértices dentro de max_distance
        """
        if start_vertex not in self.vertices:
            return []
        
        # Inicializa distâncias
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0
        
        # Fila de prioridade para o algoritmo de Dijkstra
        pq = [(0, start_vertex)]
        
        # Conjunto para manter registro de vértices processados
        processed = set()
        
        while pq:
            current_distance, current_vertex = heapq.heappop(pq)
            
            # Se já processamos este vértice, ignoramos
            if current_vertex in processed:
                continue
            
            processed.add(current_vertex)
            
            # Se a distância atual for maior que max_distance, podemos parar
            if current_distance > max_distance:
                continue
            
            # Verifica todos os vizinhos
            for neighbor, weight in self.adjacency_list[current_vertex].items():
                distance = current_distance + weight
                
                # Se encontramos um caminho mais curto, atualizamos a distância
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        # Retorna todos os vértices com distância <= max_distance
        results = []
        for vertex in self.vertices:
            if distances[vertex] <= max_distance:
                results.append((vertex, distances[vertex]))
        
        return sorted(results, key=lambda x: x[1])
    
    def get_diameter(self):
        """
        Calcula o diâmetro do grafo, que é o maior dos caminhos mais curtos entre quaisquer
        pares de vértices. Usa o algoritmo de Floyd-Warshall para encontrar todos os caminhos 
        mais curtos e depois identifica o mais longo deles.

        Em um grafo direcionado, o diâmetro representa a maior distância que uma mensagem
        precisa percorrer entre quaisquer dois nós que possuem um caminho entre si.

        Retorna:
            tuple: Uma tupla contendo o diâmetro (int) e o caminho (string)
        """
        if not self.vertices:
            return 0, "Grafo desconexo ou sem arestas"

        # Inicializa a matriz de distâncias e caminhos
        dist = {}
        next_vertex = {}
        
        # Inicializa todas as distâncias como infinito
        for i in self.vertices:
            dist[i] = {}
            next_vertex[i] = {}
            for j in self.vertices:
                dist[i][j] = float('inf')
                next_vertex[i][j] = None

        # Define distâncias para si mesmo como 0 e inicializa arestas diretas
        for i in self.vertices:
            dist[i][i] = 0
            for j, weight in self.adjacency_list[i].items():
                dist[i][j] = weight
                next_vertex[i][j] = j

        # Algoritmo de Floyd-Warshall - encontra os caminhos mais curtos entre todos os pares
        for k in self.vertices:
            for i in self.vertices:
                for j in self.vertices:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]

        # Encontra o diâmetro (a maior distância finita entre quaisquer dois vértices)
        diameter = 0
        start, end = None, None
        
        for i in self.vertices:
            for j in self.vertices:
                if i != j and dist[i][j] < float('inf') and dist[i][j] > diameter:
                    diameter = dist[i][j]
                    start, end = i, j

        # Se não encontrou diâmetro entre vértices conectados
        if start is None or end is None:
            return 0, "Grafo desconexo ou sem arestas"

        # Reconstrói o caminho correspondente ao diâmetro
        path = [start]
        current = start
        while current != end:
            current = next_vertex[current][end]
            path.append(current)

        path_str = " --> ".join(path) + f", peso total: {diameter}"
        return diameter, path_str
