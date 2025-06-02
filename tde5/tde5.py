# Grafo 2 - Ponderado nâo direcionado: Relações entre atores em uma obra
#   Peso é queivalente a quantidade de colaborações em diferentes obras

from collections import defaultdict
from tqdm import tqdm
import pandas as pd
import heapq

class GrafoDirecionado:
    def __init__(self):
      self.grafo = defaultdict(list)
      self.ordem = 0 # Número de vértices no grafo
      self.tamanho = 0 # Número de arestas no grafo

    def adiciona_vertice(self, u):
        if u not in self.grafo:  # Verifica se o vértice já existe
            self.grafo[u] = []  # Adiciona o vértice
            self.ordem += 1

    def adiciona_aresta(self, origem, destino):        
        # Cria os vértices se não existirem
        if origem not in self.grafo:
            self.adiciona_vertice(origem)
        if destino not in self.grafo:
            self.adiciona_vertice(destino)  
            
        # Atualiza o peso se a aresta já existir
        for i in range(len(self.grafo[origem])):
            vertice, _ = self.grafo[origem][i]
            if vertice == destino:
                peso =self.grafo[origem][i][1]
                peso += 1
                self.grafo[origem][i] = (destino, peso)
                return 
            
        # Adiciona a aresta se não existir
        peso = 1
        self.grafo[origem].append((destino, peso))
        self.tamanho += 1   

    def inserir_dados(G):
        df = pd.read_csv("netflix_amazon_disney_titles.csv", usecols=['director','cast'])

        df['director'] = df['director'].str.upper().str.strip()
        df['cast'] = df['cast'].str.upper().str.strip()

        for _, row in df.iterrows():
            diretores = row['director']
            elenco = row['cast']

            if pd.isna(diretores) or pd.isna(elenco):
                continue

            lista_diretores = [d.strip() for d in diretores.split(',')]
            lista_atores = [a.strip() for a in elenco.split(',')]

            for ator in lista_atores:
                for diretor in lista_diretores:
                    G.adiciona_aresta(ator, diretor)


    def imprime_lista_adjacencias(self):   
        final_text = "" 
        for vertice, adjacentes in self.grafo.items():
            text = f'[{vertice}]: '
            edges_text = "" 
            
            for destino, peso in adjacentes:
                edges_text += f'({destino}, {peso}) -> '
            
            if edges_text == "":
                edges_text = "(Nao existem arestas)"
            text = text + edges_text.strip(' -> ')
            final_text += text + "\n"
            print(text)

        # Gera o arquivo grafo.txt
        with open("grafo.txt", "w", encoding="utf-8") as f:
            f.write(final_text)

    # Exercício 2
    def componentes_fortemente_conexos(self):
        def dfs(v, visitado, pilha):
            visitado.add(v)
            for vizinho, _ in self.grafo[v]:
                if vizinho not in visitado:
                    dfs(vizinho, visitado, pilha)
            pilha.append(v)
    
        def dfs_transposto(v, visitado, componente, grafo_transp):
            visitado.add(v)
            componente.append(v)
            for vizinho, _ in grafo_transp[v]:
                if vizinho not in visitado:
                    dfs_transposto(vizinho, visitado, componente, grafo_transp)
    
        def grafo_transposto():
            transposto = GrafoDirecionado()
            for vertice in self.grafo:
                for adjacente, peso in self.grafo[vertice]:
                    transposto.adiciona_aresta(adjacente, vertice)
            return transposto
    
        pilha_tempo = []
        componentes = []
        visitado = set()
    
        # Passo 1: DFS no grafo original para ordem de término
        for vertice in self.grafo:
            if vertice not in visitado:
                dfs(vertice, visitado, pilha_tempo)
    
        # Passo 2: DFS no grafo transposto
        visitado.clear()
        GTransposto = grafo_transposto()
    
        while pilha_tempo:
            vertice = pilha_tempo.pop()
            if vertice not in visitado:
                componente = []
                dfs_transposto(vertice, visitado, componente, GTransposto.grafo)
                componentes.append(componente)
    
        return componentes
    
    #Exercício 4
    def centralidade(self, vertice):
        if vertice not in self.grafo: return 0

        grau_saida = len(self.grafo[vertice])
        grau_entrade = 0

        for vertice in self.grafo:
            for adjacente, _ in self.grafo[vertice]:
                if vertice == adjacente:
                    grau_entrade += 1

        grau_total = grau_saida + grau_entrade
        grau_maximo = 2 * (self.ordem - 1)

        return grau_total / grau_maximo

    #Exercício 5
    def bfs_caminhos_mais_curtos(self, vertice):
        distancias = {}
        caminhos = {}
        visitados = {}  
        for v in self.grafo:
            distancias[v] = float('inf') 
            caminhos[v] = []
            visitados[v] = False
        
        distancias[vertice] = 0
        caminhos[vertice] = [[vertice]]
        visitados[vertice] = True
        fila = [vertice]
        
        while fila:
            current = fila.pop(0)

            for adj, _ in self.grafo[current]:
                if not visitados[adj]:
                    visitados[adj] = True
                    fila.append(adj)    
                if distancias[adj] > distancias[current] + 1:
                    distancias[adj] = distancias[current] + 1
                    caminhos[adj] = [caminho + [adj] for caminho in caminhos[current]]
                elif distancias[adj] == distancias[current] + 1:
                    for caminho in caminhos[current]:
                        if caminho + [adj] not in caminhos[adj]:
                            caminhos[adj].append(caminho + [adj])
        return caminhos    
    
    def intermediacao(self, vertice):
        resultado = 0
        for v in self.grafo:
            caminhos = self.bfs_caminhos_mais_curtos(v)
            for destino in self.grafo:
                if destino == v:
                    continue
                total_caminhos = len(caminhos[destino])
                for caminho in caminhos[destino]:
                    try:
                        idx = caminho.index(vertice)
                        if idx != 0 and idx != len(caminho) - 1:
                            resultado += 1 / total_caminhos
                    except ValueError:
                        continue
    
        if not self.direcionado: return resultado / 2
        return resultado
    
    # Exercício 6
    def centralidade_proximidade(self, vertice):
        if vertice not in self.grafo: return 0

        def bfs(vertice):
            visitado = {vertice: 0}
            fila = [vertice]
            while fila:
                atual = fila.pop(0)
                for vizinho, _ in self.grafo[atual]:
                    if vizinho not in visitado:
                        visitado[vizinho] = visitado[atual] + 1
                        fila.append(vizinho)

            del visitado[vertice]
            return visitado

        distancias = bfs(vertice)
        soma_distancias = sum(distancias.values())
        num_vertices_alcancaveis = len(distancias)
        n_total = len(self.grafo)
        centralidade_bruta = num_vertices_alcancaveis / soma_distancias

        return centralidade_bruta
    
