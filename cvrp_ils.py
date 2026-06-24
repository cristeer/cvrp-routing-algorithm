import random
from cvrp_busca_local import custo_rota, custo_total, carga_rota
from cvrp_vnd import vnd, rota_plana_para_rotas, rotas_para_rota_plana

# perturbação: relocate aleatório de k clientes
def perturbar(rotas, demandas, capacidade, k, seed=None):
    rng = random.Random(seed)
    rotas_novas = [r[:] for r in rotas]

    movimentos = 0
    tentativas = 0
    max_tentativas = 10 * k

    while movimentos < k and tentativas < max_tentativas:
        tentativas += 1

        # escolhe rota de origem com pelo menos 1 cliente
        rotas_nao_vazias = [i for i, r in enumerate(rotas_novas) if r]
        if not rotas_nao_vazias:
            break
        i = rng.choice(rotas_nao_vazias)
        pos = rng.randrange(len(rotas_novas[i]))
        cliente = rotas_novas[i][pos]

        j = rng.randrange(len(rotas_novas))

        # verifica capacidade (se muda de rota)
        if j != i:
            if carga_rota(rotas_novas[j], demandas) + demandas[cliente] > capacidade:
                continue

        # remove o cliente da origem
        origem_sem = rotas_novas[i][:pos] + rotas_novas[i][pos + 1:]

        # insere em posição aleatória no destino
        base = origem_sem if j == i else rotas_novas[j]
        ins = rng.randint(0, len(base))
        nova_destino = base[:ins] + [cliente] + base[ins:]

        if j == i:
            rotas_novas[i] = nova_destino
        else:
            rotas_novas[i] = origem_sem
            rotas_novas[j] = nova_destino

        # descarta rotas vazias
        rotas_novas = [r for r in rotas_novas if r]
        movimentos += 1

    return rotas_novas

def ils(rota_inicial_plana, matriz_distancias, demandas, capacidade, max_iter=300, k=4, seed=42): 
    rng = random.Random(seed)

    #  solução inicial: VND sobre a solução construtiva 
    rota_atual_plana, custo_atual = vnd(
        rota_inicial_plana, matriz_distancias, demandas, capacidade)

    melhor_rota_plana = rota_atual_plana[:]
    melhor_custo = custo_atual

    for _ in range(max_iter):
        # perturbação
        rotas_atual = rota_plana_para_rotas(rota_atual_plana)
        iter_seed = rng.randint(0, 10**9)
        rotas_perturbadas = perturbar(rotas_atual, demandas, capacidade, k, seed=iter_seed)
        rota_perturbada_plana = rotas_para_rota_plana(rotas_perturbadas)

        # busca local sobre a solução perturbada
        rota_otimizada_plana, custo_otimizado = vnd(
            rota_perturbada_plana, matriz_distancias, demandas, capacidade)

        # atualiza melhor solução global
        if custo_otimizado < melhor_custo - 1e-9:
            melhor_rota_plana = rota_otimizada_plana[:]
            melhor_custo = custo_otimizado

        # critério de aceitação: best accept
        if custo_otimizado < custo_atual - 1e-9:
            rota_atual_plana = rota_otimizada_plana
            custo_atual = custo_otimizado

    return melhor_rota_plana, melhor_custo
