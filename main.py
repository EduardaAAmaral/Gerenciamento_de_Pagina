import sys
import time

# Função para simular a leitura de acessos de páginas (I para instruções e D para dados)
def ler_acessos(arquivo):
    with open(arquivo, 'r') as f:
        acessos = [linha.strip() for linha in f]
    return acessos

# Algoritmo Ótimo
def faltas_pagina_otimo(acessos, num_frames):
    memoria = []
    faltas = 0
    carregamentos = 0

    for i, pagina in enumerate(acessos):
        if pagina not in memoria:
            faltas += 1
            carregamentos += 1
            if len(memoria) < num_frames:
                memoria.append(pagina)
            else:
                # Encontrar a página que será usada mais tarde ou nunca mais
                futuros_usos = []
                for pag in memoria:
                    if pag in acessos[i+1:]:
                        futuros_usos.append(acessos[i+1:].index(pag))
                    else:
                        futuros_usos.append(float('inf')) # Nunca mais será usada
                pagina_a_remover = memoria[futuros_usos.index(max(futuros_usos))]
                memoria.remove(pagina_a_remover)
                memoria.append(pagina)
    return faltas, carregamentos

# Algoritmo LRU (Least Recently Used)
def faltas_pagina_lru(acessos, num_frames):
    memoria = []
    faltas = 0
    carregamentos = 0
    uso_recente = {}

    for i, pagina in enumerate(acessos):
        if pagina not in memoria:
            faltas += 1
            carregamentos += 1
            if len(memoria) < num_frames:
                memoria.append(pagina)
            else:
                # Remover a página menos recentemente usada
                lru_pagina = min(memoria, key=lambda x: uso_recente.get(x, -1))
                memoria.remove(lru_pagina)
                memoria.append(pagina)
        uso_recente[pagina] = i
    return faltas, carregamentos

# Função principal
def main():
    if len(sys.argv) != 3:
        print("Uso: python Gerenciador_de_memoria.py <arquivo_de_acessos> <num_frames>")
        return

    arquivo_acessos = sys.argv[1]
    num_frames = int(sys.argv[2])

    print(f"Lendo acessos do arquivo: {arquivo_acessos}")
    acessos = ler_acessos(arquivo_acessos)
    print(f"Acessos lidos: ... (total {len(acessos)})")

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
    eficiencia = faltas_otimo / faltas_lru

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
