import cvrp_busca_local

def rota_plana_para_rotas(rota_plana):
    # [0, c1, c2, 0, c3, 0]  ->  [[c1, c2], [c3]]
    rotas = []
    atual = []
    for no in rota_plana:
        if no == 0:
            if atual:
                rotas.append(atual)
                atual = []
        else:
            atual.append(no)
    if atual:
        rotas.append(atual)
    return rotas

def rotas_para_rota_plana(rotas):
    # [[c1, c2], [c3]]  ->  [0, c1, c2, 0, c3, 0]
    plana = [0]
    for rota in rotas:
        for cliente in rota:
            plana.append(cliente)
        plana.append(0)
    return plana

def vnd(rota_inicial_plana, matriz_distancias, demandas, capacidade):
    rotas = rota_plana_para_rotas(rota_inicial_plana)
    vizinhancas = [cvrp_busca_local.vizinhanca_relocate, cvrp_busca_local.vizinhanca_swap, cvrp_busca_local.vizinhanca_2opt]

    k = 0
    while k < len(vizinhancas):
        melhorou = vizinhancas[k](rotas, matriz_distancias, demandas, capacidade)
        if melhorou:
            k = 0  # volta para a primeira vizinhanca
        else:
            k += 1

    rota_final_plana = rotas_para_rota_plana(rotas)
    return rota_final_plana, cvrp_busca_local.custo_total(rotas, matriz_distancias)