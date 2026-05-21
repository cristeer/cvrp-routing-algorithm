import math

def calcular_distancia (x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return round(distancia)

def ler_instancias (file_path):
    coordenadas = []
    demandas = []
    capacidade = 0

    lendo_coordenadas = False
    lendo_demandas = False
    
    with open (file_path, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if linha.startswith("CAPACITY"):
                # separa na lista ['CAPACITY', 'x'] e extrai cap
                capacidade = int(linha.split(":")[-1].strip())
                continue

            if linha.startswith("NODE_COORD_SECTION"):
                lendo_coordenadas = True
                lendo_demandas = False
                continue

            if linha.startswith("DEMAND_SECTION"):
                lendo_demandas = True
                lendo_coordenadas = False
                continue
            
            if linha.startswith("DEPOT_SECTION") or linha.startswith("EOF"):
                break
        
            if lendo_coordenadas:
                # .split() dividir a linha em partes (ID, X, Y)
                partes = linha.split()

                if len(partes) >= 3:
                    x = float(partes[1])
                    y = float(partes[2])
                    coordenadas.append((x, y))
            elif lendo_demandas:
                partes = linha.split()

                if len(partes) >= 2:
                    demanda = int(partes[1])
                    demandas.append(demanda)

    num_cidades = len(coordenadas)

    # criar matriz de distâncias inicializada com zeros
    matriz_distancias = []
    for i in range (num_cidades):
        linha = []
        for j in range(num_cidades):
            linha.append(0)
        matriz_distancias.append(linha)
    
    # preencher a matriz com as distancias
    for i in range(num_cidades):
        for j in range(num_cidades):
            if i != j:
                dist = calcular_distancia(
                    coordenadas[i][0], coordenadas[i][1], coordenadas[j][0], coordenadas[j][1]
                    )
                matriz_distancias[i][j] = dist

    return matriz_distancias, num_cidades, demandas, capacidade