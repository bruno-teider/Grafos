# Grupo: Bruno Teider, Bernardo Czizyk, Luiz Mathias, Rafaela Vecchi
import os
import email
from collections import defaultdict

class Grafo:
    def __init__(self):
      self.grafo = defaultdict(list)
      self.ordem = 0 # Número de vértices no grafo
      self.tamanho = 0 # Número de arestas no grafo


    def get_adjacente(self, vertice):
        return self.grafo.get(vertice, [])

    def adiciona_vertice(self, u):
        if u not in self.grafo:  # Verifica se o vértice já existe
            self.grafo[u] = []  # Adiciona o vértice
            self.ordem += 1

    def adiciona_aresta(self, origem, destino, peso):
        if peso <= 0:
            return  
        
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
        self.grafo[origem].append((destino, peso))
        self.tamanho += 1   

    def tem_aresta(self, origem, destino):
        # Verifica se existe uma aresta entre dois vértices
        for v, _ in self.grafo.get(origem, []):
            if v == destino:
                return True
        return False
    
    # Exercício 2 a
    def imprime_ordem(self):
        print(f"Ordem do grafo: {self.ordem}")
        
    # Exercício 2 b
    def imprime_tamanho(self):
        print(f"Tamanho do grafo: {self.tamanho}")
    
    # Exercício 2 c
    def vertices_isolados(self):
        vertices_isolados = set(self.grafo.keys())
        for adjacentes in self.grafo.values():
            for destino, _ in adjacentes:
                if destino in vertices_isolados:
                    vertices_isolados.remove(destino)
        print("Número de Vértices Isolados:", len(vertices_isolados))

    def grau_entrada(self, vertice):
        grau = 0
        for adjacentes in self.grafo.values():
            for destino, _ in adjacentes:
                if destino == vertice:
                    grau += 1
        return grau
    
    # Exercício 2 d
    def maiores_graus_saida(self):
        graus_saida = {}

        for email, adjacentes in self.grafo.items():
            graus_saida[email] = len(adjacentes)

        graus_saida_ordenados = sorted(graus_saida.items(), key=lambda item: item[1], reverse=True)

        print("Top 20 indivíduos com maior grau de saída:")
        for i in range(min(20, len(graus_saida_ordenados))):
            email, grau = graus_saida_ordenados[i]
            print(f"{email}: {grau}")

    # Exercício 2 e
    def maiores_graus_entrada(self):
        graus_entrada = {}
        
        for email, adjacentes in self.grafo.items():
            graus_entrada[email] = self.grau_entrada(email)
        
        graus_entrada = sorted(graus_entrada.items(), key=lambda item: item[1], reverse=True)[:20]
        
        print("Top 20 indivíduos com maior grau de entrada:")
        for email, grau in graus_entrada:
            print(f"{email}: {grau}")

    def dfs(self, origem, destino):
        visitado = []
        pilha = []
        caminho = [[origem]]
        pilha.append(origem)

        while pilha:
            elemento = pilha.pop()
            caminho_atual = caminho.pop()
            
            if elemento not in visitado:
                visitado.append(elemento)
                
                if elemento == destino:
                    return caminho_atual
                
                adjacentes = [adj[0] for adj in self.grafo[elemento]]
                for adj in sorted(adjacentes, reverse=True):
                    if adj not in visitado:
                        pilha.append(adj)
                        caminho.append(caminho_atual + [adj])
        return None 

    # Exercício 3
    def euleriano(self):
        # verifica se o grau de saida == ao grau de entrada
        for vertice in self.grafo:
            grau_saida = len(self.grafo[vertice])
            grau_entrada = self.grau_entrada(vertice)
            if grau_saida != grau_entrada:
                print("O grafo não é euleriano pois as condições não foram aceitas.")
                return False
        
            for vertice in self.grafo:
                if len(self.dfs(vertice, vertice)) == 0:
                    print("O grafo não é euleriano pois não é conexo.")
                    return False
            
        print("O grafo é euleriano.")
        return True

    # Exercício 4
    def menor_caminho(self, origem, limite_distancia):     
        distancias = {vertice: float('infinity') for vertice in self.grafo}
        distancias[origem] = 0
        visitados = set()
        
        while len(visitados) < self.ordem:
            # Encontra o vértice não visitado com a menor distância
            min_distancia = float('infinity')
            vertice_atual = None
            
            for vertice in self.grafo:
                if vertice not in visitados and distancias[vertice] < min_distancia:
                    min_distancia = distancias[vertice]
                    vertice_atual = vertice
            
            # Condição de parada
            if vertice_atual is None or min_distancia > limite_distancia:
                break
            
            visitados.add(vertice_atual)
            
            # Verifica vizinhos
            for vizinho, peso in self.grafo[vertice_atual]:
                if vizinho not in visitados:
                    distancia = distancias[vertice_atual] + peso
                    
                    # Se tiver caminho menor
                    if distancia < distancias[vizinho]:
                        distancias[vizinho] = distancia
        
        # Filtra os vértices que estão dentro do limite de distância
        vertices_alcancaveis = [vertice for vertice, distancia in distancias.items() if distancia <= limite_distancia and vertice != origem]
        print(f"Vértices alcançáveis de '{origem}' com distância <= {limite_distancia}: {len(vertices_alcancaveis)}")
        return vertices_alcancaveis

    # Exercício 5
    def dijkstra(self, origem):
        visitados = set()
        custo = {vertice: [float('inf'), None] for vertice in self.grafo}
        custo[origem][0] = 0
        
        while len(visitados) < len(self.grafo):
            min_vertice = None
            min_distancia = float('inf')
            
            for vertice in self.grafo:
                if vertice not in visitados and custo[vertice][0] < min_distancia:
                    min_vertice = vertice
                    min_distancia = custo[vertice][0]
            
            if min_vertice is None:
                break
                
            visitados.add(min_vertice)
            
            for vizinho, peso in self.grafo[min_vertice]:
                if vizinho not in visitados:
                    distancia = custo[min_vertice][0] + peso
                    if distancia < custo[vizinho][0]:
                        custo[vizinho][0] = distancia
                        custo[vizinho][1] = min_vertice
        return custo

    def reconstruir_caminho(self, custo, origem, destino):
        caminho = []
        
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            atual = custo[atual][1]
        return caminho

    def calcular_diametro(self):
        maior_caminho = 0
        caminho_diametro = None
        origem_final = None
        destino_final = None

        # Usar lista de vértices ao invés de range
        vertices = list(self.grafo.keys())
        
        count = 0
        for origem in vertices:
            custo = self.dijkstra(origem)
            print(f"Dikstra {count} de {len(vertices)} feito")
            count += 1
            for destino in vertices:
                if origem != destino:
                    distancia = custo[destino][0]
                    if distancia != float('inf') and distancia > maior_caminho:
                        maior_caminho = distancia
                        origem_final = origem
                        destino_final = destino

        if origem_final and destino_final:
            caminho_diametro = self.reconstruir_caminho(
                self.dijkstra(origem_final), 
                origem_final, 
                destino_final
            )
            
            print(f"Diâmetro do Grafo: {maior_caminho}")
            print(f"Caminho do diâmetro: {' -> '.join(map(str, caminho_diametro))}")
            return maior_caminho, caminho_diametro
        
        print("Não foi possível encontrar o diâmetro do grafo")
        return None, None

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
        with open("grafo.txt", "w") as f:
            f.write(final_text)

