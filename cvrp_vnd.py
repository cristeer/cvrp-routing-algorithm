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


def custo_rota(rota, matriz_distancias):
    # deposito -> clientes -> deposito
    if not rota:
        return 0
    custo = matriz_distancias[0][rota[0]]
    for i in range(len(rota) - 1):
        custo += matriz_distancias[rota[i]][rota[i + 1]]
    custo += matriz_distancias[rota[-1]][0]
    return custo


def custo_total(rotas, matriz_distancias):
    total = 0
    for rota in rotas:
        total += custo_rota(rota, matriz_distancias)
    return total


def carga_rota(rota, demandas):
    carga = 0
    for cliente in rota:
        carga += demandas[cliente]
    return carga


def vizinhanca_relocate(rotas, matriz_distancias, demandas, capacidade):
    for i in range(len(rotas)):
        origem = rotas[i]
        for pos in range(len(origem)):
            cliente = origem[pos]
            origem_sem = origem[:pos] + origem[pos + 1:]

            for j in range(len(rotas)):
                # checa capacidade quando muda de veiculo
                if j != i:
                    if carga_rota(rotas[j], demandas) + demandas[cliente] > capacidade:
                        continue

                # base onde o cliente vai ser inserido
                base = origem_sem if j == i else rotas[j]

                for ins in range(len(base) + 1):
                    nova_destino = base[:ins] + [cliente] + base[ins:]

                    if j == i:
                        # so a rota i muda
                        delta = custo_rota(nova_destino, matriz_distancias) \
                                - custo_rota(origem, matriz_distancias)
                    else:
                        # rota i perde o cliente, rota j ganha
                        delta = (custo_rota(origem_sem, matriz_distancias)
                                 + custo_rota(nova_destino, matriz_distancias)) \
                                - (custo_rota(origem, matriz_distancias)
                                   + custo_rota(rotas[j], matriz_distancias))

                    if delta < -1e-9:
                        # aplica a primeira melhora encontrada
                        if j == i:
                            rotas[i] = nova_destino
                        else:
                            rotas[i] = origem_sem
                            rotas[j] = nova_destino
                        # descarta rotas que ficaram vazias
                        rotas[:] = [r for r in rotas if r]
                        return True
    return False



def vizinhanca_swap(rotas, matriz_distancias, demandas, capacidade):
    for i in range(len(rotas)):
        for j in range(i + 1, len(rotas)):
            carga_i = carga_rota(rotas[i], demandas)
            carga_j = carga_rota(rotas[j], demandas)
            custo_i = custo_rota(rotas[i], matriz_distancias)
            custo_j = custo_rota(rotas[j], matriz_distancias)

            for a in range(len(rotas[i])):
                for b in range(len(rotas[j])):
                    cli_a = rotas[i][a]
                    cli_b = rotas[j][b]

                    # capacidade depois da troca
                    nova_carga_i = carga_i - demandas[cli_a] + demandas[cli_b]
                    nova_carga_j = carga_j - demandas[cli_b] + demandas[cli_a]
                    if nova_carga_i > capacidade or nova_carga_j > capacidade:
                        continue

                    nova_i = rotas[i][:]
                    nova_j = rotas[j][:]
                    nova_i[a] = cli_b
                    nova_j[b] = cli_a

                    delta = (custo_rota(nova_i, matriz_distancias)
                             + custo_rota(nova_j, matriz_distancias)) \
                            - (custo_i + custo_j)

                    if delta < -1e-9:
                        rotas[i] = nova_i
                        rotas[j] = nova_j
                        return True
    return False


def vizinhanca_2opt(rotas, matriz_distancias, demandas, capacidade):
    for r in range(len(rotas)):
        rota = rotas[r]
        custo_atual = custo_rota(rota, matriz_distancias)
        for i in range(len(rota) - 1):
            for j in range(i + 1, len(rota)):
                nova = rota[:i] + rota[i:j + 1][::-1] + rota[j + 1:]
                if custo_rota(nova, matriz_distancias) < custo_atual - 1e-9:
                    rotas[r] = nova
                    return True
    return False


def vnd(rota_inicial_plana, matriz_distancias, demandas, capacidade):
    rotas = rota_plana_para_rotas(rota_inicial_plana)

    vizinhancas = [vizinhanca_relocate, vizinhanca_swap, vizinhanca_2opt]

    k = 0
    while k < len(vizinhancas):
        melhorou = vizinhancas[k](rotas, matriz_distancias, demandas, capacidade)
        if melhorou:
            k = 0  # volta para a primeira vizinhanca
        else:
            k += 1

    rota_final_plana = rotas_para_rota_plana(rotas)
    return rota_final_plana, custo_total(rotas, matriz_distancias)