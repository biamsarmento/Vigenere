# site para testar frases novas: https://www.cs.du.edu/~snarayan/crypt/vigenere.html

import string
from collections import Counter

# Frequências das letras em inglês
english_frequencies = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

def prepare_ciphertext(text):
    """Prepara o texto cifrado removendo espaços, pontuação e convertendo para maiúsculas."""
    return ''.join(char for char in text.upper() if char in string.ascii_uppercase)

def chi_squared_stat(observed, expected):
    """Calcula o valor do qui-quadrado para duas distribuições."""
    return sum((observed.get(letter, 0) - expected[letter]) ** 2 / expected[letter] for letter in expected)

def calculate_letter_frequencies(text):
    """Calcula a frequência relativa das letras em um texto."""
    text = [char for char in text if char in string.ascii_uppercase]
    n = len(text)
    freq = Counter(text)
    return {letter: (freq[letter] / n) * 100 for letter in string.ascii_uppercase}

def decrypt_with_key(ciphertext, key):
    """Decifra o texto cifrado usando a chave fornecida, preservando pontuações e espaços."""
    plaintext = []
    key_length = len(key)
    key_index = 0  # Índice da chave para avançar apenas em letras

    for char in ciphertext:
        if char in string.ascii_uppercase:
            # Decifra apenas letras maiúsculas
            shift = ord(key[key_index % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            plaintext.append(decrypted_char)
            key_index += 1
        elif char in string.ascii_lowercase:
            # Decifra letras minúsculas
            shift = ord(key[key_index % key_length]) - ord('A')
            decrypted_char = chr((ord(char.upper()) - shift - ord('A')) % 26 + ord('A')).lower()
            plaintext.append(decrypted_char)
            key_index += 1
        else:
            # Mantém pontuações e espaços inalterados
            plaintext.append(char)

    return ''.join(plaintext)

def find_key(ciphertext):
    """Encontra a chave de 5 caracteres para decifrar o texto cifrado usando análise de frequência."""
    key_length = 5
    ciphertext = prepare_ciphertext(ciphertext)  # Preparar o texto cifrado
    key = []

    for i in range(key_length):
        # Obter o i-ésimo grupo de caracteres (cada letra da chave cifra um grupo específico)
        group = ciphertext[i::key_length]
        
        # Calcular a frequência das letras no grupo atual
        observed_freq = calculate_letter_frequencies(group)
        
        # Testar cada possível deslocamento de 'A' a 'Z' para encontrar o melhor ajuste
        min_chi_squared = float('inf')
        best_shift = None

        for shift in range(26):
            # Ajustar frequências para o deslocamento atual
            shifted_freq = {chr((ord(letter) - shift - ord('A')) % 26 + ord('A')): freq for letter, freq in observed_freq.items()}
            
            # Calcular o qui-quadrado para este deslocamento
            chi_squared = chi_squared_stat(shifted_freq, english_frequencies)
            
            # Manter o melhor ajuste baseado no valor do qui-quadrado
            if chi_squared < min_chi_squared:
                min_chi_squared = chi_squared
                best_shift = shift

        # Determinar a letra da chave com base no melhor deslocamento
        key_char = chr(ord('A') + best_shift)
        key.append(key_char)

    return ''.join(key)

# Exemplo de uso
ciphertext = """rvgllakieg tye tirtucatzoe.  whvnvvei i winu mpsecf xronieg giid abfuk thv mfuty; wyenvvvr ik ij a drmg,
                 drzzqly eomemsei in dy jouc; wyenvvvr i wied mpsvlf znmollnkarzlp palszng seworv cfffzn narvhfusvs,
                 rnd srzngznx up khv rerr ff emeiy  flnvrac i deek; aed ejpvcirlcy wyeeevvr dy hppfs gvt jucy ae upgei 
                 haed ffmv, tyat zt ieqliies r skroeg dorrl grieczplv tf prvvvnt de wrod dvliseiatvlp stvpginx ieto khv
                 stievt, aed detyouicrlcy keotkieg geoglv's hrtj ofw--tyen, z atcolnk it yixh tzmv to xek to jer as jofn 
                 aj i tan.  khzs ij mp susskitltv foi pzstfl rnd sacl.  wzty a pyicosfpyicrl wlolrzsh tako tyrfws yidsecf 
                 lpoe hzs snoid; i huzetcy kakv tf thv syip.  khvre zs eotyieg slrgrijieg ie tyis.  zf khep blt keen it,
                 rldosk acl mvn zn tyezr dvgiee, jode tzmv or ftyer, thvrijhmerp nvarcy khe jade fvecinxs kowrrus tye 
                 fcern nity mv."""
ciphertext2 = """oi. zd fhrip nvtkvp, hnu z jpkv xgunp nchscvw. ooxnyytj zq ty yfkl. i cftl ik kflrv. cmyd mfjkedfpa sltiz. i ivyslp ichlcp jpkv dw mrzvlks ifl hnu ycymzfll."""
ciphertext3 = """jm iscuizh nieef jirmtyt sa xy daz uytt avl dopf. niie jm wedz zvnzz. c miwf niie tocjqdn. j haqy j cmo zjnutb uhut jsovfwu iz ucne. if muixm bbvq ui xruuy b wtpff rqqist. ijmi ue modk. uu ctnf xiskuoa zef, j qjlx iuwe fp qsiff mpmq nise tflf."""
ciphertext_clean = prepare_ciphertext(ciphertext)  # Preparar o texto cifrado para garantir que está no formato correto
key = find_key(ciphertext_clean)
print("Chave encontrada:", key)

# Decifrar o texto cifrado usando a chave encontrada e mantendo pontuações
plaintext = decrypt_with_key(ciphertext, key)
print("Texto decifrado:", plaintext)
