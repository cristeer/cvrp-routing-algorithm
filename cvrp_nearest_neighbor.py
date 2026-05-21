def nearest_neighbor (matriz_distancias, num_cidades, demandas, capacidade):
    visitados = [False] * num_cidades
    visitados[0] = True  # Começa no depósito
    cidades_visitadas = 1
    
    custo_total = 0.0
    carga_atual = 0
    cidade_atual = 0

    while cidades_visitadas < num_cidades:
        menor_dist = float('inf') 
        prox_cidade = None

        for i in range (1, num_cidades):
            if not visitados[i] and matriz_distancias[cidade_atual][i] < menor_dist:
                if carga_atual + demandas[i] <= capacidade:
                    menor_dist = matriz_distancias[cidade_atual][i]
                    prox_cidade = i

            if prox_cidade is not None:
                custo_total += menor_dist
                cidade_atual = prox_cidade
                visitados[cidade_atual] = True
                carga_atual += demandas[cidade_atual]
                cidades_visitadas += 1
            else:
                #atingiu a capacidade, volta para o depósito
                custo_total += matriz_distancias[cidade_atual][0]
                cidade_atual = 0
                carga_atual = 0
        
    custo_total += matriz_distancias[cidade_atual][0]  # Volta para o depósito no final
    return custo_total
                