# -- Main --

def ler_arquivos(dataPath, G):
    for item in os.listdir(dataPath):
        # Faz a criação do caminho do arquivo ex Amostra Enron - 2016/{item}/_sent_mail
        item_path = os.path.join(dataPath, item)

        # Chama a função recursivamente se o item for uma pasta
        if os.path.isdir(item_path):
            ler_arquivos(item_path, G)
        else:
            inserir_dados(item_path, G)
        
def inserir_dados(item_path, G):
    with open(item_path, "r") as file:
        msg = email.message_from_file(file)
        sender = msg["From"]
        receivers = msg["To"]

        if not sender or not receivers:
            return
        
        # Mantém apenas o que está dentro de < > e remove o ponto inicial, se existir
        sender = sender.split("<")[-1].split(">")[0].lstrip(".").strip()
        G.adiciona_vertice(sender)

        receivers = [r.split("<")[-1].split(">")[0].lstrip(".").strip() for r in receivers.split(",")]
        
        for receiver in receivers:
            if receiver:
                G.adiciona_vertice(receiver)
                peso = 1
            if G.tem_aresta(sender, receiver):
                peso += 1  # Incrementa o peso se a aresta já existir
            G.adiciona_aresta(sender, receiver, peso)   

# Main

import time

start = time.time()

G = Grafo()
dataPath = './Amostra Enron - 2016/'
ler_arquivos(dataPath, G)
# G.imprime_lista_adjacencias()
# print('\n')
# G.imprime_ordem()
# G.imprime_tamanho()
# G.vertices_isolados()
# print('\n')
# G.maiores_graus_saida()
# print('\n')
# G.maiores_graus_entrada()
# print(G.dfs('seareel@neosoft.com', 'kimberly.watson@enron.com'))
# print(G.euleriano())
# G.menor_caminho('seareel@neosoft.com', 20)
# G.calcular_diametro()

end = time.time()

print(f"Tempo de execução: {end - start:.2f} segundos")