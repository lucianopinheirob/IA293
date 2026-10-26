# %%
import numpy as np

#%%
# Questão 2
def inv_mult(a, Base):

    # preciso de um número i t.q. que i * (a mod N) mod N == 1

    a = np.rint(a)

    a_mod_N = a % Base
    for i in range(Base):
        if (i * a_mod_N) % Base == 1:
            return i

def text_to_num(S_text):
    # Considerando um mapa A - 1 ... Z - 26
    # Retorna o asc2 - 96 de cada char de S
    
    S_num = [ord(char) - 96 for char in S_text]
    
    return S_num

def num_to_text(S_num):

    # Considerando um mapa A - 1 ... Z - 26
    
    # Retorna o caracetere correspondente ao asc2+96 de cada número da lista
    
    S_text = ''.join(chr(i+96) for i in S_num)
    
    return S_text

def Cifra_Hill(Chave_Cifr, S_num, Base):
    
    N = len(Chave_Cifr)
    
    S_Cifr = np.array([])

    # Fazendo um padding com 0 caso a seq. não seja divisível por N
    n_Padding = len(S_num) % N
    if n_Padding != 0:
        for i in range(0, N-n_Padding):  
            S_num = np.append(S_num, 0)
    #print("S_num_pad = ", S_num)

    # Particiona a seq de entrada em fatias de comprimento N, realiza a cifra e concatena.
    for i in range(0,len(S_num),N):
        
        S_Slice = S_num[i:i+N]

        #print(S_Slice)
        
        S_Cifr = np.append(S_Cifr, Chave_Cifr @ S_Slice)
    
    return (S_Cifr % Base).astype(int)

Base = 26

print("Inverso multiplicativo de -5 na base 26:", inv_mult(-5, Base))

S_text = "banana"
print(f"S_tex: {S_text}")
S_text_to_num = text_to_num("banana")
print(f"S_text_to_num: {S_text_to_num}")
S_num_to_text = num_to_text(S_text_to_num)
print(f"S_num_to_text: {S_num_to_text}")

print("\n")

A = np.array([[1, 2], [3, 1]])
print(f"A: {A}")
S_num = np.array([1,2,2])
print(f"S_num: {S_num}")
S_Cifra_Hill = Cifra_Hill(A, S_num, Base)
print(f"S_Cifra_Hill: {S_Cifra_Hill}")



#%%
# Questão 3
def deHill(A, Base):
    # Autoexplicativo
    # Custo dominado pela operação de inverter que é O(len(A)^3)
    det_A = np.rint(np.linalg.det(A))
    inv_A = np.linalg.inv(A)
    inv_mult_det_A = np.rint(inv_mult(det_A, Base))
    algo = np.rint((inv_A*det_A))
    return (algo*inv_mult_det_A).astype(int) % Base


Base = 26
A = np.array([[1, 2], [3, 1]])

X = deHill(A, Base)

X

# %%
# Questão 4

# Mensagem a ser codificada
print("Mensagem original")
S_text = "matheusmelhorprof"
print(S_text)

S_num = text_to_num(S_text)

# Base para a aritmetica modular
Base = 29

# Chave de cifrar
A_1 = np.array([[7, 9], [4, 15]])
A_2 = np.array([[3, 12, 11], [1, 3, 10], [5, 5, 1]])

# Chave de decifrar
X_1 = deHill(A_1, Base)
X_2 = deHill(A_2, Base)

# Mensagens cifradas com A_1 e A_2
S_Cifra_A_1 = Cifra_Hill(A_1, S_num, Base)
S_Cifra_A_2 = Cifra_Hill(A_2, S_num, Base)

Stop_1 = -(len(A_1) - len(S_text) % len(A_1)) # Para desconsiderar o padding
Stop_2 = -(len(A_2) -len(S_text) % len(A_2))

print("\n")
print("Mensagem cifrada 1:")
print(num_to_text(S_Cifra_A_1)[:Stop_1])
print("\n")
print("Mensagem cifrada 2:")
print(num_to_text(S_Cifra_A_2)[:Stop_2])

# Mensagens decifradas com X_1 e X_2
S_Decifra_A_1 = Cifra_Hill(X_1, S_Cifra_A_1, Base)
S_Decifra_A_2 = Cifra_Hill(X_2, S_Cifra_A_2, Base)

# Mensagem decifrada em texto
print("\n")
print("Mensagem decifrada 1:")
print(num_to_text(S_Decifra_A_1)[:Stop_1])

print("\n")
print("Mensagem decifrada 2:")
print(num_to_text(S_Decifra_A_2)[:Stop_2])