def grafoDirecionado():
    # Exercicio 1
    Grafo1 = GrafoDirecionado()
    GrafoDirecionado.inserir_dados(Grafo1)
    # Grafo1.imprime_lista_adjacencias()
    
    # Exercicio 2
    componentes = Grafo1.componentes_fortemente_conexos()
    print(f"Número componentes fortemente conexos: {len(componentes)}")
    
    # Exercício 4
    centralidade = Grafo1.centralidade("ROBERT DOWNEY JR.")
    print(f"Centralidade do vértice: {centralidade:.2f}")
    
    # Exercício 5
    intermediacao = Grafo1.intermediacao("ROBERT DOWNEY JR.")
    print(f"Centralidade de intermediação do vértice: {intermediacao:.2f}")
    
    # Exercício 6
    proximidade = Grafo1.centralidade_proximidade("YURI LOWENTHAL")
    print(f"Centralidade de proximidade do vértice: {proximidade:.2f}")

class GrafoNaoDirecionado():
    def __init__(self):
        self.grafo = defaultdict(list)
        self.ordem = 0
        self.tamanho = 0 

    def adiciona_vertice(self, u):
        if u not in self.grafo: 
            self.grafo[u] = [] 
            self.ordem += 1

    def adiciona_aresta(self, origem, destino):        
        # Cria os vértices se não existirem
        if origem not in self.grafo:
            self.adiciona_vertice(origem)
        if destino not in self.grafo:
            self.adiciona_vertice(destino)  
            
        # Verifica se a aresta já existe e atualiza o peso
        aresta_existe = False
        
        # Atualiza o peso na lista de adjacência de origem
        for i in range(len(self.grafo[origem])):
            vertice, peso = self.grafo[origem][i]
            if vertice == destino:
                peso += 1
                self.grafo[origem][i] = (destino, peso + 1)
                aresta_existe = True
                break
            
        # Atualiza o peso na lista de adjacência de destino
        if aresta_existe:
            for i in range(len(self.grafo[destino])):
                vertice, peso = self.grafo[destino][i]
                if vertice == origem:
                    peso += 1
                    self.grafo[destino][i] = (origem, peso + 1)
                    break
            return
            
        # Adiciona a aresta se não existir
        peso = 1
        self.grafo[origem].append((destino, peso))
        self.grafo[destino].append((origem, peso))
        self.tamanho += 1

    def inserir_dados(self):
        df = pd.read_csv("netflix_amazon_disney_titles.csv", usecols=['director','cast'])

        df['cast'] = df['cast'].str.upper().str.strip()

        for _, row in df.iterrows():
            elenco = row['cast']
            if pd.isna(elenco): continue

            lista_atores = [a.strip() for a in elenco.split(',')]

            for i in range(len(lista_atores)):
                for j in range(i + 1, len(lista_atores)):
                    self.adiciona_aresta(lista_atores[i], lista_atores[j])

    def imprime_lista_adjacencias(self):   
        final_text = "" 
        for vertice, adjacentes in self.grafo.items():
            text = f'[{vertice}]: '
            edges_text = "" 
            
            for destino, peso in adjacentes:
                edges_text += f'({destino}, {peso}) <-> '
            
            if edges_text == "":
                edges_text = "(Nao existem arestas)"
            text = text + edges_text.strip(' <-> ')
            final_text += text + "\n"
            print(text)

        # Gera o arquivo grafo.txt
        with open("grafo.txt", "w", encoding="utf-8") as f:
            f.write(final_text)

    # Exercício 2
    def componentes_conexos(self):
        visitado = set()
        contador = 0

        for vertice in self.grafo:
            if vertice not in visitado:
                contador += 1

                pilha = [vertice]

                while pilha:
                    v = pilha.pop()
                    if v not in visitado:
                        visitado.add(v)
                        for vizinho, _ in self.grafo[v]:
                            if vizinho not in visitado:
                                pilha.append(vizinho)
        return contador
    
    # Exercício 3
    def arvore_geradora_minima(self, vertice):
        visitados = set()
        visitados.add(vertice)
        arestas = []
        fila = []

        for vizinho, peso in self.grafo[vertice]:
            heapq.heappush(fila, (peso, vertice, vizinho))

        while fila:
            peso, origem, destino = heapq.heappop(fila)
            if destino not in visitados:
                visitados.add(destino)
                arestas.append((origem, destino, peso))
                for vizinho, peso_adj in self.grafo[destino]:
                    if vizinho not in visitados:
                        heapq.heappush(fila, (peso_adj, destino, vizinho))
        return arestas
    
    # Exercício 4
    def centralidade(self, vertice):
        if vertice not in self.grafo: return 0

        grau = len(self.grafo[vertice])
        grau_maximo = 2 * (self.ordem - 1)

        return grau / grau_maximo
    
    def maior_centralidade(self):
        maior = 0
        nome = ''
        for vertice in self.grafo:
            centralidade = self.centralidade(vertice)
            if centralidade > maior:
                maior = centralidade
                nome = vertice
            
        print(f'Maior Centralidade: {nome} -> {maior}')

    # Exercício 5
    def centralidade_intermediacao_brandes(self, vertice):
        if vertice not in self.grafo: return 0.0
        n = len(self.grafo)
        if n <= 2: return 0.0

        vertices = list(self.grafo.keys())
        intermediacao = 0.0

        # Para cada vértice s como origem
        for v in tqdm(vertices):
            if v == vertice:
                continue

            pilha = []
            predecessores = {w: [] for w in vertices}
            caminhos_mais_curtos = {w: 0 for w in vertices} 
            distâncias = {w: -1 for w in vertices}
            dependencias = {w: 0 for w in vertices} 

            caminhos_mais_curtos[v] = 1
            distâncias[v] = 0
            fila_bfs = [v] 

            # BFS
            while fila_bfs:
                v = fila_bfs.pop(0)
                pilha.append(v)

                for v2, _ in self.grafo[v]:
                    if distâncias[v2] < 0:
                        fila_bfs.append(v2)
                        distâncias[v2] = distâncias[v] + 1

                    # Caminho mais curto para v2 via v
                    if distâncias[v2] == distâncias[v] + 1:
                        caminhos_mais_curtos[v2] += caminhos_mais_curtos[v]
                        predecessores[v2].append(v)

            while pilha:
                v2 = pilha.pop()
                for v in predecessores[v2]:
                    dependencias[v] += (caminhos_mais_curtos[v] / caminhos_mais_curtos[v2]) * (1 + dependencias[v2])

            # Soma contribuição para o vértice de interesse
            for v2 in vertices:
                if v2 != v and v2 != vertice:
                    intermediacao += dependencias[v2]

        # Normalizar valor entre 0 e 1
        normalizacao = (n - 1) * (n - 2) / 2
        return intermediacao / normalizacao
    

    # Exercício 6
    def centralidade_proximidade(self, vertice):
        if vertice not in self.grafo: return 0

        def bfs(vertice):
            visitados = {vertice: 0}
            fila = [vertice]
            while fila:
                atual = fila.pop(0)
                for vizinho, _ in self.grafo[atual]:
                    if vizinho not in visitados:
                        visitados[vizinho] = visitados[atual] + 1
                        fila.append(vizinho)

            del visitados[vertice]
            return visitados

        distancias = bfs(vertice)
        soma_distancias = sum(distancias.values())
        num_vertices_alcancaveis = len(distancias)
        centralidade_bruta = num_vertices_alcancaveis / soma_distancias

        return centralidade_bruta

