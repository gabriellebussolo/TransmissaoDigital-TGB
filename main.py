import textwrap
import numpy as np
import matplotlib.pyplot as plt

def ascii_to_binary(texto):
    binario_final = ""
    for char in texto:
        codigo_ascii = ord(char)
        binario = format(codigo_ascii, '08b')
        binario_final += binario
    return binario_final

def binary_to_ascii(binario):
    bytes_separados = textwrap.wrap(binario, 8)
    string_final = ""
    for byte in bytes_separados:
        numero = int(byte, 2)
        caractere = chr(numero)
        string_final += caractere
    return string_final

def manchester_encode(binario):
    sinal = []
    for bit in binario:
        if bit == "1":
            sinal += [1, -1]   # HIGH → LOW
        else:
            sinal += [-1, 1]   # LOW → HIGH
    return sinal

def manchester_decode(sinal):
    binario = ""
    for i in range(0, len(sinal), 2):
        par = sinal[i:i+2]
        if par == [1, -1]:
            binario += "1"
        else:
            binario += "0"
    return binario

def awgn(signal, sigma):
    noise = np.random.normal(0, sigma, len(signal))
    return signal + noise


def bpsk_modulation(sinal, fc=0.5, amostragem=100):
    t_total = len(sinal)
    t = np.linspace(0, t_total, t_total * amostragem)

    portadora = np.cos(2*np.pi*fc*t)
    sinal_bpsk = np.zeros_like(t)

    idx = 0
    for nivel in sinal:
        inicio = idx * amostragem
        fim = (idx + 1) * amostragem
        sinal_bpsk[inicio:fim] = nivel * portadora[inicio:fim]
        idx += 1

    return t, sinal_bpsk

def bpsk_demodulation(received, fc=0.5, amostragem=100):
    t = np.linspace(0, len(received)/amostragem, len(received))
    portadora = np.cos(2*np.pi*fc*t)

    # Multiplica pela portadora
    sinal_multiplicado = received * portadora

    # Integra símbolo a símbolo
    num_simbolos = len(received) // amostragem
    manchester_recuperado = []

    for i in range(num_simbolos):
        inicio = i * amostragem
        fim = (i + 1) * amostragem
        energia = np.sum(sinal_multiplicado[inicio:fim])

        if energia >= 0:
            manchester_recuperado.append(1)
        else:
            manchester_recuperado.append(-1)

    return manchester_recuperado


def qpsk_modulation(binario, fc=2, amostragem=200):
    # O QPSK mapeia 2 bits por símbolo, se houver número ímpar de bits, adiciona um zero no final
    if len(binario) % 2 != 0:
        binario += "0"   

    # Divide a string binária em grupos de 2 bits
    pares = [binario[i:i+2] for i in range(0, len(binario), 2)]

    # Mapeamento de fase para cada par de bits
    mapa_IQ = {
        "00": ( 1,  1),
        "01": (-1,  1),
        "11": (-1, -1),
        "10": ( 1, -1)
    }

    # Quantidade total de símbolos.
    t_total = len(pares)
    
    # Cria o eixo de tempo
    t = np.linspace(0, t_total, t_total * amostragem)
    
    # Portadoras Q/I
    carrier_I = np.cos(2*np.pi*fc*t)
    carrier_Q = np.sin(2*np.pi*fc*t)

    # Cria um vetor cheio de zeros para o sinal modulado
    sinal = np.zeros_like(t)

    # Monta a QPSK, obtendo a fase correta para cada par de bits normalização de energia
    norm = 1/np.sqrt(2)

    # 6) construção símbolo a símbolo
    for k, par in enumerate(pares):
        I, Q = mapa_IQ[par]

        inicio = k * amostragem
        fim = (k + 1) * amostragem

        c = carrier_I[inicio:fim]
        s = carrier_Q[inicio:fim]

        sinal[inicio:fim] = norm * (I * c + Q * s)

    return t, sinal

