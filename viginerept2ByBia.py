import string
from collections import Counter

# Frequências aproximadas de letras em inglês (fonte: Wikipédia)
english_letter_freq = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

# Função para formatar o texto criptografado
def format_ciphertext(text):
    # Remove tudo que não for letra e converte para maiúsculas
    return ''.join([c for c in text.upper() if c in string.ascii_uppercase])

# Função para calcular o índice de coincidência
def index_of_coincidence(text):
    freq = Counter(text)
    N = len(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))
    return ic

# Estimativa do comprimento da senha
def estimate_key_length(ciphertext, max_len=20):
    avg_ic = []
    for key_len in range(1, max_len + 1):
        ic_values = [
            index_of_coincidence(ciphertext[i::key_len]) for i in range(key_len)
        ]
        avg_ic.append((key_len, sum(ic_values) / key_len))
    likely_key_len = max(avg_ic, key=lambda x: x[1])[0]
    return likely_key_len

# Frequência em cada grupo e tentativa de dedução da senha
def find_key(ciphertext, key_len):
    key = ""
    for i in range(key_len):
        segment = ciphertext[i::key_len]
        frequencies = Counter(segment)
        most_common_char, _ = frequencies.most_common(1)[0]
        
        shift = (ord(most_common_char) - ord('E')) % 26
        key += chr(shift + ord('A'))
    return key

# Decifragem com a senha
def decrypt_vigenere(ciphertext, key):
    plaintext = []
    key_len = len(key)
    for i, char in enumerate(ciphertext):
        if char in string.ascii_uppercase:
            shift = (ord(char) - ord(key[i % key_len])) % 26
            plaintext.append(chr(shift + ord('A')))
        else:
            plaintext.append(char)
    return ''.join(plaintext)

