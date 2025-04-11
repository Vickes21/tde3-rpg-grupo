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

def verificar_euleriano(grafo):
    """
    Verifica se o grafo é Euleriano (possui um ciclo Euleriano).
    
    Para um grafo direcionado ser Euleriano:
    1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado
    2. Para cada nó, o grau de entrada deve ser igual ao grau de saída
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        
    Returns:
        bool: True se o grafo é Euleriano, False caso contrário
        list: Lista de condições que não foram satisfeitas (vazia se Euleriano)
    """
    # Obtém todos os vértices que têm arestas de entrada ou saída
    vertices_ativos = set()
    
    # Calcula o grau de entrada para cada nó
    graus_entrada = Counter()
    for remetente in grafo:
        vertices_ativos.add(remetente)
        for destinatario, peso in grafo[remetente].items():
            vertices_ativos.add(destinatario)
            graus_entrada[destinatario] += peso
    
    # Calcula o grau de saída para cada nó
    graus_saida = {}
    for remetente in grafo:
        graus_saida[remetente] = sum(grafo[remetente].values())
    
    # Verifica condição 2: grau de entrada igual ao grau de saída para todos os vértices
    vertices_desbalanceados = []
    for no in vertices_ativos:
        grau_entrada = graus_entrada[no]
        grau_saida = graus_saida.get(no, 0)
        
        if grau_entrada != grau_saida:
            vertices_desbalanceados.append((no, grau_entrada, grau_saida))
    
    # Verifica condição 1: todos os vértices com grau não-zero pertencem a um único componente fortemente conectado
    # Usaremos o algoritmo de Kosaraju para encontrar componentes fortemente conectados
    
    # Passo 1: Realiza DFS e armazena vértices em ordem de tempo de finalização
    visitados = set()
    ordem_finalizacao = []
    
    def dfs_primeira_passagem(no):
        """Realiza a primeira passagem DFS para o algoritmo de Kosaraju."""
        visitados.add(no)
        for vizinho in grafo.get(no, {}):
            if vizinho not in visitados:
                dfs_primeira_passagem(vizinho)
        ordem_finalizacao.append(no)
    
    # Executa DFS em todos os vértices
    for no in vertices_ativos:
        if no not in visitados:
            dfs_primeira_passagem(no)
    
    # Passo 2: Cria o grafo transposto (inverte todas as arestas)
    grafo_transposto = defaultdict(dict)
    for remetente in grafo:
        for destinatario, peso in grafo[remetente].items():
            grafo_transposto[destinatario][remetente] = peso
    
    # Passo 3: Realiza DFS no grafo transposto em ordem de tempo de finalização
    visitados = set()
    componentes = []
    
    def dfs_segunda_passagem(no, componente):
        """Realiza a segunda passagem DFS para o algoritmo de Kosaraju."""
        visitados.add(no)
        componente.append(no)
        for vizinho in grafo_transposto.get(no, {}):
            if vizinho not in visitados:
                dfs_segunda_passagem(vizinho, componente)
    
    # Processa vértices em ordem inversa de tempo de finalização
    for no in reversed(ordem_finalizacao):
        if no not in visitados:
            componente = []
            dfs_segunda_passagem(no, componente)
            componentes.append(componente)
    
    # Verifica se há mais de um componente fortemente conectado com vértices de grau não-zero
    componentes_nao_zero = []
    for componente in componentes:
        tem_nao_zero = False
        for no in componente:
            if graus_entrada[no] > 0 or graus_saida.get(no, 0) > 0:
                tem_nao_zero = True
                break
        if tem_nao_zero:
            componentes_nao_zero.append(componente)
    
    # Prepara a lista de condições não satisfeitas
    condicoes_nao_satisfeitas = []
    
    if len(componentes_nao_zero) > 1:
        condicoes_nao_satisfeitas.append(f"O grafo tem {len(componentes_nao_zero)} componentes fortemente conectados em vez de 1")
    
    if vertices_desbalanceados:
        condicoes_nao_satisfeitas.append(f"Existem {len(vertices_desbalanceados)} vértices onde grau de entrada != grau de saída")
        # Inclui detalhes para até 5 vértices desbalanceados como exemplos
        for i, (no, grau_ent, grau_sai) in enumerate(vertices_desbalanceados[:5]):
            condicoes_nao_satisfeitas.append(f"  Exemplo {i+1}: {no} (grau de entrada: {grau_ent}, grau de saída: {grau_sai})")
        if len(vertices_desbalanceados) > 5:
            condicoes_nao_satisfeitas.append(f"  ... e mais {len(vertices_desbalanceados) - 5} vértices desbalanceados")
    
    return len(condicoes_nao_satisfeitas) == 0, condicoes_nao_satisfeitas

def verificar_ciclo_euleriano(grafo):
    """
    Verifica se o grafo tem um ciclo Euleriano e imprime os resultados.
    
    Args:
        grafo: O grafo representado como uma lista de adjacência
        
    Returns:
        bool: True se o grafo é Euleriano, False caso contrário
        list: Lista de condições que não foram satisfeitas
    """
    e_euleriano, condicoes_nao_satisfeitas = verificar_euleriano(grafo)
    
    if e_euleriano:
        print("O grafo é Euleriano (possui um ciclo Euleriano).")
        print("\nUm ciclo Euleriano é um caminho que percorre cada aresta exatamente uma vez e retorna ao nó inicial.")
        print("Isso significa que você pode traçar o grafo inteiro sem levantar o lápis e voltar ao ponto de partida.")
    else:
        print("O grafo NÃO é Euleriano.")
        print("\nCondições não satisfeitas:")
        for condicao in condicoes_nao_satisfeitas:
            print(f"- {condicao}")
        
        print("\nExplicação das condições para um grafo direcionado ser Euleriano:")
        print("1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado.")
        print("   Isso significa que você pode alcançar qualquer nó a partir de qualquer outro nó no grafo.")
        print("2. Para cada nó, o grau de entrada deve ser igual ao grau de saída.")
        print("   Isso significa que cada nó deve ter o mesmo número de arestas de entrada e saída.")
    
    return e_euleriano, condicoes_nao_satisfeitas

def main():
    """Função principal para executar o verificador de ciclo Euleriano."""
    # Constrói o grafo de emails
    print("Construindo grafo de emails...")
    grafo, todos_emails = build_email_graph()
    
    if grafo:
        print(f"Grafo construído com sucesso com {len(grafo)} vértices.")
        # Verifica se o grafo é Euleriano
        verificar_ciclo_euleriano(grafo)
    else:
        print("Falha ao construir o grafo.")

if __name__ == "__main__":
    main()
