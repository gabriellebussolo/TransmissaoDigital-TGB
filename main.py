
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

# Testes de uso
entrada = "Hello"
binario = ascii_to_binary(entrada)
print(binario)

print(binary_to_ascii("0100100001100101011011000110110001101111"))