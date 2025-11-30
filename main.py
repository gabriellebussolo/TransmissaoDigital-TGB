
import textwrap

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

# Codificador de canal AMI (bipolar)
def codificador_canal_AMI(binario):
    sinal_ami = [] # Lista onde ficará a saída
    ultimo_nivel = -1 # Começa em -1 para que o primeiro "1" vire +1
    
    for bit in binario:
        if bit == '1':
            # Alterna o nível: se estava -1, vira +1; se estava +1, vira -1
            ultimo_nivel *= -1
            sinal_ami.append(ultimo_nivel)
        else:
            # O zero sempre vira nível 0
            sinal_ami.append(0)
    
    return sinal_ami

# Decodificador de canal AMI (bipolar)
def decodificador_canal_AMI(sinal_ami):
    binario = []
    
    for nivel in sinal_ami:
        if nivel == 0:
            binario.append('0')  # 0 no sinal → bit 0
        else:
            binario.append('1') # +1 ou -1 → bit 1
    
    # Junta os bits em uma única string
    return ''.join(binario)

# Solicita uma entrada do usuário
texto = input("Digite uma string ASCII para a transmissão: ")

# Converte a string para binário
binario = ascii_to_binary(texto)
print(f"Representação binária: {binario}")

# Codifica o binário usando AMI
sinal_ami = codificador_canal_AMI(binario)
print(f"Sinal AMI: {sinal_ami}")

# Decodifica o sinal AMI de volta para binário
binario_decodificado = decodificador_canal_AMI(sinal_ami)
print(f"Binário decodificado: {binario_decodificado}")

# Converte o binário decodificado de volta para ASCII
texto_decodificado = binary_to_ascii(binario_decodificado)
print(f"String ASCII decodificada: {texto_decodificado}")