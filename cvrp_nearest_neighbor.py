def nearest_neighbor (matriz_distancias, num_clientes, demandas, capacidade):
    visitados = [False] * num_clientes
    visitados[0] = True  # Começa no depósito
    clientes_visitados = 1
    
    rota = [0]  # guardar sequencia da rota que começa no depósito
    custo_total = 0.0
    carga_atual = 0
    cliente_atual = 0

    while clientes_visitados < num_clientes:
        menor_dist = float('inf') 
        prox_cliente = None

        for i in range (1, num_clientes):
            if not visitados[i] and matriz_distancias[cliente_atual][i] < menor_dist:
                if carga_atual + demandas[i] <= capacidade:
                    menor_dist = matriz_distancias[cliente_atual][i]
                    prox_cliente = i

        if prox_cliente is not None:
            custo_total += menor_dist
            cliente_atual = prox_cliente
            visitados[cliente_atual] = True
            carga_atual += demandas[cliente_atual]
            rota.append(cliente_atual)
            clientes_visitados += 1
        else:
            # atingiu a capacidade, volta para o depósito
            custo_total += matriz_distancias[cliente_atual][0]
            rota.append(0)
            cliente_atual = 0
            carga_atual = 0
        
    custo_total += matriz_distancias[cliente_atual][0]  # Volta para o depósito no final
    rota.append(0)

    return rota, custo_total
                
