from collections import Counter
import string

# Função para cifrar e decifrar
def cifra_vigenere(texto, chave, modo="cifrar"):
    resultado = []
    chave = chave.upper()  # Converte a chave para maiúsculas
    
    for i, caractere in enumerate(texto.upper()):
        if caractere in string.ascii_uppercase:  # Ignora caracteres que não sejam letras
            deslocamento = ord(chave[i % len(chave)]) - ord('A')  # Calcula o deslocamento com base na chave
            if modo == "cifrar":  # Cifra o caractere
                resultado.append(chr((ord(caractere) - ord('A') + deslocamento) % 26 + ord('A')))
            else:  # Decifra o caractere
                resultado.append(chr((ord(caractere) - ord('A') - deslocamento) % 26 + ord('A')))
        else:
            resultado.append(caractere)  # Mantém o caractere original, caso não seja letra
    
    return ''.join(resultado)  # Retorna o texto cifrado ou decifrado

# Função para estimar o tamanho da chave com base em repetições de trigrama (Kasiski Examination)
def descobrir_tamanho_chave(texto):
    # Remove caracteres não-letras e coloca em maiúsculas para análise
    texto = ''.join([c for c in texto.upper() if c in string.ascii_uppercase])
    
    # Identifica as distâncias entre trigramas repetidos
    distancias = [j - i for i in range(len(texto) - 3) for j in range(i + 3, len(texto) - 2)
                  if texto[i:i + 3] == texto[j:j + 3]]
    
    # Encontra fatores comuns entre as distâncias
    fatores = [f for d in distancias for f in range(2, d + 1) if d % f == 0]
    
    # Retorna o fator mais comum como a estimativa do tamanho da chave
    return Counter(fatores).most_common(1)[0][0]

# Função para estimar a chave com base na análise de frequência
def estimar_chave(texto, tamanho_chave):
    # Remove caracteres não-letras e coloca em maiúsculas
    texto = ''.join([c for c in texto.upper() if c in string.ascii_uppercase])
    chave = []
    
    # Para cada posição da chave, encontra a letra mais comum
    for i in range(tamanho_chave):
        subtexto = texto[i::tamanho_chave]  # Divide o texto em blocos usando o tamanho estimado da chave
        frequencias = Counter(subtexto)  # Conta a frequência de cada letra no bloco
        letra_comum = frequencias.most_common(1)[0][0]  # Identifica a letra mais comum no bloco
        # Calcula a letra da chave assumindo que a letra mais comum é 'E'
        chave.append(chr((ord(letra_comum) - ord('E') + 26) % 26 + ord('A')))
    
    return ''.join(chave)  # Retorna a chave estimada como uma string

# Função para decifrar o conteúdo de um arquivo usando a cifra de Vigenère
def decifrar_arquivo(nome_arquivo):
    # Lê o conteúdo do arquivo com a codificação UTF-8
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read()
    
    # Estima o tamanho da chave e a própria chave
    tamanho_chave = descobrir_tamanho_chave(texto)
    chave = estimar_chave(texto, tamanho_chave)
    
    # Decifra o texto usando a chave estimada
    return cifra_vigenere(texto, chave, modo="decifrar"), chave

# Processa os arquivos .txt
for i in range(1, 3):
    nome_arquivo = f"desafio{i}.txt"
    texto_decifrado, chave = decifrar_arquivo(nome_arquivo)
    print(f"Decifragem do arquivo {nome_arquivo} com chave estimada '{chave}':\n{texto_decifrado}")
    print("\n" + "-"*50 + "\n")
