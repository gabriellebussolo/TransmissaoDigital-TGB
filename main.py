import textwrap
import numpy as np
import matplotlib.pyplot as plt
import random
import string
from scipy.special import erfc # Importação adicionada para a curva teórica de BER

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


def qpsk_modulation(manchester, fc=2, amostragem=200):

    # Garantir que o número de níveis seja par (2 por símbolo)
    if len(manchester) % 2 != 0:
        manchester.append(1)   # padding mínimo só pra completar par

    # Agrupa pares Manchester → símbolos (I,Q)
    pares_IQ = [(manchester[i], manchester[i+1]) 
                for i in range(0, len(manchester), 2)]

    t_total = len(pares_IQ)
    t = np.linspace(0, t_total, t_total * amostragem)

    carrier_I = np.cos(2*np.pi*fc*t)
    carrier_Q = np.sin(2*np.pi*fc*t)

    sinal = np.zeros_like(t)
    norm = 1/np.sqrt(2)

    for k, (I, Q) in enumerate(pares_IQ):
        inicio = k * amostragem
        fim = (k + 1) * amostragem
        sinal[inicio:fim] = norm * (I * carrier_I[inicio:fim] +
                                    Q * carrier_Q[inicio:fim])

    return t, sinal

def qpsk_demodulation(received, fc=2, amostragem=200):

    t = np.linspace(0, len(received)/amostragem, len(received))
    carrier_I = np.cos(2*np.pi*fc*t)
    carrier_Q = np.sin(2*np.pi*fc*t)

    num_simbolos = len(received) // amostragem
    manchester_rec = []

    for i in range(num_simbolos):
        inicio = i * amostragem
        fim = (i + 1) * amostragem
        trecho = received[inicio:fim]

        I = np.sum(trecho * carrier_I[inicio:fim])
        Q = np.sum(trecho * carrier_Q[inicio:fim])

        # decisores para recuperar os níveis Manchester
        nivel_I = 1 if I >= 0 else -1
        nivel_Q = 1 if Q >= 0 else -1

        manchester_rec += [nivel_I, nivel_Q]

    return manchester_rec

def ber_calculator(original_binary, received_binary):
    """Calcula a Taxa de Erro de Bit (BER)."""
    # Garantir que as strings tenham o mesmo tamanho
    min_len = min(len(original_binary), len(received_binary))
    original_binary = original_binary[:min_len]
    received_binary = received_binary[:min_len]

    num_errors = sum(b1 != b2 for b1, b2 in zip(original_binary, received_binary))
    
    if min_len == 0:
        return 0.0
    return num_errors / min_len

def theoretical_ber(ebno_linear):
    """Calcula a BER teórica para BPSK/QPSK (coerente) no canal AWGN."""
    # P_e = Q(sqrt(2 * Eb/N0))
    # Onde Q(x) = 0.5 * erfc(x / sqrt(2))
    return 0.5 * erfc(np.sqrt(ebno_linear))

def simulate_ber_vs_ebno(original_binary, ebno_db_range, N_sim=20):
    """Simula a BER em função de Eb/N0 para BPSK e QPSK."""
    
    # 1. Pré-processamento: Codificar em Manchester
    binario_manchester = manchester_encode(original_binary)
    
    ber_bpsk = []
    ber_qpsk = []
    
    # Fatores de amostragem/integração para normalizar o ruído AWGN:
    # A = amostragem / 2. (Resulta da integração do produto do sinal pela portadora)
    A_bpsk = 100 / 2 # amostragem=100 para BPSK
    A_qpsk = 200 / 2 # amostragem=200 para QPSK (usado na modulação QPSK)
    
    # Conversão de dB para escala linear
    ebno_linear_range = 10**(ebno_db_range / 10)
    
    for ebno_linear in ebno_linear_range:
        
        # --- Cálculo de Sigma (Variância do Ruído) ---
        
        # 1. Sigma ideal (assumindo Eb=1 na saída do filtro casado)
        sigma_ideal_bpsk = np.sqrt(1 / (2 * ebno_linear))
        sigma_ideal_qpsk = np.sqrt(1 / (4 * ebno_linear))

        # 2. ESCALONAMENTO DO RUÍDO: Multiplica pela raiz quadrada do fator de integração (A)
        # O ruído AWGN deve ser amplificado para ter o efeito correto após a integração (soma).
        sigma_bpsk = sigma_ideal_bpsk * np.sqrt(A_bpsk)
        sigma_qpsk = sigma_ideal_qpsk * np.sqrt(A_qpsk)
        
        # Inicializa contadores de erro para a média
        total_errors_bpsk = 0
        total_errors_qpsk = 0
        
        # Assume o tamanho da mensagem original para o denominador da BER
        total_bits = len(original_binary)
        
        for _ in range(N_sim): # Múltiplas execuções para média estatística
            
            # --- Simulação BPSK ---
            t_bpsk, bpsk_signal = bpsk_modulation(binario_manchester)
            bpsk_ruido = awgn(bpsk_signal, sigma=sigma_bpsk)
            manchester_recuperado_bpsk = bpsk_demodulation(bpsk_ruido)
            binario_bpsk = manchester_decode(manchester_recuperado_bpsk)
            
            # Cálculo de Erro
            min_len_bpsk = min(total_bits, len(binario_bpsk))
            total_errors_bpsk += sum(b1 != b2 for b1, b2 in zip(original_binary[:min_len_bpsk], binario_bpsk[:min_len_bpsk]))
            
            # --- Simulação QPSK ---
            t_qpsk, qpsk_signal = qpsk_modulation(binario_manchester)
            qpsk_ruido = awgn(qpsk_signal, sigma=sigma_qpsk)
            manchester_recuperado_qpsk = qpsk_demodulation(qpsk_ruido)
            binario_qpsk = manchester_decode(manchester_recuperado_qpsk)

            # Cálculo de Erro
            min_len_qpsk = min(total_bits, len(binario_qpsk))
            total_errors_qpsk += sum(b1 != b2 for b1, b2 in zip(original_binary[:min_len_qpsk], binario_qpsk[:min_len_qpsk]))
        
        # Média de BER
        # O número de bits total é o tamanho da mensagem original * número de simulações
        ber_bpsk.append(total_errors_bpsk / (total_bits * N_sim))
        ber_qpsk.append(total_errors_qpsk / (total_bits * N_sim))

    return ebno_db_range, np.array(ber_bpsk), np.array(ber_qpsk), ebno_linear_range, t_qpsk, qpsk_signal, qpsk_ruido, t_bpsk, bpsk_signal, bpsk_ruido, binario_manchester

