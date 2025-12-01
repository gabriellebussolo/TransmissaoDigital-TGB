
import textwrap
import numpy as np
import matplotlib.pyplot as plt

# Converte uma string ASCII em binário
def ascii_to_binary(texto):
    binario_final = ""
    
    for char in texto:
        codigo_ascii = ord(char) # Pega o código ASCII do caractere
        binario = format(codigo_ascii, '08b') # Converte para binário em 8 bits
        binario_final += binario # Adiciona o binário a string final

    return binario_final

# Converte binário em ASCII
def binary_to_ascii(binario):
    bytes_separados = textwrap.wrap(binario, 8) # Quebra a string em cada byte (8 bits)
    string_final = ""                       
    
    for byte in bytes_separados:
        numero = int(byte, 2) # Converte o binário para um número inteiro
        caractere = chr(numero) # Converte o número inteiro para ASCII
        string_final += caractere # Guarda o caractere na strig final
    
    return string_final

# Codificador de canal NRZ-S
# -1 = -V (nível negativo)
# +1 = +V (nível positivo)
def codificador_canal_NRZS(binario):
    sinal_nrz = [] # Lista onde ficará a saída
    nivel_atual = +1 # Começa em nível positivo (+V)
    
    for bit in binario:
        if bit == '0':
            # o 0 gera inversão de nível
            nivel_atual *= -1
        # Se o bit for 1, nada muda (mantém o nível)
        sinal_nrz.append(nivel_atual)
    
    return sinal_nrz

# Decodificador de canal NRZ-S
def decodificador_canal_NRZS(sinal):
    binario = []
    
    # O primeiro nível não tem "anterior", então assumimos o nível inicial +1 que definimos no codificador
    nivel_anterior = +1

    for nivel in sinal:
        if nivel == nivel_anterior:
            binario.append('1')     # Mesmo nível → bit 1
        else:
            binario.append('0')     # Nível mudou → bit 0
        
        # Atualiza o nível anterior
        nivel_anterior = nivel

    return ''.join(binario)

# Solicita uma entrada do usuário
texto = input("Digite uma string ASCII para a transmissão: ")

# Converte a string para binário
binario = ascii_to_binary(texto)
print(f"Representação binária: {binario}")

# Codifica o binário usando NRZ-S
sinal_nrzs = codificador_canal_NRZS(binario)
print(f"Sinal NRZ-S: {sinal_nrzs}")

# Decodifica o sinal NRZ-S de volta para binário
binario_decodificado = decodificador_canal_NRZS(sinal_nrzs)
print(f"Binário decodificado: {binario_decodificado}")

# Converte o binário decodificado de volta para ASCII
texto_decodificado = binary_to_ascii(binario_decodificado)
print(f"String ASCII decodificada: {texto_decodificado}")