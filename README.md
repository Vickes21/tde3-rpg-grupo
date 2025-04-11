# Análise de Grafo de Emails

Este projeto implementa um conjunto de ferramentas para análise de um grafo de emails, onde os vértices são endereços de email e as arestas representam emails enviados entre eles. O peso das arestas representa a frequência de comunicação.

## Requisitos

- Python 3.6 ou superior
- Conjunto de dados de emails no diretório `/home/hower/studies/2025/rpg/tde1-grupos/dataset`

## Estrutura do Projeto

O projeto é dividido em cinco etapas principais, cada uma implementada em um script Python separado:

1. **Criação da Lista de Adjacência** (`create_adj_list.py`)
2. **Estatísticas do Grafo** (`graph_statistics.py`)
3. **Verificação de Ciclo Euleriano** (`eulerian_checker.py`)
4. **Busca por Distância** (`distance_finder.py`)
5. **Cálculo do Diâmetro do Grafo** (`graph_diameter.py`)

Além disso, o projeto inclui um módulo de utilidades (`email_graph.py`) que contém funções comuns utilizadas por todos os scripts.

## Como Usar

### 1. Criação da Lista de Adjacência

Este script constrói o grafo de emails a partir do conjunto de dados e salva a lista de adjacência em um arquivo de texto.

```bash
python create_adj_list.py
```

**Saída:**
- Um arquivo de texto (`email_graph_adjacency_list.txt`) contendo a lista de adjacência do grafo.
- Cada linha representa uma conexão entre remetente e destinatário com seu respectivo peso.

### 2. Estatísticas do Grafo

Este script calcula e exibe várias estatísticas sobre o grafo de emails, incluindo número de vértices, arestas, vértices isolados e os indivíduos com maior grau de entrada e saída.

```bash
python graph_statistics.py
```

**Saída:**
- Número de vértices (ordem)
- Número de arestas (tamanho)
- Número de vértices isolados
- Top 20 indivíduos com maior grau de saída (número de emails enviados)
- Top 20 indivíduos com maior grau de entrada (número de emails recebidos)

### 3. Verificação de Ciclo Euleriano

Este script verifica se o grafo é Euleriano (possui um ciclo Euleriano). Para um grafo direcionado ser Euleriano:
1. Todos os vértices com grau não-zero devem pertencer a um único componente fortemente conectado
2. Para cada vertice, o grau de entrada deve ser igual ao grau de saída

```bash
python eulerian_checker.py
```

**Saída:**
- Indicação se o grafo é Euleriano ou não
- Se não for Euleriano, lista de condições que não foram satisfeitas
- Explicação das condições para um grafo direcionado ser Euleriano

### 4. Busca por Distância

Este script encontra todos os vértices dentro de uma distância especificada a partir de um vertice inicial. Utiliza o algoritmo de Dijkstra para encontrar os caminhos mais curtos.

```bash
python distance_finder.py <email_inicial> <distancia_maxima>
```

**Parâmetros:**
- `<email_inicial>`: Endereço de email do vertice inicial (ex: john.doe@example.com)
- `<distancia_maxima>`: Distância máxima para busca (valor numérico)

**Exemplo:**
```bash
python distance_finder.py drew.fossum@enron.com 50
```

**Saída:**
- Lista de todos os vértices (endereços de email) que estão dentro da distância especificada
- Distância de cada vértice em relação ao vertice inicial
- Tempo de execução da busca

### 5. Cálculo do Diâmetro do Grafo

Este script calcula o diâmetro do grafo, que é o caminho mais longo entre qualquer par de vértices. Retorna tanto o valor do diâmetro quanto o caminho correspondente.

```bash
python graph_diameter.py
```

**Saída:**
- Valor do diâmetro do grafo
- Caminho que representa o diâmetro (sequência de vertices)
- vertice de origem e vertice de destino do caminho
- Comprimento do caminho (número de vertices)
- Tempo de execução do cálculo

## Exemplo de Fluxo de Trabalho

Para uma análise completa do grafo de emails, você pode seguir este fluxo de trabalho:

1. Gere a lista de adjacência:
   ```bash
   python create_adj_list.py
   ```

2. Analise as estatísticas básicas do grafo:
   ```bash
   python graph_statistics.py
   ```

3. Verifique se o grafo possui um ciclo Euleriano:
   ```bash
   python eulerian_checker.py
   ```

4. Explore os vértices próximos a um vertice específico:
   ```bash
   python distance_finder.py drew.fossum@enron.com 50
   ```

5. Calcule o diâmetro do grafo:
   ```bash
   python graph_diameter.py
   ```

## Notas Adicionais

- O cálculo do diâmetro pode ser computacionalmente intensivo para grafos grandes, pois requer o cálculo dos caminhos mais curtos entre todos os pares de vértices.
- A implementação ignora o fato de que os caminhos entre componentes conectados diferentes seriam infinitos, para simplificar a análise.
- Todos os scripts incluem medição de tempo de execução para avaliar a performance.

## Resultados

Com base na análise do conjunto de dados de emails da Enron:

- O grafo possui 2127 vértices (endereços de email)
- O grafo possui 3340 arestas (emails enviados)
- O diâmetro do grafo é 212, representado pelo caminho:
  stephanie.harris@enron.com → james.derrick@enron.com → j.harris@enron.com → erica.braden@enron.com
