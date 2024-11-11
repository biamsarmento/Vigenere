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

# Prepara o texto cifrado removendo espaços, pontuação e convertendo para maiúsculas.
def prepare_ciphertext(text):
    return ''.join(char for char in text.upper() if char in string.ascii_uppercase)

    # Calcula o Índice de Coincidência (IC) para um texto.
def calculate_index_of_coincidence(text):
    n = len(text)
    frequencies = Counter(text)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

# Estima o comprimento da chave, retornando o mais provável usando Índice de Coincidência.
def estimate_key_length(ciphertext, max_key_length=20):
    ic_english = 0.068  # IC esperado para inglês
    best_key_length = 1
    min_diff = float('inf')

    # Divide o texto em subgrupos correspondentes ao comprimento da chave
    for key_length in range(1, max_key_length + 1):
        ic_sum = 0
        for i in range(key_length):
            group = ciphertext[i::key_length]
            ic_sum += calculate_index_of_coincidence(group)
        ic_avg = ic_sum / key_length

        # Compara com o IC esperado para encontrar o comprimento mais provável
        diff = abs(ic_avg - ic_english)
        if diff < min_diff:
            min_diff = diff
            best_key_length = key_length

    return best_key_length

# Calcula o valor do qui-quadrado para duas distribuições.
def chi_squared_stat(observed, expected):
    return sum((observed.get(letter, 0) - expected[letter]) ** 2 / expected[letter] for letter in expected)

# Calcula a frequência relativa das letras em um texto.
def calculate_letter_frequencies(text):
    text = [char for char in text if char in string.ascii_uppercase]
    n = len(text)
    freq = Counter(text)
    return {letter: (freq[letter] / n) * 100 for letter in string.ascii_uppercase}

# Encontra a chave de caracteres para decifrar o texto cifrado usando análise de frequência.
def find_key(ciphertext, key_length):
    key = []

    for i in range(key_length):
        group = ciphertext[i::key_length]
        observed_freq = calculate_letter_frequencies(group)
        min_chi_squared = float('inf')
        best_shift = None

        for shift in range(26):
            shifted_freq = {chr((ord(letter) - shift - ord('A')) % 26 + ord('A')): freq for letter, freq in observed_freq.items()}
            chi_squared = chi_squared_stat(shifted_freq, english_frequencies)
            if chi_squared < min_chi_squared:
                min_chi_squared = chi_squared
                best_shift = shift

        key_char = chr(ord('A') + best_shift)
        key.append(key_char)

    return ''.join(key)

