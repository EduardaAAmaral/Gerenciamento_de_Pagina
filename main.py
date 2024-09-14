from collections import OrderedDict, deque
import re
import sys
import timeit

# Função para simular a leitura de acessos de páginas (I para instruções e D para dados)
def ler_acessos(arquivo):
    acessos = []
    with open(arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            match = re.match(r'^[ID](\d+)', linha)
            if match:
                acessos.append(linha)
            else:
                print(f"Formato de linha inválido: {linha}")
    return acessos

# Converte a quantidade de memória para frames com base no tamanho da página
def calcular_frames(memoria_fisica_kb, tamanho_pagina_kb=4):
    return memoria_fisica_kb // tamanho_pagina_kb

# Algoritmo Ótimo
def faltas_pagina_otimo(acessos, num_frames):
    memoria = []
    faltas = 0
    carregamentos = 0
    carregamentos_por_pagina = {}  # Dicionário para rastrear carregamentos por página
    posicoes_futuras = {pagina: deque() for pagina in acessos}

    # Preenche as posições futuras para cada página
    for i, pagina in enumerate(acessos):
        posicoes_futuras[pagina].append(i)

    for i, pagina in enumerate(acessos):
        posicoes_futuras[pagina].popleft()  # Substitui pop(0) por popleft para maior eficiência

        if pagina not in memoria:
            faltas += 1
            carregamentos += 1
            carregamentos_por_pagina[pagina] = carregamentos_por_pagina.get(pagina, 0) + 1  # Conta o carregamento
            if len(memoria) < num_frames:
                memoria.append(pagina)
            else:
                futuros_usos = []
                for pag in memoria:
                    if posicoes_futuras[pag]:
                        futuros_usos.append(posicoes_futuras[pag][0])
                    else:
                        futuros_usos.append(float('inf'))
                pagina_a_remover = memoria[futuros_usos.index(max(futuros_usos))]
                memoria.remove(pagina_a_remover)
                memoria.append(pagina)

    return faltas, carregamentos, carregamentos_por_pagina

# Algoritmo LRU (Least Recently Used)
def faltas_pagina_lru(acessos, num_frames):
    memoria = OrderedDict()
    faltas = 0
    carregamentos = 0
    carregamentos_por_pagina = {}  # Dicionário para rastrear carregamentos por página

    for pagina in acessos:
        if pagina not in memoria:
            faltas += 1
            carregamentos += 1
            carregamentos_por_pagina[pagina] = carregamentos_por_pagina.get(pagina, 0) + 1  # Conta o carregamento
            if len(memoria) >= num_frames:
                memoria.popitem(last=False)
            memoria[pagina] = None
        else:
            memoria.move_to_end(pagina)

    return faltas, carregamentos, carregamentos_por_pagina

# Função para exibir acessos
def exibir_acessos(acessos):
    n = len(acessos)
    if n > 5:
        print(f"Acessos lidos: {acessos[:5]} ... {acessos[-5:]} (total {len(acessos)})")
    else:
        print(f"Acessos lidos: {acessos} (total {len(acessos)})")

# Função principal
def main():
    if len(sys.argv) != 3:
        print("Uso: python Gerenciador_de_memoria.py <arquivo_de_acessos> <memoria_fisica_kb>")
        return

    arquivo_acessos = sys.argv[1]
    memoria_fisica_kb = int(sys.argv[2])

    print(f"Lendo acessos do arquivo: {arquivo_acessos}")
    acessos = ler_acessos(arquivo_acessos)
    exibir_acessos(acessos)

    # Converter memória física para número de frames
    num_frames = calcular_frames(memoria_fisica_kb)
    print(f"Calculando faltas de página com {num_frames} frames (para {memoria_fisica_kb} KB de memória física)...")

    # Para maior precisão de tempo, repete a execução várias vezes
    num_execucoes = 100  # Ajuste conforme necessário
    total_time_otimo = 0
    total_time_lru = 0

    for _ in range(num_execucoes):
        # Algoritmo Ótimo
        inicio_otimo = timeit.default_timer()
        faltas_otimo, carregamentos_otimo, carregamentos_por_pagina_otimo = faltas_pagina_otimo(acessos, num_frames)
        fim_otimo = timeit.default_timer()
        total_time_otimo += fim_otimo - inicio_otimo

        # Algoritmo LRU
        inicio_lru = timeit.default_timer()
        faltas_lru, carregamentos_lru, carregamentos_por_pagina_lru = faltas_pagina_lru(acessos, num_frames)
        fim_lru = timeit.default_timer()
        total_time_lru += fim_lru - inicio_lru

    # Calcular a média dos tempos
    tempo_medio_otimo = total_time_otimo / num_execucoes
    tempo_medio_lru = total_time_lru / num_execucoes

    # Calcular eficiência
    eficiencia = faltas_otimo / faltas_lru if faltas_lru > 0 else float('inf')

    print(f"Faltas de página (Ótimo): {faltas_otimo}")
    print(f"Faltas de página (LRU): {faltas_lru}")
    print(f"Eficiência do LRU em relação ao Ótimo: {eficiencia:.2f}")
    print(f"Tempo médio de execução (Ótimo): {tempo_medio_otimo:.6f} segundos")
    print(f"Tempo médio de execução (LRU): {tempo_medio_lru:.6f} segundos")

    # Perguntar se deseja listar o número de carregamentos
    listar = input("Deseja listar o número de carregamentos por página (s/n)? ").lower()
    if listar == 's':
        print(f"Carregamentos por página (Ótimo): {carregamentos_por_pagina_otimo}")
        print(f"Carregamentos por página (LRU): {carregamentos_por_pagina_lru}")

if __name__ == "__main__":
    main()