# Exemplo de uso
# ciphertext = "Texto criptografado com caracteres extras 123!"
ciphertext1 = "rvgllakieg tye tirtucatzoe.  whvnvvei i winu mpsecf xronieg giid abfuk thv mfuty; wyenvvvr ik ij a drmg, drzzqly eomemsei in dy jouc; wyenvvvr i wied mpsvlf znmollnkarzlp palszng seworv cfffzn narvhfusvs, rnd srzngznx up khv rerr ff emeiy flnvrac i deek; aed ejpvcirlcy wyeeevvr dy hppfs gvt jucy ae upgei haed ff mv, tyat zt ieqliies r skroeg dorrl grieczplv tf prvvvnt de wrod dvliseiatvlp stvpginx ieto khv stievt, aed detyouicrlcy keotkieg geoglv's hrtj ofw--tyen, z atcolnk it yixh tzmv to xek to jer as jofn aj i tan.  khzs ij mp susskitltv foi pzstfl rnd sacl.  wzty a pyicosfpyicrl wlolrzsh tako tyrfws yidsecf lpoe hzs snoid; i huzetcy kakv tf thv syip.  khvre zs eotyieg slrgrijieg ie tyis.  zf khep blt keen it, rldosk acl mvn zn tyezr dvgiee, jode tzmv or ftyer, thvrijh merp nvarcy khe jade fvecinxs kowrrus tye fcern nity mv."
ciphertext2 = "tpsja kexis ttgztpb wq ssmil tfdxf vsetw ytafrttw btzf pcbroxdzo zn tqac wix, bwfd s, je ahvup sd pcbqqxff lfzed d avu ytwoxavneh sg p aznst qaghv. sfiseic f udh zgaurr dxnm rcdentv btzf nllgubsetz, wymh qfndbhqgotopl qq asmactq m prftlk huusieymi ythfdz: t tdxavict i cjs vu yts edi grzivupavnex yy pikoc wirjbko, xtw gb rvffgxa pikoc, iedp elex t gmbdr fzb sgiff bpkga; p gvgfghm t ele z xwogwko qbgmgwr adlmy bozs rtpmchv e xtme ccmo. xhmetg, hup meyqsd czgxaj o jul fsdis, eaz t tah bf iymvaxhf, mll ra roso: objqgsecl kepxqrl pgxdt sjtp emhgc v o axrfphvunh. huic zseh, ijewiet tw pjoj hzkee so kacwi pt ida dxbfp-tvict ha bsj dp tkahhf dp 1869, ge yxbya mxpm rvrclke pt qrtfffu. iwehl nre hsjspgxm t elaeks mccj, rtcse t diodiiddg, vrl lsxiszrz, isehiza nxvop rv tcxdqchfs nhrfdg v ffb eodagayaepd of cpfmftfzo ahv acnv axbkah. cezp tquvcj! vpkhmss v qfx rmd vfugx gmghrs yxq mciecthw. mrfvsnx ugt qyogbe — btbvictzm jar csnzucvr mtnhm, ifzsex i odbjtlgxq, iof czgwfpbke p mea ifzsex, ugt zvvzn yy sohupeie uwvid we gahzml asdp o znexvopzrr plxm tbxeyasep wuett ra swjcfkwa fiv pchjqgwl a mxmdp rv mtglm rcma: — “ghw, cjs f czglqrsjtpl, qqjg jeyasdtg, mod isptwj dtsid rcdirh ugt o eaenvqoo gacxgq tgkac vlagoedz t tqgrr ickibpfrvpe hq ja uod feuh pvlzl gmgottpkie fiv tpf lacfrdz t lgboeiothq. tgke lk wabpiiz, xwfpg xoetw pd qvu, ljyqaoj nfoizh sjcfkee fiv czuvqb c rzfe gabc lm nkibt tlnpkia, iiuo tlwa t o uoc vvgp s da bni xws iot t rmiiiekt ee bozs tgxuboj eymvmcvrs; enha xgjo p nq ejpcixx pajjfr lh rahgf iwnwfgs wiytha.” qcd e qbix pazgz! gea, cof mp tvdtdvnoh hmh jznex ebdzzcpl ugt zye oxmjtw. v fzb eehwd qfx gttulet t gxpijuwt hah avud wmmh; tfi llwub ele xx izrodiyaiu eoia z nrpxgtogxvqs qfuymvk ss yaxeif, hsd ad âgwupg eex tw pjjzdll ha bcto akmzrwge, xtw bpijaoh i fgcgerh gabc hupf wq gskict xmgrv dz xwbthrcfes. fpfue p tfagfvctws. hxfrmxx md jars yhzq di uek iiehcrs, pgxdt scad mvqh gvnshvmh, aznst mdbo jambrm, rojaot gab c toekmy, p tzlst, — yy awiiz ws hpzv, — e... exrtpa ganbizrwr! dljyu p dfunh pttg uicxm cjsd ect e ftftetke etbyoct. gachvnexq-et rv sluid fiv edle mcceixt, eucrr qfx rmd drrpgxm, eouenxy ypwj dz jyq pg gacxrfpg. v vpkhmss, gaoxgqj arid. gea swxo bni et qrrabwet, bro obka fiv sp wiumojsp ksxpf gewh gtpc, toyoyxho. eex h qqj csieh idp qfidt exiodeymi pgodaebgm... ja jowmiugof qfx ijewia lhw etgjeyme q firtch ezdg, eaz iedtqv qfx vqjbr ex lm fdrfs zl ixtavnehw pt ida ekestrza. p wepd ele dbq, a fiv mpgse rcevtglm p sjsl tracwda pke meoieyme-xd. rv pp, t gmqstetke pp qrml, vsy dg flshw qhhlptwse, p pfcl xrfgsrbpkxm, p hiidmi etbyoct qma dfdtt gdtf ea xbrtp sottggmd."
ciphertext = format_ciphertext(ciphertext1)  # Formata o texto
print(f"Formatted ciphertext: {ciphertext}")

key_len = estimate_key_length(ciphertext)
print(f"Estimated key length: {key_len}")

recovered_key = find_key(ciphertext, key_len)
print(f"Recovered key: {recovered_key}")

plaintext = decrypt_vigenere(ciphertext, recovered_key)
print(f"Decrypted message: {plaintext}")