# Detecta o menor padrão repetitivo em uma chave. (Para evitar algo como: CUBOCUBOCUBO)
def find_repetitive_pattern(key):
    for i in range(1, len(key) // 2 + 1):
        pattern = key[:i]
        if key == pattern * (len(key) // len(pattern)):
            return pattern
    return key

# Decifra o texto cifrado usando a chave fornecida, preservando pontuações e espaços.
def decrypt_with_key(ciphertext, key):
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

# Exemplo de uso
ciphertext1 = """rvgllakieg tye tirtucatzoe.  whvnvvei i winu mpsecf xronieg giid abfuk thv mfuty; wyenvvvr ik ij a drmg,
                 drzzqly eomemsei in dy jouc; wyenvvvr i wied mpsvlf znmollnkarzlp palszng seworv cfffzn narvhfusvs,
                 rnd srzngznx up khv rerr ff emeiy  flnvrac i deek; aed ejpvcirlcy wyeeevvr dy hppfs gvt jucy ae upgei 
                 haed ffmv, tyat zt ieqliies r skroeg dorrl grieczplv tf prvvvnt de wrod dvliseiatvlp stvpginx ieto khv
                 stievt, aed detyouicrlcy keotkieg geoglv's hrtj ofw--tyen, z atcolnk it yixh tzmv to xek to jer as jofn 
                 aj i tan.  khzs ij mp susskitltv foi pzstfl rnd sacl.  wzty a pyicosfpyicrl wlolrzsh tako tyrfws yidsecf 
                 lpoe hzs snoid; i huzetcy kakv tf thv syip.  khvre zs eotyieg slrgrijieg ie tyis.  zf khep blt keen it,
                 rldosk acl mvn zn tyezr dvgiee, jode tzmv or ftyer, thvrijhmerp nvarcy khe jade fvecinxs kowrrus tye 
                 fcern nity mv."""
ciphertext2 = """dnch vv paq l yzelcc tzksr ewdx tflh z lau swd
                polosi aou xoer ggczj ae flr chvco oew lcqh ytulesu
                uur tt yxs y rvflt, rsse b cyy pv t pflbkhm
                fzzubn fta whr plbjhm
                qzav, lokp pfrs ycs kkygy hfh hycr
                yx dmyh kky ye oce, tfzixa
                ymfbxxr rsoe fy cisj uur ss rvt jtyv luas o dtn, qz
                w jxe lzhybne mskmep, t yvxp fta whrcgsi
                eiip o mxnbphkt ty
                t gvx hmh hybs gd ufg gm
                eclvh kp oew ymfzc getpf sx ajzbv
                bsjlbu urcpnv tnb wwxatq ocng lmh
                bf hnc soj mo iycn
                bn rss dbdbws fy tfp bzzhr, tb dr dppodl
                ymf gyhujo gvx tfp hybned kv wo, zlpp
                bn rss dbdbws fy tfp bzzhr, tb dr dppodl
                i iycn bm ezbet bc hwka ymf
                gf blj eobx mw ewdx
                app mfn rclrp yop th"""
ciphertext3 = """dnch vv owa f dbljpf wanay mbmc evrl e afp aik
                hcevaz mhp myym xantx ax hyo zfnal fgw lcqh ysqvyxw
                bse ww zaa f zaoqe, hywj q htg bc l dysjbtf
                aojowe zeu khk ryygfe
                owrx, lokp pfqo iwx mrwtb kgk pfkw
                hc ocel pzd tm ajw, hygqom
                rhulrsi ldis fr evpg smp pj tvt jtyv kqkm t fal, dc
                z kam shmhgyu swpbjk, b kcpd yai ntkxvcc
                zzca i axgdcehr lw
                q xxx hmh hyao qx zhn ez
                hfmyp rx tnb jcldh vjoxr zp ocgjm
                nlealo piwahj tgd jtuylo ltpg lmh
                bf gjm mtl tm vbfo
                ev yax mgorcw kn yax ngrvk, aj ud wkeyxg
                pgq amhnlb dsv ldm yabned kv vk, jfur
                il evv eeliex od evv feomm, bn kj riwwux
                b dnmh wd ykvst ue uthy qkc
                xh blj eobw ig ybfe
                ycs pgq zjtwy dzf zl"""
ciphertext4 = """cimmw, j ahg'r nedx ytwnfnumhgq
                bfhnr xlr rmv wpbrdlxw wpyk amnikhmn
                fnm g ulbgi jx'l 'vyvwx hd ni
                uxruc, hgc umfx, g xel kgemg' hl nc ldyuiuhysh
                paco m itqtiw rmvv ahsti
                bm'q mmdx g dsnebo'x ukcbxax
                wpy axysh mac syfhpt jkhk jrxs
                wpy vtl'u fxegfzx t upvw lff wtrq nslm rjqxl
                zvx magt xbfc, jx ptq uvnx
                rii phptx magok mayu m xocs hbw
                ubw payu m wbb us rhs
                cym bd j nnlr tlhpce yi tr zsnk nbvmr
                upyew wpy attf qx?
                pmvpw rmv atgr ni?
                phsmh rhs uiee kf xh zm gyvd kzwxed?
                pv exye qx mm ulx zyshxg?
                go xax ebvwxl, xsneb zsn mpvwm fc
                jj b mmmh rhs jx ptq kylm y tyffcs xablh?
                m'f hlmc 17, b wmo'x dgmx egrrimg'
                usu m dgmx m fbqt chn
                zfxmr, g lrhp uiikx gu eee ufrm ppprz
                rmvv yttpvbmc tsgz ubw ieyzmg'
                yppq mac gek lgei hy rii zrk
                j atl lpaaxpf xh uc gsngb
                j ltmc ulx vppawl, wpy dgmx xatr
                qpnl, g tep rmv htgaf abmf imf"""
ciphertext5 ="""j, z dhgu nixs vg zecn r xesbd
                qussv sbi bex v vbu nb gbp abcessr
                oou c qco'k eacx nbnh jk uyz nvuag
                cln fwoty v gvipvjfu, c esbccmse
                nbrffmye mpl ab, hirn'f kivlr w'mc zbzmfq
                accfxl'g qiizwtvx gcnflecx
                ji v'ab ciis zfo rjfis awhyn ywlv cg'g uyy yotk hvuik
                fvyf zn'f hiv fngu ectvu
                zz gvf nieze nuf soucau
                j'u qnbor vr bfon gc zfo
                vt uyy cosks jot fprf
                bex bis kczs pe ynfuy qng uylbihy
                cq kbehn vpcx lcv aofh gfl n kizfr
                oou xvs xznu o tdcys
                jw nus xflyr xrm rbezht
                w'e nuabb sy asyk nb mpl"""

ciphertext_clean = prepare_ciphertext(ciphertext1)
key_length = estimate_key_length(ciphertext_clean)
initial_key = find_key(ciphertext_clean, key_length)
key = find_repetitive_pattern(initial_key)
print("Chave encontrada:", key)

# Decifra o texto cifrado usando a chave encontrada e mantendo pontuações
plaintext = decrypt_with_key(ciphertext1, key)
print("Texto decifrado:", plaintext)
