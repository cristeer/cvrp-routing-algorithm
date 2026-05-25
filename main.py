import cvrplib_reader, cvrp_nearest_neighbor, cvrp_busca_local
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
        matriz_distancias, num_clientes, demandas, capacidade = cvrplib_reader.ler_instancias(caminho_ficheiro)

        inicio = time.time()

        rota_inicial, custo_fo_inicial = cvrp_nearest_neighbor.nearest_neighbor(matriz_distancias, num_clientes, demandas, capacidade)

        rota_final, custo_fo_final = cvrp_busca_local.dois_opt_primeira_melhora(rota_inicial, matriz_distancias)

        fim = time.time()
        tempo_execucao = fim - inicio

        print(f"Instancia: {ficheiro} | Clientes: {num_clientes} | Capacidade veiculo: {capacidade}")
        print(f"Custo (fo) inicial [vizinho mais proximo]: {custo_fo_inicial}")
        print(f"Custo (fo) final [busca local]: {custo_fo_final}")
        print(f"Tempo de Execução: {tempo_execucao:.6f} seg")
        print("-" * 50)

if __name__ == "__main__":
    main()