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
    """Decifra o texto cifrado usando a chave fornecida."""
    plaintext = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            shift = ord(key[i % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            plaintext.append(decrypted_char)
        else:
            plaintext.append(char)
    return ''.join(plaintext)

def find_key(ciphertext):
    """Encontra a chave de 5 caracteres para decifrar o texto cifrado usando análise de frequência."""
    key_length = 5
    ciphertext = ciphertext.replace(" ", "").upper()
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
ciphertext = "RVGLLAKIEGTYETIRTUCATZOEWHVNVVEIIWINUMPSECFXRONIEGGIIDABFUKTHVMFUTYWYENVVVRIKIJADRMGDRZZQLYEOMEMSEIINDYJOUCWYENVVVRIWIEDMPSVLFZNMOLLNKARZLPPALSZNGSEWORVCFFFZNNARVHFUSVSRNDSRZNGZNXUPKHVRERRFFEMEIYFLNVRACIDEEKAEDEJPVCIRLCYWYEEEVVRDYHPPFSGVTJUCYAEUPGEIHAEDFFMVTYATZTIEQLIIESRSKROEGDORRLGRIECZPLVTFPRVVVNTDEWRODDVLISEIATVLPSTVPGINXIETOKHVSTIEVTAEDDETYOUICRLCYKEOTKIEGGEOGLVSHRTJOFWTYENZATCOLNKITYIXHTZMVTOXEKTOJERASJOFNAJITANKHZSIJMPSUSSKITLTVFOIPZSTFLRNDSACLWZTYAPYICOSFPYICRLWLOLRZSHTAKOTYRFWSYIDSECFLPOEHZSSNOIDIHUZETCYKAKVTFTHVSYIPKHVREZSEOTYIEGSLRGRIJIEGIETYISZFKHEPBLTKEENITRLDOSKACLMVNZNTYEZRDVGIEEJODETZMVORFTYERTHVRIJHMERPNVARCYKHEJADEFVECINXSKOWRRUSTYEFCERNNITYMV"  # Texto cifrado de exemplo (pode substituir por um texto maior)
key = find_key(ciphertext)
print("Chave encontrada:", key)

# Decifrar o texto cifrado usando a chave encontrada
plaintext = decrypt_with_key(ciphertext, key)
print("Texto decifrado:", plaintext)