def plot_ondas(manchester, 
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
    
def plot_ber(ebno_db, ber_bpsk, ber_qpsk, ebno_linear):
    """Gera o gráfico de BER em função de Eb/N0 (dB)."""
    
    # Adicionando um piso para BERs zero (essencial para plotar no eixo logarítmico)
    # Se BER=0, substitui por 1e-7 para que o ponto apareça.
    ber_bpsk_plot = np.where(ber_bpsk == 0, 1e-7, ber_bpsk)
    ber_qpsk_plot = np.where(ber_qpsk == 0, 1e-7, ber_qpsk)
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(ebno_db, ber_bpsk_plot, 'ro-', label='BPSK (Simulado)')
    plt.semilogy(ebno_db, ber_qpsk_plot, 'bs-', label='QPSK (Simulado)')
    
    plt.xlabel('$E_b/N_0$ (dB)')
    plt.ylabel('Taxa de Erro de Bit (BER)')
    plt.title('BER vs $E_b/N_0$ para BPSK e QPSK em canal AWGN')
    plt.grid(True, which="both")
    plt.legend()
    
    # Ajusta limite Y para melhor visualização
    min_ber_to_plot = 1e-7
    if np.any(ber_bpsk_plot < 1):
        min_ber_to_plot = np.min(ber_bpsk_plot[ber_bpsk_plot < 1]) / 2

    plt.ylim(max(1e-7, min_ber_to_plot), 1)
    plt.show()

# ============================================================
# EXECUÇÃO
# ============================================================

option = input("Voce deseja inserir uma mensagem ou quer que o sistema gere uma aleatoria? \nDigite 'i' para inserir ou 'g' para gerar aleatoria: ")
if option == 'g':
    tamanho = int(input("Digite o tamanho da mensagem aleatoria a ser gerada (numero de caracteres): "))
    chars = string.printable  # inclui letras, números, símbolos e espaço
    texto = ''.join(random.choice(chars) for _ in range(tamanho))
    print(f"\nMensagem aleatoria gerada: {texto}")
else: 
    texto = input("Digite uma string ASCII para a transmissão: ")
    
original_binary_simulation = ascii_to_binary(texto)
    
# Definir a faixa de Eb/N0 a ser testada (em dB)
ebno_db_range = np.linspace(0, 10, 21)
    
# Da pra aumentar este valor para ter uma curva mais suave
N_simulacoes_por_ponto = 100
    
# Executar a simulação
ebno_db, ber_bpsk, ber_qpsk, ebno_linear, t_qpsk, qpsk_signal, qpsk_ruido, t_bpsk, bpsk_signal, bpsk_ruido, binario_manchester = simulate_ber_vs_ebno(
    original_binary_simulation, 
    ebno_db_range, 
    N_sim=N_simulacoes_por_ponto
)
    
print(f"\nSimulação concluída com {N_simulacoes_por_ponto} repetições por ponto.")

# Plot ondas
plot_ondas(
    binario_manchester,
    t_bpsk, bpsk_signal, bpsk_ruido,
    t_qpsk, qpsk_signal, qpsk_ruido
)
# Plotar o resultado
plot_ber(ebno_db, ber_bpsk, ber_qpsk, ebno_linear)