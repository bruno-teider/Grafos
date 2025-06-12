from collections import defaultdict, deque, Counter
from tqdm import tqdm
import pandas as pd
import heapq
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import gc
import numpy as np

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

        # Contagem de vértices em cada componente
        tamanhos_componentes = []

        for componente in componentes:
            tamanhos_componentes.append(len(componente))

        contagem = Counter(tamanhos_componentes)

        plt.bar(contagem.keys(), contagem.values(), color='mediumseagreen')
        plt.title('Distribuição de Tamanhos dos Componentes Fortemente Conexos')
        plt.xlabel('Tamanho do Componente')
        plt.ylabel('Número de Componentes')
        
        # Force integer ticks on both axes
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.tight_layout()
        plt.show()

        return componentes
    
    #Exercício 4
    def centralidade(self, vertice_alvo): 
        if vertice_alvo not in self.grafo: 
            return 0

        grau_saida = len(self.grafo[vertice_alvo])
        grau_entrada = 0

        for v in self.grafo:  
            for adjacente, _ in self.grafo[v]:
                if adjacente == vertice_alvo:
                    grau_entrada += 1

        grau_total = grau_saida + grau_entrada
        grau_maximo = 2 * (self.ordem - 1)

        return grau_total / grau_maximo if grau_maximo > 0 else 0

    def maiores_centralidades(self):
        centralidades = {}
        # Pegamos apenas os graus de saída zero, ou seja, os diretores
        vertices_grau_saida_zero = [v for v in self.grafo if len(self.grafo[v]) == 0]
        
        for vertice in tqdm(vertices_grau_saida_zero):
            centralidade = self.centralidade(vertice)
            centralidades[vertice] = centralidade

        centralidades_ordenadas = sorted(centralidades.items(), key=lambda x: x[1], reverse=True)

        print(f"Maiores Centralidades Diretores (vértices com grau de saída = 0")
        for vertice, centralidade in centralidades_ordenadas[:10]:
            print(f"{vertice}: {centralidade:.4f}")

    #Exercício 5
    def bfs_caminhos_mais_curtos_contagem(self, origem):
        distancia = {}
        sigma = defaultdict(int)  # número de caminhos mais curtos
        predecessores = defaultdict(list)
        
        for v in self.grafo:
            distancia[v] = float('inf')
        
        distancia[origem] = 0
        sigma[origem] = 1
        fila = deque([origem])
        
        while fila:
            v = fila.popleft()
            for vizinho, _ in self.grafo[v]:
                if distancia[vizinho] == float('inf'):
                    distancia[vizinho] = distancia[v] + 1
                    fila.append(vizinho)
                if distancia[vizinho] == distancia[v] + 1:
                    sigma[vizinho] += sigma[v]
                    predecessores[vizinho].append(v)
        
        return distancia, sigma, predecessores
  
    def intermediacao(self, vertice_alvo):
        if vertice_alvo not in self.grafo:
            return 0.0
        
        intermedia = 0.0
        vertices = list(self.grafo.keys())

        for s in vertices:
            if s == vertice_alvo:
                continue

            dist, sigma, pred = self.bfs_caminhos_mais_curtos_contagem(s)
            delta = defaultdict(float)
            stack = [v for v in sorted(dist.keys(), key=lambda x: -dist[x]) if dist[v] < float('inf')]

            for w in stack:
                for v in pred[w]:
                    c = (sigma[v] / sigma[w]) * (1 + delta[w])
                    delta[v] += c
                if w != s and w == vertice_alvo:
                    intermedia += delta[w]

        n = len(vertices)
        if n <= 2:
            return 0.0
        else:
            return intermedia / ((n - 1) * (n - 2))
    
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
    
    def distribuicao_grau(self):
        grau_saida = defaultdict(int)
        grau_entrada = defaultdict(int)

        for vertice in self.grafo:
            grau_saida[vertice] = len(self.grafo[vertice])
            for adjacente, _ in self.grafo[vertice]:
                grau_entrada[adjacente] += 1

        # Após calcular grau_saida e grau_entrada
        contagem_saida = Counter(grau_saida.values())
        contagem_entrada = Counter(grau_entrada.values())

        # Plotando os gráficos
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        axs[0].bar(contagem_saida.keys(), contagem_saida.values(), color='skyblue')
        axs[0].set_title('Distribuição de Grau de Saída')
        axs[0].set_xlabel('Grau de saída')
        axs[0].set_ylabel('Número de vértices')
        axs[1].bar(contagem_entrada.keys(), contagem_entrada.values(), color='salmon')
        axs[1].set_title('Distribuição de Grau de Entrada')
        axs[1].set_xlabel('Grau de entrada')
        axs[1].set_ylabel('Número de vértices')
        plt.tight_layout()
        plt.show()

        return grau_saida, grau_entrada
    
