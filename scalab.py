import multiprocessing as mp
from bitarray import bitarray
import sys

# --- Configurações ---
N_NUMEROS = 25
TAMANHO_S14 = 14
TAMANHO_S15 = 15
SOMA_MIN = 221
SOMA_MAX = 233

# --- Função para checar sequência >=7 ---
def tem_sequencia_maior_ou_igual_que_7(numeros):
    numeros_ordenados = sorted(numeros)
    atual = 1
    for i in range(1, len(numeros_ordenados)):
        if numeros_ordenados[i] == numeros_ordenados[i - 1] + 1:
            atual += 1
            if atual >= 5:
                return True
        else:
            atual = 1
    return False

# --- Gera combinações via backtracking, filtrando ---
def gera_combinacoes(tamanho, filtra_soma=False):
    resultados = []
    combinacao = []

    def backtrack(inicio):
        if len(combinacao) == tamanho:
            if tem_sequencia_maior_ou_igual_que_7(combinacao):
                return
            if filtra_soma:
                s = sum(combinacao)
                if s < SOMA_MIN or s > SOMA_MAX:
                    return
            resultados.append(combinacao[:])
            return
        for i in range(inicio, N_NUMEROS + 1):
            combinacao.append(i)
            backtrack(i + 1)
            combinacao.pop()

    backtrack(1)
    return resultados

# --- Converte listas de números para bitarrays ---
def converte_para_bitarray(arrays, tamanho=N_NUMEROS):
    bitarrays = []
    for arr in arrays:
        ba = bitarray(tamanho)
        ba.setall(0)
        for num in arr:
            ba[num - 1] = 1  # índice zero-based
        bitarrays.append(ba)
    return bitarrays

# --- Constroi índice invertido: número -> set índices de s15 que contém o número ---
def cria_indice_invertido(bitarrays_s15):
    indice = [set() for _ in range(N_NUMEROS)]
    for idx, ba in enumerate(bitarrays_s15):
        for num in range(N_NUMEROS):
            if ba[num]:
                indice[num].add(idx)
    return indice

# --- Função para processar um chunk de s14 (índices e bitarrays) ---
def processa_chunk(args):
    chunk_s14, bitarrays_s15, indice_invertido = args
    from collections import defaultdict
    contagem = defaultdict(int)  # s15_idx -> count de s14 que ele contém

    for ba_s14 in chunk_s14:
        bits_s14 = [i for i, bit in enumerate(ba_s14) if bit]  # mais rápido que search()
        if not bits_s14:
            continue

        sets = [indice_invertido[b] for b in bits_s14]
        sets.sort(key=len)

        candidatos = sets[0].copy()
        for s in sets[1:]:
            candidatos &= s
            if not candidatos:
                break

        for c in candidatos:
            contagem[c] += 1

    return contagem

# --- Função para juntar dicionários de contagem ---
def junta_contagens(dicts):
    from collections import defaultdict
    contagem_total = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            contagem_total[k] += v
    return contagem_total

# --- Função principal ---
def main():
    print("Gerando combinações s14 (14 números, filtro seq≥7 e soma)...")
    s14_list = gera_combinacoes(TAMANHO_S14, filtra_soma=True)  # ← ATIVADO filtro soma
    print(f"Total s14: {len(s14_list)}")

    print("Gerando combinações s15 (15 números, filtro seq≥7 e soma)...")
    s15_list = gera_combinacoes(TAMANHO_S15, filtra_soma=True)
    print(f"Total s15: {len(s15_list)}")

    print("Convertendo combinações para bitarrays...")
    bit_s14 = converte_para_bitarray(s14_list)
    bit_s15 = converte_para_bitarray(s15_list)

    print("Criando índice invertido para s15...")
    indice_inv = cria_indice_invertido(bit_s15)

    print("Dividindo s14 em chunks para paralelização...")
    n_processos = mp.cpu_count()
    chunk_size = len(bit_s14) // n_processos + 1
    chunks = [bit_s14[i * chunk_size:(i + 1) * chunk_size] for i in range(n_processos)]

    print(f"Executando paralelização com {n_processos} processos...")
    with mp.Pool(n_processos) as pool:
        resultados = pool.map(processa_chunk, [(chunk, bit_s15, indice_inv) for chunk in chunks])

    print("Agregando resultados...")
    contagem_total = junta_contagens(resultados)

    print("Selecionando melhores combinações s15...")
    melhores = sorted(contagem_total.items(), key=lambda x: x[1], reverse=True)

    print(f"Top 10 melhores combinações s15 e quantos s14 cobrem:")
    for idx, cont in melhores[:10]:
        print(f"s15 idx {idx}, cobre {cont} s14 combinações, conjunto: {s15_list[idx]}")

if __name__ == "__main__":
    main()
