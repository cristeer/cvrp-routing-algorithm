import matplotlib.pyplot as plt
import numpy as np

# 1. Insira aqui os dados da sua tabela final
instancias = ['A-n32-k5', 'A-n33-k6', 'A-n36-k5', 'A-n45-k7', 'A-n63-k10', 'B-n31-k5', 'B-n34-k5', 'B-n38-k6', 'B-n44-k7', 'B-n66-k9', 'P-n16-k8', 'P-n19-k2', 'P-n23-k8', 'P-n40-k5', 'P-n50-k10']
otimo = [784, 742, 799, 1146, 1314, 672, 788, 805, 909, 1316, 450, 212, 529, 458, 696]
mc_savings = [796, 742, 805, 1154, 1325, 673, 792, 819, 928, 1360, 465, 219, 534, 474, 706]
nearest_neighbor = [1145, 1042, 1077, 1428, 1934, 887, 886, 1268, 1274, 1679, 497, 250, 746, 682, 907]

x = np.arange(len(instancias))  # Localização das labels no eixo X
largura = 0.25  # Largura das barras

# fig, ax = plt.subplots(figsize=(10, 6))
fig, ax = plt.subplots(figsize=(12, 6))
# 2. Criando as barras
rects1 = ax.bar(x - largura, otimo, largura, label='Ótimo da Literatura (fo*)', color='#2ca02c')
rects2 = ax.bar(x, mc_savings, largura, label='M.C. Savings (Oliveira et al.)', color='#1f77b4')
rects3 = ax.bar(x + largura, nearest_neighbor, largura, label='Nearest Neighbor (Proposto)', color='#d62728')

# 3. Formatando o gráfico (Padrão Acadêmico)
ax.set_ylabel('Custo Total da Rota (Distância)', fontsize=12)
ax.set_title('Heurísticas vs. Solução Ótima', fontsize=14)
ax.set_xticks(x)
# ax.set_xticklabels(instancias, fontsize=11)
ax.set_xticklabels(instancias, rotation=45, ha='right', fontsize=10)
ax.legend(fontsize=11)

# Adiciona uma grade de fundo leve para facilitar a leitura dos valores
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 4. Ajustar layout e salvar
plt.tight_layout()
plt.savefig('grafico_comparativo.png', dpi=300) # Salva com alta resolução
print("Gráfico 'grafico_comparativo.png' gerado com sucesso!")
plt.show()