def grafoDirecionado():
    # Exercicio 1
    Grafo1 = GrafoDirecionado()
    GrafoDirecionado.inserir_dados(Grafo1)
    # Grafo1.imprime_lista_adjacencias()
    
    # Exercicio 2
    # componentes = Grafo1.componentes_fortemente_conexos()
    # print(f"Número componentes fortemente conexos: {len(componentes)}")
    
    # # Exercício 4
    # centralidade = Grafo1.centralidade("ROBERT DOWNEY JR.")
    # print(f"Centralidade do vértice: {centralidade:.2f}")
    # maiores = Grafo1.maiores_centralidades()
    
    # # Exercício 5
    # intermediacao = Grafo1.intermediacao("ROBERT DOWNEY JR.")
    # print(f"Centralidade de intermediação do vértice: {intermediacao:.2f}")
    
    # # Exercício 6
    # proximidade = Grafo1.centralidade_proximidade("YURI LOWENTHAL")
    # print(f"Centralidade de proximidade do vértice: {proximidade:.2f}")

    # distribuicao_grau = Grafo1.distribuicao_grau()

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
                self.grafo[origem][i] = (destino, peso)
                aresta_existe = True
                break
            
        # Atualiza o peso na lista de adjacência de destino
        if aresta_existe:
            for i in range(len(self.grafo[destino])):
                vertice, peso = self.grafo[destino][i]
                if vertice == origem:
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
        componentes = []
        contador = 0

        for vertice in self.grafo:
            if vertice not in visitado:
                contador += 1
                componente_atual = []
                pilha = [vertice]

                while pilha:
                    v = pilha.pop()
                    if v not in visitado:
                        visitado.add(v)
                        componente_atual.append(v)
                        for vizinho, _ in self.grafo[v]:
                            if vizinho not in visitado:
                                pilha.append(vizinho)
                
                componentes.append(componente_atual)
        
        # Contagem de vértices em cada componente
        tamanhos_componentes = []

        for componente in componentes:
            tamanhos_componentes.append(len(componente))
            # print(f'Componente {contador}: {componente}')

        contagem = Counter(tamanhos_componentes)

        contagem_sem_gigante = {k: v for k, v in contagem.items() if k < 1000}

        plt.bar(contagem_sem_gigante.keys(), contagem_sem_gigante.values(), color='mediumseagreen')
        plt.title('Distribuição dos Componentes Conexos (sem o maior)')
        plt.xlabel('Tamanho do Componente')
        plt.ylabel('Número de Componentes')
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.tight_layout()
        plt.show()
        
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
    def centralidade_intermediacao(self, vertice_alvo): 
        if vertice_alvo not in self.grafo: 
            return 0

        grau = len(self.grafo[vertice_alvo])
        grau_maximo = self.ordem - 1

        return grau / grau_maximo if grau_maximo > 0 else 0
    
    def maior_centralidade(self):
        maior = 0
        nome = ''
        for vertice in self.grafo:
            centralidade = self.centralidade_intermediacao(vertice)
            if centralidade > maior:
                maior = centralidade
                nome = vertice
            
        print(f'Maior Centralidade: {nome} -> {maior}')
    
    def maiores_centralidades(self):
        centralidades = {}
        
        for vertice in tqdm(self.grafo):
            centralidade = self.centralidade_intermediacao(vertice)
            centralidades[vertice] = centralidade

        centralidades_ordenadas = sorted(centralidades.items(), key=lambda x: x[1], reverse=True)

        print(f"Maiores Centralidades Atores")
        for vertice, centralidade in centralidades_ordenadas[:10]:
            print(f"{vertice}: {centralidade:.4f}")

    # Exercício 5 / 7
    def intermediacoes_brandes(self):
        # Converte vértices para lista para processamento eficiente
        lista_vertices = list(self.grafo.keys())
        total_vertices = len(lista_vertices)
        tamanho_chunk = 1000
        
        # Inicializa usando numpy para ser rodável
        centralidade_intermediacao = np.zeros(total_vertices, dtype=np.float64)
        mapeamento_vertice_para_indice = {vertice: indice for indice, vertice in enumerate(lista_vertices)}
        
        # Processa em chunks para conseguir rodar
        total_chunks = (total_vertices + tamanho_chunk - 1) // tamanho_chunk
        barra_progresso = tqdm(total=total_vertices, desc="Calculando intermediacao")
        
        for numero_chunk in range(total_chunks):
            indice_inicial_chunk = numero_chunk * tamanho_chunk
            indice_final_chunk = min((numero_chunk + 1) * tamanho_chunk, total_vertices)
            vertices_do_chunk = lista_vertices[indice_inicial_chunk:indice_final_chunk]
            
            # Processa cada vértice no chunk
            for vertice_origem in vertices_do_chunk:
                indice_vertice_origem = mapeamento_vertice_para_indice[vertice_origem]
                
                # Estruturas de dados para Brandes
                pilha_ordem_visitacao = []
                lista_predecessores = [[] for _ in range(total_vertices)]
                contador_caminhos_curtos = np.zeros(total_vertices, dtype=np.float64)
                contador_caminhos_curtos[indice_vertice_origem] = 1.0
                distancias_minimas = np.full(total_vertices, -1, dtype=np.int32)
                distancias_minimas[indice_vertice_origem] = 0
                dependencia_parcial = np.zeros(total_vertices, dtype=np.float64)
                
                # BFS
                fila_bfs = deque([indice_vertice_origem])
                
                while fila_bfs:
                    indice_vertice_atual = fila_bfs.popleft()
                    pilha_ordem_visitacao.append(indice_vertice_atual)
                    vertice_atual = lista_vertices[indice_vertice_atual]
                    
                    # Itera sobre vizinhos do vértice atual
                    for vertice_vizinho, _ in self.grafo[vertice_atual]:
                        indice_vertice_vizinho = mapeamento_vertice_para_indice[vertice_vizinho]
                        
                        # Se for primeira vez visitando o vizinho
                        if distancias_minimas[indice_vertice_vizinho] < 0:
                            fila_bfs.append(indice_vertice_vizinho)
                            distancias_minimas[indice_vertice_vizinho] = distancias_minimas[indice_vertice_atual] + 1
                        
                        # Se encontrou caminho mais curto para vizinho passando pelo vértice atual
                        if distancias_minimas[indice_vertice_vizinho] == distancias_minimas[indice_vertice_atual] + 1:
                            contador_caminhos_curtos[indice_vertice_vizinho] += contador_caminhos_curtos[indice_vertice_atual]
                            lista_predecessores[indice_vertice_vizinho].append(indice_vertice_atual)
                
                # Acumulação: processa vértices em ordem reversa
                while pilha_ordem_visitacao:
                    indice_vertice_processado = pilha_ordem_visitacao.pop()
                    
                    for indice_predecessor in lista_predecessores[indice_vertice_processado]:
                        if contador_caminhos_curtos[indice_vertice_processado] > 0:
                            proporcao_caminhos = contador_caminhos_curtos[indice_predecessor] / contador_caminhos_curtos[indice_vertice_processado]
                            dependencia_parcial[indice_predecessor] += proporcao_caminhos * (1.0 + dependencia_parcial[indice_vertice_processado])
                    
                    # Acumula centralidade (exceto para o vértice origem)
                    if indice_vertice_processado != indice_vertice_origem:
                        centralidade_intermediacao[indice_vertice_processado] += dependencia_parcial[indice_vertice_processado]
                
                barra_progresso.update(1)
            
            # Limpa memória após cada chunk
            gc.collect()
        
        barra_progresso.close()
        
        # Converte de volta para dicionário
        resultado_centralidades = {
            lista_vertices[indice]: centralidade_intermediacao[indice] 
            for indice in range(total_vertices)
        }
        
        for vertice in resultado_centralidades:
            resultado_centralidades[vertice] /= 2.0
        
        return resultado_centralidades

    def maiores_intermediacoes(self):
        intermediacoes = self.intermediacoes_brandes()
        intermediacoes_ordenadas = sorted(
            intermediacoes.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        print("Maiores Intermediações (Algoritmo de Brandes)")
        for vertice, intermediacao in intermediacoes_ordenadas[:10]:
            print(f"{vertice}: {intermediacao:.4f}")
        
        return intermediacoes_ordenadas

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
    
    def maiores_proximidades(self):
        proximidades = {}
        
        for vertice in tqdm(self.grafo):
            proximidade = self.centralidade_proximidade(vertice)
            proximidades[vertice] = proximidade

        proximidades_ordenadas = sorted(proximidades.items(), key=lambda x: x[1], reverse=True)

        print(f"Maiores Proximidades Atores")
        for vertice, proximidade in proximidades_ordenadas[:10]:
            print(f"{vertice}: {proximidade:.4f}")

    def distribuicao_grau_nao_direcionado(self):
        grau = defaultdict(int)

        for vertice in self.grafo:
            grau[vertice] = len(self.grafo[vertice])

        contagem = Counter(grau.values())

        plt.bar(contagem.keys(), contagem.values(), color='mediumseagreen')
        plt.title('Distribuição de Grau (Grafo Não Direcionado)')
        plt.xlabel('Grau')
        plt.ylabel('Número de vértices')
        plt.tight_layout()
        plt.show()

        return grau

def grafoNaoDirecionado():
    # Exercicio 1
    Grafo2 = GrafoNaoDirecionado()
    Grafo2.inserir_dados()
    # Grafo2.imprime_lista_adjacencias()

    # # Exercício 2
    # componentes = Grafo2.componentes_conexos()
    # print(f"Número de componentes conexos: {componentes}")

    # # Exercicio 3
    # arestas = Grafo2.arvore_geradora_minima("JOÃO MIGUEL")
    # print("Arestas da árvore geradora mínima:")
    # for origem, destino, peso in arestas:
    #     print(f"{origem} - {destino} (Peso: {peso})")

    # # Exercicio 4
    # centralidade = Grafo2.centralidade("NORMAN REEDUS")
    # print(f"Centralidade do vértice: {centralidade}")
    #Grafo2.maior_centralidade()

    # Exercicio 5
    # intermediacao = Grafo2.centralidade_intermediacao("ROBERT DOWNEY JR.")
    # print(f"Centralidade de intermediação do vértice: {intermediacao:.2f}")

    # Exercicio 6
    # proximidade = Grafo2.centralidade_proximidade("NORMAN REEDUS")
    # print(f"Centralidade de proximidade do vértice: {proximidade:.2f}")

    # distribuicao_grau = Grafo2.distribuicao_grau_nao_direcionado()
    #Ex6 = Grafo2.maiores_centralidades()
    Ex7 = Grafo2.maiores_intermediacoes()
    # Ex8 = Grafo2.maiores_proximidades()

# --X-- Main --X--
# grafoDirecionado()
grafoNaoDirecionado()