def qpsk_demodulation(received, fc=2, amostragem=200):
    # Cria o eixo de tempo
    t = np.linspace(0, len(received)/amostragem, len(received))

    portadora_I = np.cos(2*np.pi*fc*t)
    portadora_Q = np.sin(2*np.pi*fc*t)

    # Dividir o sinal recebido em símbolos
    num_simbolos = len(received) // amostragem
    bits = ""

    # Para cada símbolo, correlaciona com as portadoras I e Q
    for i in range(num_simbolos):
        inicio = i * amostragem
        fim = (i + 1) * amostragem

        trecho = received[inicio:fim]

        # correlaciona
        I = np.sum(trecho * portadora_I[inicio:fim])
        Q = np.sum(trecho * portadora_Q[inicio:fim])

        # decisão por quadrante
        if I > 0 and Q > 0:
            bits += "00"
        elif I < 0 and Q > 0:
            bits += "01"
        elif I < 0 and Q < 0:
            bits += "11"
        else:
            bits += "10"

    return bits


def plot_all(manchester, 
             t_bpsk, bpsk, bpsk_ruido,
             t_qpsk, qpsk, qpsk_ruido):

    fig, axs = plt.subplots(5, 1, figsize=(13, 11), sharex=False)

    axs[0].step(range(len(manchester)), manchester, where='post')
    axs[0].set_title("Manchester")
    axs[0].grid(True)

    axs[1].plot(t_bpsk, bpsk)
    axs[1].set_title("BPSK")
    axs[1].grid(True)

    axs[2].plot(t_bpsk, bpsk_ruido)
    axs[2].set_title("BPSK com Ruído (AWGN)")
    axs[2].grid(True)

    axs[3].plot(t_qpsk, qpsk)
    axs[3].set_title("QPSK")
    axs[3].grid(True)

    axs[4].plot(t_qpsk, qpsk_ruido)
    axs[4].set_title("QPSK com Ruído (AWGN)")
    axs[4].set_xlabel("Tempo")
    axs[4].grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# EXECUÇÃO
# ============================================================

texto = input("Digite uma string ASCII para a transmissão: ")

binario = ascii_to_binary(texto)
print("\n[1] BINÁRIO DA MENSAGEM:")
print(binario)

sinal_manchester = manchester_encode(binario)
print("\n[2] SINAL MANCHESTER:")
print(sinal_manchester)

binario_decod = manchester_decode(sinal_manchester)
print("\n[3] DECODIFICAÇÃO MANCHESTER:")
print(binario_decod)

ascii_recuperado = binary_to_ascii(binario_decod)
print("\n[4] ASCII RECUPERADO:")
print(ascii_recuperado)

# BPSK
t_bpsk, bpsk = bpsk_modulation(sinal_manchester)
bpsk_ruido = awgn(bpsk, sigma=0.5)

# QPSK
t_qpsk, qpsk = qpsk_modulation(binario)
qpsk_ruido = awgn(qpsk, sigma=0.5)

# =============== DEMODULAÇÃO BPSK ===============
manchester_recuperado_bpsk = bpsk_demodulation(bpsk_ruido)

binario_bpsk = manchester_decode(manchester_recuperado_bpsk)
ascii_bpsk = binary_to_ascii(binario_bpsk)

print("\n[5] MENSAGEM RECUPERADA VIA BPSK:")
print("Binário:", binario_bpsk)
print("ASCII:", ascii_bpsk)

# =============== DEMODULAÇÃO QPSK ===============
binario_qpsk = qpsk_demodulation(qpsk_ruido)

# remover padding se houver
binario_qpsk = binario_qpsk[:len(binario)]

ascii_qpsk = binary_to_ascii(binario_qpsk)

print("\n[6] MENSAGEM RECUPERADA VIA QPSK:")
print("Binário:", binario_qpsk)
print("ASCII:", ascii_qpsk)


# Plot final
plot_all(
    sinal_manchester,
    t_bpsk, bpsk, bpsk_ruido,
    t_qpsk, qpsk, qpsk_ruido
)
