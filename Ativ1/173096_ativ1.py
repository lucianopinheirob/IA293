# %%
import numpy as np
import matplotlib.pyplot as plt


def produto_vetorial(u, v):
    return u[0] * v[1] - u[1] * v[0]


def ponto_no_triangulo(P, A, B, C):
    AB = [B[0] - A[0], B[1] - A[1]]
    AP = [P[0] - A[0], P[1] - A[1]]

    BC = [C[0] - B[0], C[1] - B[1]]
    BP = [P[0] - B[0], P[1] - B[1]]

    CA = [A[0] - C[0], A[1] - C[1]]
    CP = [P[0] - C[0], P[1] - C[1]]

    produto1 = produto_vetorial(AB, AP)
    produto2 = produto_vetorial(BC, BP)
    produto3 = produto_vetorial(CA, CP)
    
    # Se tiver ordenado em sentido anti-horário o ponto deve estar à direita dos 3 vetores, ou seja os prod. vet. devem ser todos positivos
    todos_positivos = produto1 >= 0 and produto2 >= 0 and produto3 >= 0 
    
    # Se tiver ordenado em sentido horário o ponto deve estar à esquerda dos 3 vetores, ou seja os prod. vet. devem ser todos negativos
    todos_negativos = produto1 <= 0 and produto2 <= 0 and produto3 <= 0

    # Obs.: a igualdade refere-se ao caso em que o ponto está exatamente em cima da aresta do triângulo.

    return todos_positivos or todos_negativos


def ponto_no_poligono(P, vertices):
    N = len(vertices)

    # O loop abaixo particiona perfeitamente o polígono convexo em triângulos
    for i in range(1, N - 1):
        A = vertices[0]
        B = vertices[i]
        C = vertices[i + 1]

        # Se há ponto dentro de algum dos triângulos internos do polígono, o ponto está dentro do polígono
        if ponto_no_triangulo(P, A, B, C):
            return True 

    return False # Se não há ponto em nenhum triângulo o ponto está fora


def area_monte_carlo(vertices, M, seed=0):
    # Gera nuvem de M pontos no quadrado [0,1]^2
    rng = np.random.default_rng(seed)
    pontos = rng.random((M, 2))

    pontos_dentro = []
    pontos_fora = []

    # Verifica se ponto está dentro ou fora
    for P in pontos:
        if ponto_no_poligono(P, vertices):
            pontos_dentro.append(P)
        else:
            pontos_fora.append(P)

    # Cálcula área com base na razão pontos dentro / pontos gerados
    area = len(pontos_dentro) / M

    return area, pontos_dentro, pontos_fora

def area_triangulo_Heron(A,B,C):
    # Só implementa Heron normal no triangulo

    mod_AB = np.sqrt((B[1] - A[1])**2 + (B[0] - A[0])**2)
    mod_BC = np.sqrt((C[1] - B[1])**2 + (C[0] - B[0])**2)
    mod_CA = np.sqrt((A[1] - C[1])**2 + (A[0] - C[0])**2)
    
    p = (mod_AB + mod_BC + mod_CA)/2

    area_triangulo = np.sqrt(p*(p-mod_AB)*(p-mod_BC)*(p-mod_CA))

    return area_triangulo

def area_poligono_Heron(vertices):
    
    N = len(vertices)
    S = 0

    # O loop abaixo particiona perfeitamente o polígono convexo em triângulos
    for i in range(1, N - 1):
        A = vertices[0]
        B = vertices[i]
        C = vertices[i + 1]
        
        # Soma as áreas de cada triângulo do polígono
        S += area_triangulo_Heron(A, B, C) 

    return S

# O plot foi obra do Gepeto
def plotar(vertices, pontos_dentro, pontos_fora, M, area, area_teo):
    x_dentro = []
    y_dentro = []
    x_fora = []
    y_fora = []

    for P in pontos_dentro:
        x_dentro.append(P[0])
        y_dentro.append(P[1])

    for P in pontos_fora:
        x_fora.append(P[0])
        y_fora.append(P[1])

    # Monta o contorno do polígono.
    x_contorno = []
    y_contorno = []

    for vertice in vertices:
        x_contorno.append(vertice[0])
        y_contorno.append(vertice[1])

    # Repete o primeiro vértice para fechar o contorno.
    x_contorno.append(vertices[0][0])
    y_contorno.append(vertices[0][1])

    plt.figure(figsize=(7, 7))
    plt.scatter(x_fora, y_fora, color="black", s=5, label="Pontos externos")
    plt.scatter(x_dentro, y_dentro, color="blue", s=5, label="Pontos internos")
    plt.plot(x_contorno, y_contorno, color="red", label="Contorno")

    plt.title(f"M = {M} | Área estimada = {area:.4f} | Área teórica = {area_teo:.4f}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect("equal")
    #plt.legend()
    plt.show()


# %%

# Questão 02

# Vértices ordenados ao redor do contorno do polígono.
verticess = [[(0.1, 0.1), (0.1, 0.9), (0.9, 0.9)], # Triângulo
             [(0.1, 0.1), (0.1, 0.9), (0.9, 0.9), (0.9, 0.1) ]] # Quadrado 

# Quantidade de pontos a serem gerados aleatoriamente dentro do quadrado
Ms = [100, 1000, 10000]

for vertices in verticess:
    for M in Ms:
        area_teorica = area_poligono_Heron(vertices)
        area_estimada, pontos_dentro, pontos_fora = area_monte_carlo(vertices, M)
        erro = abs(area_estimada - area_teorica)

        #print(f"Área teórica:  {area_teorica:.4f}")
        #print(f"Área estimada: {area_estimada:.4f}")

        plotar(vertices, pontos_dentro, pontos_fora, M, area_estimada, area_teorica)

# %%

# Questão 04

# A sugestão dos vertices foi do Gepeto
verticess = [
    [(0.9, 0.7), (0.9, 0.3), (0.7, 0.1), (0.3, 0.1), (0.1, 0.3), (0.1, 0.7), (0.3, 0.9), (0.7, 0.9)], # 8 lados
    [(0.890, 0.660), (0.878, 0.420), (0.753, 0.270), (0.541, 0.172), (0.245, 0.202), (0.101, 0.365), (0.100, 0.523), (0.236, 0.720), (0.532, 0.839), (0.752, 0.800)], # 10 lados
    [(0.900, 0.500), (0.846, 0.300), (0.700, 0.154), (0.500, 0.100), (0.300, 0.154), (0.154, 0.300), (0.100, 0.500), (0.154, 0.700), (0.300, 0.846), (0.500, 0.900), (0.700, 0.846), (0.846, 0.700)] # 12 lados
]

# Quantidade de pontos a serem gerados aleatoriamente dentro do quadrado
M = 10000

for vertices in verticess:
    area_teorica = area_poligono_Heron(vertices)
    area_estimada, pontos_dentro, pontos_fora = area_monte_carlo(vertices, M)
    erro = abs(area_estimada - area_teorica)

    #print(f"Área teórica:  {area_teorica:.4f}")
    #print(f"Área estimada: {area_estimada:.4f}")

    plotar(vertices, pontos_dentro, pontos_fora, M, area_estimada, area_teorica)

# %%