def grafoNaoDirecionado():
    # Exercicio 1
    Grafo2 = GrafoNaoDirecionado()
    Grafo2.inserir_dados()
    # Grafo2.imprime_lista_adjacencias()

    # Exercício 2
    componentes = Grafo2.componentes_conexos()
    print(f"Número de componentes conexos: {componentes}")

    # Exercicio 3
    arestas = Grafo2.arvore_geradora_minima("JOÃO MIGUEL")
    print("Arestas da árvore geradora mínima:")
    for origem, destino, peso in arestas:
        print(f"{origem} - {destino} (Peso: {peso})")

    # Exercicio 4
    centralidade = Grafo2.centralidade("NORMAN REEDUS")
    print(f"Centralidade do vértice: {centralidade}")
    Grafo2.maior_centralidade()

    # Exercicio 5
    # intermediacao = Grafo2.centralidade_intermediacao_brandes("NORMAN REEDUS")
    # print(f"Centralidade de intermediação do vértice: {intermediacao:.2f}")

    # Exercicio 6
    proximidade = Grafo2.centralidade_proximidade("NORMAN REEDUS")
    print(f"Centralidade de proximidade do vértice: {proximidade:.2f}")

# --X-- Main --X--
# grafoDirecionado*()
grafoNaoDirecionado()