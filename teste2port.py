import string
from collections import Counter

# Frequências das letras em inglês
# english_frequencies = {
#     'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
#     'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
#     'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
#     'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
#     'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
#     'Z': 0.074
# }

portuguese_frequencies = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57,
    'F': 1.02, 'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40,
    'K': 0.02, 'L': 2.78, 'M': 4.74, 'N': 5.05, 'O': 10.73,
    'P': 2.52, 'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
    'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 'Y': 0.01,
    'Z': 0.47
}


def prepare_ciphertext(text):
    """Prepara o texto cifrado removendo espaços, pontuação e convertendo para maiúsculas."""
    return ''.join(char for char in text.upper() if char in string.ascii_uppercase)

def calculate_index_of_coincidence(text):
    """Calcula o Índice de Coincidência (IC) para um texto."""
    n = len(text)
    frequencies = Counter(text)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def estimate_key_length(ciphertext, max_key_length=20):
    """Estima o comprimento da chave, retornando o mais provável usando Índice de Coincidência."""
    ic_english = 0.068  # IC esperado para inglês
    ic_portuguese = 0.072
    best_key_length = 1
    min_diff = float('inf')

    for key_length in range(1, max_key_length + 1):
        # Dividir o texto em subgrupos correspondentes ao comprimento da chave
        ic_sum = 0
        for i in range(key_length):
            group = ciphertext[i::key_length]
            ic_sum += calculate_index_of_coincidence(group)
        ic_avg = ic_sum / key_length

        # Comparar com o IC esperado para encontrar o comprimento mais provável
        diff = abs(ic_avg - ic_portuguese)
        if diff < min_diff:
            min_diff = diff
            best_key_length = key_length

    return best_key_length

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
            shift = ord(key[key_index % key_length]) - ord('A')
            decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            plaintext.append(decrypted_char)
            key_index += 1
        elif char in string.ascii_lowercase:
            shift = ord(key[key_index % key_length]) - ord('A')
            decrypted_char = chr((ord(char.upper()) - shift - ord('A')) % 26 + ord('A')).lower()
            plaintext.append(decrypted_char)
            key_index += 1
        else:
            plaintext.append(char)

    return ''.join(plaintext)

def find_key(ciphertext, key_length):
    """Encontra a chave de caracteres para decifrar o texto cifrado usando análise de frequência."""
    key = []

    for i in range(key_length):
        group = ciphertext[i::key_length]
        observed_freq = calculate_letter_frequencies(group)
        min_chi_squared = float('inf')
        best_shift = None

        for shift in range(26):
            shifted_freq = {chr((ord(letter) - shift - ord('A')) % 26 + ord('A')): freq for letter, freq in observed_freq.items()}
            chi_squared = chi_squared_stat(shifted_freq, portuguese_frequencies)
            if chi_squared < min_chi_squared:
                min_chi_squared = chi_squared
                best_shift = shift

        key_char = chr(ord('A') + best_shift)
        key.append(key_char)

    return ''.join(key)

