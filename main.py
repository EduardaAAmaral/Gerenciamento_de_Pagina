from collections import OrderedDict, deque
import re
import sys
import time

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

# Algoritmo Ótimo
def faltas_pagina_otimo(acessos, num_frames):
    memoria = []
    faltas = 0
    carregamentos = 0
    posicoes_futuras = {pagina: deque() for pagina in acessos}

    # Preenche as posições futuras para cada página
    for i, pagina in enumerate(acessos):
        posicoes_futuras[pagina].append(i)

    for i, pagina in enumerate(acessos):
        posicoes_futuras[pagina].popleft()  # Substitui pop(0) por popleft para maior eficiência

        if pagina not in memoria:
            faltas += 1
            carregamentos += 1
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

    return faltas, carregamentos

# Algoritmo LRU (Least Recently Used)
def faltas_pagina_lru(acessos, num_frames):
    memoria = OrderedDict()
    faltas = 0
    carregamentos = 0

    for pagina in acessos:
        if pagina not in memoria:
            faltas += 1
            carregamentos += 1
            if len(memoria) >= num_frames:
                memoria.popitem(last=False)
            memoria[pagina] = None
        else:
            memoria.move_to_end(pagina)

    return faltas, carregamentos

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
        print("Uso: python Gerenciador_de_memoria.py <arquivo_de_acessos> <num_frames>")
        return

    arquivo_acessos = sys.argv[1]
    num_frames = int(sys.argv[2])

    print(f"Lendo acessos do arquivo: {arquivo_acessos}")
    acessos = ler_acessos(arquivo_acessos)
    exibir_acessos(acessos)

    print(f"Calculando faltas de página com {num_frames} frames...")

    # Algoritmo Ótimo
    inicio_otimo = time.time()
    faltas_otimo, carregamentos_otimo = faltas_pagina_otimo(acessos, num_frames)
    fim_otimo = time.time()
    tempo_otimo = fim_otimo - inicio_otimo

    # Algoritmo LRU
    inicio_lru = time.time()
    faltas_lru, carregamentos_lru = faltas_pagina_lru(acessos, num_frames)
    fim_lru = time.time()
    tempo_lru = fim_lru - inicio_lru

    # Calcular eficiência
    eficiencia = faltas_otimo / faltas_lru if faltas_lru > 0 else float('inf')

    print(f"Faltas de página (Ótimo): {faltas_otimo}")
    print(f"Faltas de página (LRU): {faltas_lru}")
    print(f"Eficiência do LRU em relação ao Ótimo: {eficiencia:.2f}")
    print(f"Tempo de execução (Ótimo): {tempo_otimo:.2f} segundos")
    print(f"Tempo de execução (LRU): {tempo_lru:.2f} segundos")

    # Perguntar se deseja listar o número de carregamentos
    listar = input("Deseja listar o número de carregamentos (s/n)? ").lower()
    if listar == 's':
        print(f"Carregamentos (Ótimo): {carregamentos_otimo}")
        print(f"Carregamentos (LRU): {carregamentos_lru}")

if __name__ == "__main__":
    main()
