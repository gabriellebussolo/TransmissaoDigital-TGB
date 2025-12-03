# Simulação de Transmissão Digital

Este projeto é uma ferramenta de simulação desenvolvida em Python para demonstrar uma implementação de um sistema completo de transmissão digital, que inclui:

- Geração ou inserção de uma String em ASCII para a transmissão
- Conversão dessa String para binário
- Aplicação do codificador de canal Manchester
- Modulação por QPSK e BPSK
- Adição de ruído no canal (AWGN)
- Demodulação e decodificação dos dados recebidos

No resultado será visualizado as formas das ondas depois de cada etapa, além de um gráfico estatístico de Taxa de Erro de Bit (BER) em função da Razão Sinal-Ruído por Bit.

## Pré-requisitos

Certifique-se de ter o Python 3 instalado. Você precisará das seguintes bibliotecas científicas:

```bash
pip install numpy matplotlib scipy
```

## Execução

Execute o script principal no terminal:

```bash
python main.py
```

O programa solicitará que você escolha o modo de operação:

- `i`: para inserir uma string para ser processada
- `g`: para que o sistema gere uma string aleatória para você. Nesse caso, será requisitado o tamanho desejado da mensagem.

## Arquitetura e Funcionamento do Código

O fluxo de simulação é modularizado nas seguintes etapas:
