import unicodedata

def remove_acentos(texto):
    """Remove acentos de uma string em português."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def vigenere_encrypt(plaintext, key):
    """Criptografa uma string usando a cifra de Vigenère."""
    plaintext = remove_acentos(plaintext).upper()  # Mantenha em maiúsculas para a criptografia
    key = remove_acentos(key).upper()
    
    ciphertext = []
    key_length = len(key)
    key_index = 0

    for char in plaintext:
        if char.isalpha():  # Verifica se o caractere é uma letra
            shift = ord(key[key_index % key_length]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            ciphertext.append(encrypted_char)
            key_index += 1
        else:
            ciphertext.append(char)  # Mantém caracteres não alfabéticos inalterados

    return ''.join(ciphertext).lower()  # Converte o texto criptografado para minúsculas

def vigenere_decrypt(ciphertext, key):
    """Descriptografa uma string usando a cifra de Vigenère."""
    ciphertext = remove_acentos(ciphertext).upper()
    key = remove_acentos(key).upper()
    
    plaintext = []
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if char.isalpha():  # Verifica se o caractere é uma letra
            shift = ord(key[key_index % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            plaintext.append(decrypted_char)
            key_index += 1
        else:
            plaintext.append(char)  # Mantém caracteres não alfabéticos inalterados

    return ''.join(plaintext).lower()  # Converte o texto descriptografado para minúsculas

# Exemplo de uso

# texto = """Se você quiser eu vou te dar um amor
# Desses de cinema
# Não vai te faltar carinho
# Plano ou assunto ao longo do dia
# Se você quiser eu largo tudo
# Vou pro mundo com você meu bem
# Nessa nossa estrada só terá belas praias e cachoeiras
# Aonde o vento é brisa
# Onde não haja quem possa
# Com a nossa felicidade
# Vamos brindar a vida, meu bem
# Aonde o vento é brisa
# E o céu claro de estrelas
# Do que a gente precisa
# Tomar um banho de chuva
# Um banho de chuva
# Ai, ai ai ai, ai ai ai, ai ai ai ai ah
# Ai, ai ai ai, ai ai ai, ai ai ai ai ah
# Ai, ai ai ai, ai ai ai, ai ai ai ai ah
# Ai, ai ai ai, ai ai ai, ai ai ai ai ah
# Se você quiser eu vou te dar um amor
# Desses de cinema
# Não vai te faltar carinho
# Plano ou assunto ao longo do dia
# Se você quiser eu largo tudo
# Vou pro mundo com você meu bem
# Nessa nossa estrada só terá belas praias e cachoeiras
# Aonde o vento é brisa
# Onde não haja quem possa
# Com a nossa felicidade
# Vamos brindar a vida, meu bem"""
# chave = "VANESSA"

texto = """There's somethin' bout the way
The street looks when it's just rained
There's a glow off the pavement
You walk me to the car
And you know I wanna ask you to dance right there
In the middle of the parking lot
Yeah
Oh, yeah
We're drivin' down the road
I wonder if you know
I'm tryin' so hard not to get caught up now
But you're just so cool
Run your hands through your hair
Absent mindedly makin' me want you
And I don't know how it gets better than this
You take my hand and drag me head first
Fearless
And I don't know why
But with you I'd dance in a storm
In my best dress
Fearless
So baby drive slow
'Til we run out of road in this one horse town
I wanna stay right here in this passenger seat
You put your eyes on me
In this moment now capture it, remember it
'Cause I don't know how it gets better than this
You take my hand and drag me head first
Fearless
And I don't know why
But with you I'd dance in a storm
In my best dress
Fearless
Oh, oh
Well you stood there with me in the doorway
My hands shake
I'm not usually this way but
You pull me in and I'm a little more brave
It's the first kiss, it's flawless, really something, it's fearless
Oh, yeah"""
chave = "TAYLORSWIFT"

texto_sem_acentos = remove_acentos(texto)
texto_encriptado = vigenere_encrypt(texto, chave)
texto_decriptado = vigenere_decrypt(texto_encriptado, chave)

print("Texto original:", texto)
print()
print("Texto sem acentos:", texto_sem_acentos)
print()
print("Texto criptografado:", texto_encriptado)
print()
print("Texto descriptografado:", texto_decriptado)