def find_repetitive_pattern(key):
    """Detecta o menor padrão repetitivo em uma chave."""
    for i in range(1, len(key) // 2 + 1):
        pattern = key[:i]
        if key == pattern * (len(key) // len(pattern)):
            return pattern
    return key


ciphertext = """tpsja kexis ttgztpb wq ssmil tfdxf vsetw ytafrttw btzf pcbroxdzo zn tqac wix, bwfd s, je ahvup sd pcbqqxff lfzed d avu ytwoxavneh sg p aznst qaghv. sfiseic f udh zgaurr dxnm rcdentv btzf nllgubsetz, wymh qfndbhqgotopl qq asmactq m prftlk huusieymi ythfdz: t tdxavict i cjs vu yts edi grzivupavnex yy pikoc wirjbko, xtw gb rvffgxa pikoc, iedp elex t gmbdr fzb sgiff bpkga; p gvgfghm t ele z xwogwko qbgmgwr adlmy bozs rtpmchv e xtme ccmo. xhmetg, hup meyqsd czgxaj o jul fsdis, eaz t tah bf iymvaxhf, mll ra roso: objqgsecl kepxqrl pgxdt sjtp emhgc v o axrfphvunh. huic zseh, ijewiet tw pjoj hzkee so kacwi pt ida dxbfp-tvict ha bsj dp tkahhf dp 1869, ge yxbya mxpm rvrclke pt qrtfffu. iwehl nre hsjspgxm t elaeks mccj, rtcse t diodiiddg, vrl lsxiszrz, isehiza nxvop rv tcxdqchfs nhrfdg v ffb eodagayaepd of cpfmftfzo ahv acnv axbkah. cezp tquvcj! vpkhmss v qfx rmd vfugx gmghrs yxq mciecthw. mrfvsnx ugt qyogbe — btbvictzm jar csnzucvr mtnhm, ifzsex i odbjtlgxq, iof czgwfpbke p mea ifzsex, ugt zvvzn yy sohupeie uwvid we gahzml asdp o znexvopzrr plxm tbxeyasep wuett ra swjcfkwa fiv pchjqgwl a mxmdp rv mtglm rcma: — “ghw, cjs f czglqrsjtpl, qqjg jeyasdtg, mod isptwj dtsid rcdirh ugt o eaenvqoo gacxgq tgkac vlagoedz t tqgrr ickibpfrvpe hq ja uod feuh pvlzl gmgottpkie fiv tpf lacfrdz t lgboeiothq. tgke lk wabpiiz, xwfpg xoetw pd qvu, ljyqaoj nfoizh sjcfkee fiv czuvqb c rzfe gabc lm nkibt tlnpkia, iiuo tlwa t o uoc vvgp s da bni xws iot t rmiiiekt ee bozs tgxuboj eymvmcvrs; enha xgjo p nq ejpcixx pajjfr lh rahgf iwnwfgs wiytha.” qcd e qbix pazgz! gea, cof mp tvdtdvnoh hmh jznex ebdzzcpl ugt zye oxmjtw. v fzb eehwd qfx gttulet t gxpijuwt hah avud wmmh; tfi llwub ele xx izrodiyaiu eoia z nrpxgtogxvqs qfuymvk ss yaxeif, hsd ad âgwupg eex tw pjjzdll ha bcto akmzrwge, xtw bpijaoh i fgcgerh gabc hupf wq gskict xmgrv dz xwbthrcfes. fpfue p tfagfvctws. hxfrmxx md jars yhzq di uek iiehcrs, pgxdt scad mvqh gvnshvmh, aznst mdbo jambrm, rojaot gab c toekmy, p tzlst, — yy awiiz ws hpzv, — e... exrtpa ganbizrwr! dljyu p dfunh pttg uicxm cjsd ect e ftftetke etbyoct. gachvnexq-et rv sluid fiv edle mcceixt, eucrr qfx rmd drrpgxm, eouenxy ypwj dz jyq pg gacxrfpg. v vpkhmss, gaoxgqj arid. gea swxo bni et qrrabwet, bro obka fiv sp wiumojsp ksxpf gewh gtpc, toyoyxho. eex h qqj csieh idp qfidt exiodeymi pgodaebgm... ja jowmiugof qfx ijewia lhw etgjeyme q firtch ezdg, eaz iedtqv qfx vqjbr ex lm fdrfs zl ixtavnehw pt ida ekestrza. p wepd ele dbq, a fiv mpgse rcevtglm p sjsl tracwda pke meoieyme-xd. rv pp, t gmqstetke pp qrml, vsy dg flshw qhhlptwse, p pfcl xrfgsrbpkxm, p hiidmi etbyoct qma dfdtt gdtf ea xbrtp sottggmd."""

ciphertext_clean = prepare_ciphertext(ciphertext)
key_length = estimate_key_length(ciphertext_clean)
initial_key = find_key(ciphertext_clean, key_length)
key = find_repetitive_pattern(initial_key)
print("Comprimento estimado da chave:", key_length)
print("Chave encontrada:", key)

# Decifrar o texto cifrado usando a chave encontrada e mantendo pontuações
plaintext = decrypt_with_key(ciphertext, key)
print("Texto decifrado:", plaintext)
