import textwrap
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# ASCII ↔ BINÁRIO
# ============================================================

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


# ============================================================
# CODIFICAÇÃO MANCHESTER
# ============================================================

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


# ============================================================
# MODULAÇÃO BPSK (com entrada Manchester)
# ============================================================

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


# ============================================================
# MODULAÇÃO QPSK (pares de bits)
# ============================================================

def qpsk_modulation(binario, fc=2, amostragem=200):
    if len(binario) % 2 != 0:
        binario += "0"   # padding

    pares = [binario[i:i+2] for i in range(0, len(binario), 2)]

    fase_map = {
        "00": np.pi/4,
        "01": 3*np.pi/4,
        "11": -3*np.pi/4,
        "10": -np.pi/4
    }

    t_total = len(pares)
    t = np.linspace(0, t_total, t_total * amostragem)

    sinal = np.zeros_like(t)

    idx = 0
    for par in pares:
        fase = fase_map[par]
        inicio = idx * amostragem
        fim = (idx + 1) * amostragem
        sinal[inicio:fim] = np.cos(2*np.pi*fc*t[inicio:fim] + fase)
        idx += 1

    return t, sinal


# ============================================================
# PLOTS
# ============================================================

def plot_all(manchester, t_bpsk, bpsk_signal, t_qpsk, qpsk_signal):
    fig, axs = plt.subplots(3, 1, figsize=(13, 8), sharex=False)

    axs[0].step(range(len(manchester)), manchester, where='post')
    axs[0].set_title("Sinal Manchester")
    axs[0].set_ylabel("Amplitude")
    axs[0].grid(True)

    axs[1].plot(t_bpsk, bpsk_signal)
    axs[1].set_title("BPSK Modulado (com entrada Manchester)")
    axs[1].set_ylabel("Amplitude")
    axs[1].grid(True)

    axs[2].plot(t_qpsk, qpsk_signal)
    axs[2].set_title("QPSK Modulado")
    axs[2].set_xlabel("Tempo")
    axs[2].set_ylabel("Amplitude")
    axs[2].grid(True)

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
print("\n[2] SINAL MANCHESTER GERADO:")
print(sinal_manchester)

binario_decod_manchester = manchester_decode(sinal_manchester)
print("\n[3] DECODIFICAÇÃO MANCHESTER → BINÁRIO:")
print(binario_decod_manchester)

ascii_decodificado = binary_to_ascii(binario_decod_manchester)
print("\n[4] ASCII RECUPERADO:")
print(ascii_decodificado)

t_bpsk, sinal_bpsk = bpsk_modulation(sinal_manchester)
t_qpsk, sinal_qpsk = qpsk_modulation(binario)

plot_all(sinal_manchester, t_bpsk, sinal_bpsk, t_qpsk, sinal_qpsk)
