import cvrplib_reader, cvrp_nearest_neighbor
import time
import os

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
    print("-" * 50)

    for ficheiro in ficheiros:
        caminho_ficheiro = os.path.join(pasta, ficheiro)
        matriz_distancias, num_cidades, demandas, capacidade = cvrplib_reader.ler_instancias(caminho_ficheiro)

        inicio = time.time()
        custo_fo = cvrp_nearest_neighbor.nearest_neighbor(matriz_distancias, num_cidades, demandas, capacidade)
        fim = time.time()
        tempo_execucao = fim - inicio

        print(f"Instancia: {ficheiro} | Cidades: {num_cidades} | Capacidade veiculo: {capacidade}")
        print(f"Solução do algoritmo (fo): {custo_fo}")
        print(f"Tempo de Execução: {tempo_execucao:.6f} seg")
        print("-" * 50)

if __name__ == "__main__":
    main()