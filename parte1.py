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

# texto = """There's somethin' bout the way
# The street looks when it's just rained
# There's a glow off the pavement
# You walk me to the car
# And you know I wanna ask you to dance right there
# In the middle of the parking lot
# Yeah
# Oh, yeah
# We're drivin' down the road
# I wonder if you know
# I'm tryin' so hard not to get caught up now
# But you're just so cool
# Run your hands through your hair
# Absent mindedly makin' me want you
# And I don't know how it gets better than this
# You take my hand and drag me head first
# Fearless
# And I don't know why
# But with you I'd dance in a storm
# In my best dress
# Fearless
# So baby drive slow
# 'Til we run out of road in this one horse town
# I wanna stay right here in this passenger seat
# You put your eyes on me
# In this moment now capture it, remember it
# 'Cause I don't know how it gets better than this
# You take my hand and drag me head first
# Fearless
# And I don't know why
# But with you I'd dance in a storm
# In my best dress
# Fearless
# Oh, oh
# Well you stood there with me in the doorway
# My hands shake
# I'm not usually this way but
# You pull me in and I'm a little more brave
# It's the first kiss, it's flawless, really something, it's fearless
# Oh, yeah"""
# chave = "TAYLORSWIFT"

texto= """Forgive me Peter
My lost fearless leader
In closets like cedar
Preserved from when we were just kids
Is it something I did
The goddess of timing
Once found us beguiling
She said she was trying
Peter was she lying
My ribs get the feeling she did
And I didn't want to come down
I thought it was just goodbye for now
You said you were gonna grow up
Then you were gonna come find me
You said you were gonna grow up
Then you were gonna come find me
Said you were gonna grow up
Then you were gonna come find me
Words from the mouths of babes
promises, oceans deep
But never to keep
Oh, never to keep
Are you still a mind reader?
A natural scene stealer
I've heard great things Peter
But life was always easier on you
Than it was on me
And sometimes it gets me
When crossing your jet stream
We both did the best we could do underneath the same moon
In different galaxies
And I didn't want to hang around
We said it was just goodbye for now
You said you were gonna grow up
Then you were gonna come find me
You said you were gonna grow up
Then you were gonna come find me
Said you were gonna grow up
Then you were gonna come find me
Words from the mouths of babes
promises, oceans deep
But never to keep
Oh, never to keep"""
chave = "PETER"

# texto = """Quando eu digo que deixei de te amar
# É porque eu te amo
# Quando eu digo que não quero mais você
# É porque eu te quero
# Eu tenho medo de te dar meu coração
# E confessar que eu estou em tuas mãos
# Mas não posso imaginar
# O que vai ser de mim
# Se eu te perder um dia
# Eu me afasto e me defendo de você
# Mas depois me entrego
# Faço tipo, falo coisas que eu não sou
# Mas depois eu nego
# Mas a verdade
# É que eu sou louco por você
# E tenho medo de pensar em te perder
# Eu preciso aceitar que não dá mais
# Pra separar as nossas vidas
# E nessa loucura de dizer que não te quero
# Vou negando as aparências
# Disfarçando as evidências
# Mas pra que viver fingindo
# Se eu não posso enganar meu coração?
# Eu sei que te amo!
# Chega de mentiras
# De negar o meu desejo
# Eu te quero mais que tudo
# Eu preciso do seu beijo
# Eu entrego a minha vida
# Pra você fazer o que quiser de mim
# Só quero ouvir você dizer que sim!
# Diz que é verdade, que tem saudade
# Que ainda você pensa muito em mim
# Diz que é verdade, que tem saudade
# Que ainda você quer viver pra mim"""
# chave = "HINO"

# texto = """Uh, oh, oh
# Uh, oh, oh
# You were in college, working part-time, waiting tables
# Left a small town, never looked back
# I was a flight risk, with a fear of fallin'
# Wondering why we bother with love, if it never lasts
# I say, can you believe it?
# As we're lying on the couch
# The moment, I can see it
# Yes, yes, I can see it now
# Do you remember, we were sitting there, by the water?
# You put your arm around me for the first time
# You made a rebel of a careless man's careful daughter
# You're the best thing, that's ever been mine
# Flash forward, and we're taking on the world together
# And there's a drawer of my things at your place
# You learn my secrets and you figure out why I'm guarded
# You say we'll never make my parent's mistakes
# But we got bills to pay
# We got nothing figured out
# When it was hard to take
# Yes, yes, this is what I thought about
# Do you remember, we were sitting there, by the water?
# You put your arm around me for the first time
# You made a rebel of a careless man's careful daughter
# You're the best thing that's ever been mine
# Do you remember, all the city lights on the water?
# You saw me start to believe, for the first time
# You made a rebel of a careless man's careful daughter
# You're the best thing, that's ever been mine"""
# chave = "MINE"

texto_sem_acentos = remove_acentos(texto)
texto_encriptado = vigenere_encrypt(texto_sem_acentos, chave)
texto_decriptado = vigenere_decrypt(texto_encriptado, chave)

print("Texto original:", texto)
print()
print("Texto sem acentos:", texto_sem_acentos)
print()
print("Texto criptografado:", texto_encriptado)
print()
print("Texto descriptografado:", texto_decriptado)
