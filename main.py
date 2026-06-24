import cvrplib_reader, cvrp_nearest_neighbor, cvrp_vnd, cvrp_ils
import time
import os
import re


def ler_otimo(caminho_ficheiro):
    with open(caminho_ficheiro, 'r') as arquivo:
        for linha in arquivo:
            achou = re.search(r'Optimal value:\s*(\d+)', linha)
            if achou:
                return int(achou.group(1))
    return None


def gap_str(custo, otimo):
    if otimo is None:
        return "  -  "
    return f"{100 * (custo - otimo) / otimo:.2f}%"


def main():
    pasta = "instancias"

    if not os.path.exists(pasta):
        print(f"A pasta '{pasta}' não existe.")
        return

    ficheiros = [f for f in os.listdir(pasta) if f.endswith('.vrp')]

    if not ficheiros:
        print(f"Nenhum ficheiro '.vrp' encontrado em '{pasta}'.")
        return

    print(f"Encontradas {len(ficheiros)} instâncias CVRP para processar.\n")
    print("=" * 64)

    soma_gap_vnd = 0.0
    soma_gap_ils = 0.0
    qtd_gap = 0

    for ficheiro in sorted(ficheiros):
        caminho_ficheiro = os.path.join(pasta, ficheiro)
        matriz_distancias, num_clientes, demandas, capacidade = cvrplib_reader.ler_instancias(caminho_ficheiro)
        otimo = ler_otimo(caminho_ficheiro)

        # NN
        inicio = time.time()
        rota_inicial, custo_nn = cvrp_nearest_neighbor.nearest_neighbor(matriz_distancias, num_clientes, demandas, capacidade)
        tempo_nn = time.time() - inicio

        # VND
        inicio = time.time()
        rota_vnd, custo_vnd = cvrp_vnd.vnd(rota_inicial, matriz_distancias, demandas, capacidade)
        tempo_vnd = time.time() - inicio

        # ILS
        inicio = time.time()
        rota_ils, custo_ils = cvrp_ils.ils(rota_inicial, matriz_distancias, demandas, capacidade, max_iter=300, k=4, seed=42)
        tempo_ils = time.time() - inicio

        rotas_nn  = rota_inicial.count(0) - 1
        rotas_vnd = rota_vnd.count(0) - 1
        rotas_ils = rota_ils.count(0) - 1

        if otimo is not None:
            soma_gap_vnd += 100 * (custo_vnd - otimo) / otimo
            soma_gap_ils += 100 * (custo_ils - otimo) / otimo
            qtd_gap += 1

        print(f"Instancia: {ficheiro} | Clientes: {num_clientes} | "
              f"Capacidade: {capacidade} | Otimo: {otimo}")
        print(f"  {'Metodo':<22}{'Custo':>8}{'Gap':>9}{'Rotas':>7}{'Tempo(s)':>12}")

        print(f"  {'NN (construcao)':<22}{custo_nn:>8.0f}{gap_str(custo_nn, otimo):>9}"
              f"{rotas_nn:>7}{tempo_nn:>12.6f}")
        
        print(f"  {'VND (busca local)':<22}{custo_vnd:>8.0f}{gap_str(custo_vnd, otimo):>9}"
              f"{rotas_vnd:>7}{tempo_vnd:>12.6f}")
        
        print(f"  {'ILS':<22}{custo_ils:>8.0f}{gap_str(custo_ils, otimo):>9}"
              f"{rotas_ils:>7}{tempo_ils:>12.6f}")
        print("=" * 64)

    if qtd_gap > 0:
        print("\nResumo (gap medio para o otimo):")
        print(f"  VND : {soma_gap_vnd / qtd_gap:.2f}%")
        print(f"  ILS : {soma_gap_ils / qtd_gap:.2f}%")


if __name__ == "__main__":
    main()