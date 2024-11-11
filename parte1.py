import unicodedata

# Remove os acentos
def remove_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Criptografa uma string usando a cifra de Vigenère.
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper()  # Transforma o texto para maiúsculas
    key = key.upper()
    
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

# Descriptografa uma string usando a cifra de Vigenère.
def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    
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

# Exemplo em inglês

# text = """I hopped off the plane at LAX
# With a dream and my cardigan
# Welcome to the land of fame excess (woah)
# Am I gonna fit in?
# Jumped in the cab, here I am for the first time
# Look to my right, and I see the Hollywood sign
# This is all so crazy
# Everybody seems so famous
# My tummy's turnin' and I'm feelin' kinda homesick
# Too much pressure and I'm nervous
# That's when the taxi man turned on the radio
# And a Jay-Z song was on
# And a Jay-Z song was on
# And a Jay-Z song was on
# So I put my hands up
# They're playin' my song, the butterflies fly away
# I'm noddin' my head like, yeah
# Movin' my hips like, yeah
# I got my hands up, they're playin' my song
# They know I'm gonna be okay
# Yeah, it's a party in the U.S.A.
# Yeah, it's a party in the U.S.A.
# Get to the club in my taxi cab
# Everybody's looking at me now
# Like, "Who's that chick that's rockin' kicks?
# She gotta be from out of town"
# So hard with my girls not around me
# It's definitely not a Nashville party
# 'Cause all I see are stilettos
# I guess I never got the memo"""
# key ="MILEY"

# Exemplo em português

text = """Quanto a mim, lá estava, solitário e deslembrado, a namorar
certa compota da minha paixão. No fim de cada glosa ficava
muito contente, esperando que fosse a última, mas não era, e
a sobremesa continuava intata. Ninguém se lembrava de dar a
primeira voz. Meu pai, à cabeceira, saboreava a goles extensos
a alegria dos convivas, mirava-se todo nos carões alegres, nos
pratos, nas flores, deliciava- se com a familiaridade travada
entre os mais distantes espíritos, influxo de um bom jantar.
Eu via isso, porque arrastava os olhos da compota para ele e
dele para a compota, como a pedir-lhe que ma servisse; mas
fazia-o em vão. Ele não via nada; via-se a si mesmo. E as glosas
sucediam-se, como bátegas d’água, obrigando-me a recolher
o desejo e o pedido. Pacientei quanto pude; e não pude muito.
Pedi em voz baixa o doce; enfim, bradei, berrei, bati com os
pés. Meu pai, que seria capaz de me dar o sol, se eu lho exigisse,
chamou um escravo para me servir o doce; mas era tarde. A tia
Emerenciana arrancara-me da cadeira e entregara-me a uma
escrava, não obstante os meus gritos e repelões."""
key = "CUBAS"

texto_sem_acentos = remove_acentos(text)
texto_encriptado = vigenere_encrypt(texto_sem_acentos, key)
texto_decriptado = vigenere_decrypt(texto_encriptado, key)

print("Texto original:", text)
print()
print("Chave:", key)
print()
print("Texto criptografado:", texto_encriptado)
print()
print("Texto descriptografado:", texto_decriptado)
