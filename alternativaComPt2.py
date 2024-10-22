import unicodedata
import string

# Função para remover acentuação e pontuação, além de transformar em maiúsculas
def preprocessar_texto(texto):
    texto_sem_acentos = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    # Remove pontuação e espaços, e converte tudo para maiúsculas
    texto_limpo = ''.join(c for c in texto_sem_acentos if c.isalpha()).upper()
    return texto_limpo

# Função para restaurar os espaços no texto decifrado
def restaurar_espacos(texto_original, texto_sem_espacos):
    texto_decifrado = ''
    indice = 0
    for char in texto_original:
        if char.isalpha():  # Se for uma letra, usa o texto sem espaços
            texto_decifrado += texto_sem_espacos[indice]
            indice += 1
        else:  # Se não for letra (espaço ou pontuação), mantém o original
            texto_decifrado += char
    return texto_decifrado

# Função para ajustar a senha ao tamanho da mensagem
def ajustar_senha(mensagem, senha):
    senha = senha.upper()
    senha_repetida = ''
    for i in range(len(mensagem)):
        senha_repetida += senha[i % len(senha)]
    return senha_repetida

# Função de cifrar
def cifrar_vigenere(mensagem, senha):
    mensagem_limpa = preprocessar_texto(mensagem)
    senha = ajustar_senha(mensagem_limpa, senha)
    criptograma = ''
    
    for i in range(len(mensagem_limpa)):
        valor_mensagem = ord(mensagem_limpa[i]) - ord('A')
        valor_senha = ord(senha[i]) - ord('A')
        valor_cifrado = (valor_mensagem + valor_senha) % 26
        criptograma += chr(valor_cifrado + ord('A'))
    
    return criptograma

# Função de decifrar
def decifrar_vigenere(criptograma, mensagem_original, senha):
    senha = ajustar_senha(criptograma, senha)
    mensagem_decifrada_sem_espacos = ''
    
    for i in range(len(criptograma)):
        valor_criptograma = ord(criptograma[i]) - ord('A')
        valor_senha = ord(senha[i]) - ord('A')
        valor_decifrado = (valor_criptograma - valor_senha) % 26
        mensagem_decifrada_sem_espacos += chr(valor_decifrado + ord('A'))
    
    # Restaura os espaços e pontuação na mensagem decifrada
    mensagem_decifrada = restaurar_espacos(mensagem_original, mensagem_decifrada_sem_espacos)
    
    return mensagem_decifrada

# Teste do cifrador/decifrador
mensagem = "Olá, como vai você?"
senha = "LIMAO"
criptograma = cifrar_vigenere(mensagem, senha)
print(f"Mensagem Cifrada: {criptograma}")

mensagem_decifrada = decifrar_vigenere(criptograma, mensagem, senha)
print(f"Mensagem Decifrada: {mensagem_decifrada}")


# PARTE 2 --------------------------------------------------------------------------------------------------------

import unicodedata
import string
from collections import Counter

# Reutilizando as funções preprocessar_texto e restaurar_espacos da Parte I

# Função para contar a frequência de letras em um texto
def contar_frequencia(texto):
    letras = [c for c in texto if c.isalpha()]
    frequencias = Counter(letras)
    total = sum(frequencias.values())
    frequencias_relativas = {letra: (contagem / total) * 100 for letra, contagem in frequencias.items()}
    return frequencias_relativas

# Frequência esperada de letras em português (fonte: Wikipédia)
frequencias_portugues = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57, 'F': 1.02, 
    'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40, 'K': 0.02, 'L': 2.78,
    'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 'Q': 1.20, 'R': 6.53, 
    'S': 7.81, 'T': 4.34, 'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 
    'Y': 0.01, 'Z': 0.47
}

# Função de ataque por análise de frequência
def ataque_frequencia(criptograma, frequencias_esperadas):
    # Removemos a pontuação e acentuação do criptograma
    criptograma_limpo = preprocessar_texto(criptograma)
    
    # Contamos as frequências das letras no criptograma
    frequencias_criptograma = contar_frequencia(criptograma_limpo)
    print(f"Frequências encontradas no criptograma: {frequencias_criptograma}")
    
    # Suposição de que a letra mais comum do criptograma corresponde à letra mais comum do português ('A' ou 'E')
    letra_mais_comum_criptograma = max(frequencias_criptograma, key=frequencias_criptograma.get)
    letra_mais_comum_portugues = max(frequencias_esperadas, key=frequencias_esperadas.get)
    
    # Calculamos o deslocamento assumindo que a letra mais comum do criptograma deve ser a letra mais comum do português
    deslocamento = (ord(letra_mais_comum_criptograma) - ord(letra_mais_comum_portugues)) % 26
    
    # Calculamos a possível senha assumindo que o deslocamento é uniforme
    senha = chr((ord(letra_mais_comum_criptograma) - deslocamento) % 26 + ord('A'))
    
    print(f"Possível letra da senha: {senha}")
    return senha

# Teste do ataque
mensagem_cifrada = "MHQJ NXPM TBQQZ?"  # Exemplo de criptograma
senha_recuperada = ataque_frequencia(mensagem_cifrada, frequencias_portugues)
print(f"Senha Recuperada: {senha_recuperada}")

