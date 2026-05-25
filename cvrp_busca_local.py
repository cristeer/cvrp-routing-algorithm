def calcular_custo_rota (rota, matriz_distancias):
    custo = 0.0
    for i in range(len(rota) - 1):
        custo += matriz_distancias[rota[i]][rota[i+1]]
    return custo

def dois_opt_primeira_melhora (rota_inicial, matriz_distancias):
    melhor_rota = rota_inicial.copy()
    melhor_custo = calcular_custo_rota(melhor_rota, matriz_distancias)
    melhora = True

    while melhora:
        melhora = False

        #inverter os trechos i e j | ignorando depósito no início e no final 
        for i in range(1, len(melhor_rota) - 2):
            for j in range(i + 1, len(melhor_rota) - 1):
            
                if 0 in melhor_rota[i:j+1]:  # não inverter se o trecho conter depósito
                    continue
                
                #melhor_rota[i:j+1][::-1] pega o trecho do cliente i até o j e inverte a ordem 
                nova_rota = melhor_rota[:i] + melhor_rota[i:j+1][::-1] + melhor_rota[j+1:]
                novo_custo = calcular_custo_rota(nova_rota, matriz_distancias)

                # metodo primeira melhora
                if novo_custo < melhor_custo:
                    melhor_rota = nova_rota
                    melhor_custo = novo_custo
                    melhora = True
                    break # sai do loop j para tentar outra inversão 
                
            if melhora:
                break # Interrompe 'for i' e recomeça do zero com a nova rota
    
    return melhor_rota, melhor_custo
