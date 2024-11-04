import string
from collections import Counter
import unicodedata

# Frequências de letras em português e inglês
portuguese_frequencies = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57,
    'F': 1.02, 'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40,
    'K': 0.02, 'L': 2.78, 'M': 4.74, 'N': 5.05, 'O': 10.73,
    'P': 2.52, 'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
    'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 'Y': 0.01,
    'Z': 0.47
}

english_frequencies = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.361, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

def prepare_ciphertext(text):
    """Prepara o texto cifrado em letras maiúsculas sem pontuações."""
    return ''.join(char for char in text.upper() if char in string.ascii_uppercase)

def calculate_index_of_coincidence(text):
    """Calcula o Índice de Coincidência (IC) para um texto."""
    n = len(text)
    frequencies = Counter(text)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def detect_language(text):
    """Detecta o idioma do texto cifrado com base no Índice de Coincidência."""
    ic = calculate_index_of_coincidence(text)
    # IC esperado para português e inglês
    ic_portuguese = 0.072
    ic_english = 0.068
    if abs(ic - ic_portuguese) < abs(ic - ic_english):
        return "portuguese", portuguese_frequencies
    else:
        return "english", english_frequencies

def estimate_key_length(ciphertext, language, max_key_length=20):
    """Estima o comprimento da chave usando Índice de Coincidência."""
    # if language == "english":
    #     ic_language =

    ic_language = 0.068 if language == "english" else 0.072

    # ic_portuguese = 0.072
    best_key_length = 1
    min_diff = float('inf')

    for key_length in range(1, max_key_length + 1):
        ic_sum = 0
        for i in range(key_length):
            group = ciphertext[i::key_length]
            ic_sum += calculate_index_of_coincidence(group)
        ic_avg = ic_sum / key_length
        diff = abs(ic_avg - ic_language)
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
    """Decifra o texto cifrado usando a chave fornecida."""
    plaintext = []
    key_length = len(key)
    key_index = 0

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

def find_key(ciphertext, key_length, frequencies):
    """Encontra a chave de caracteres para decifrar o texto cifrado."""
    key = []

    for i in range(key_length):
        group = ciphertext[i::key_length]
        observed_freq = calculate_letter_frequencies(group)
        min_chi_squared = float('inf')
        best_shift = None

        for shift in range(26):
            shifted_freq = {chr((ord(letter) - shift - ord('A')) % 26 + ord('A')): freq for letter, freq in observed_freq.items()}
            chi_squared = chi_squared_stat(shifted_freq, frequencies)
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

# Exemplo de uso
ciphertext1 = """gp, bl, ap
                hl, ap, bl
                kwh aqzr mz kbpxmti, iweouvt tmzg-xuur, amqgmzo gentrw
                xmsx m azext gsiv, aihme pawxip jngw
                q jee i spuoux dqfo, iqgl m nred ws jmtymz'
                ebrpmemzo jlk er fabuid evxt tbzq, qs mf vrzqz yeebf
                m eil, gmv lsg jrpumii ub?
                nw im'ei xgvrs wa xtm psgku
                xtm zsymax, u knr emr mf
                grw, kmf, m oia wqm vx zwj
                ha gby dmziyjrv, im jidm fmfbvrs buidm, oc fpr ambrv?
                kwh tgb lsgz nvy iesgvq qq nbv fpr juzfx fqzi
                kwh qmlr e dmoix ws e oieixmfw yia'w oieircy hmctlfme
                cac'ei fpr fqag xtqak, fpnx'e miid jriz uvrq
                nyeep ssdenvp, iah im'ei fixmzo br fpr aazyh fwtifprv
                mvq xtmei'e i qvmerv an zc fpvrsa nx kwhv btngq
                gby xmnvz ul wqkeifa nrp gby rqtydm byf euc u'u tymzqip
                gby eil aq'ty rqdrv yixi yg cedmax'e uvwfixie
                jhx im tsf jvpxa gs bil
                aq obx zwgluvt juohvql byf
                euiz qg ama uedl gs fixi
                kmf, cqa, glua vw ipnx u busgoux mjbyf
                lb cac eiymzfqz, ji imei eqgxuvt xtmei, ng glq enxqz?
                lsg xhx kwhv mzz edwhrp ur jaz glq nvveb gmym
                lsg unhq i einmy sr i pedmyiea zez'a pedmsyx lnyspgid
                gby'dm glq jrwf bumzo glmb'f ihme fqma quvr
                ha gby dmziyjrv, mty xtm pmfg ymspgw av glq enxqz?
                lsg ana ym fxmzg xa jrpumii, rwe xtm smdag xuur
                cac zepm n vqjrp an n gmzrpqaf qmv'f gmzrjgt qegouxqz
                lsg'zr xtm oieb gluvt, xtig'w qdrv nmrr yqai"""

ciphertext2 = """ne isuw qpifij wu qoh xw vam uz eegr
                yefwwk dz cvrwea
                iab zsa tz fnplsr xaemfzo
                klnrg gu vsfyflo vo ysfyo yo qms
                ke qopi iminee im damgb xmvo
                qoh tjg mpnqs ugm qopi ewu wez
                rwksv nbwks enteevs sj trvs tegaf tjsivs r gsuhjevvsk
                ajnqi g neitb i tjina
                brvw nvo uebs qpez tgksv
                cbq s fonsn jwdixiqevw
                vvmbw tjiidnv s niya, zim teh
                abrvw o qeaxg w bmife
                w g czu ppsjo ye rwljegaf
                hg iuz a tifle krrgaka
                oozej mm waalg ve xhhzs
                mm waalg ve xhhzs
                si, vi nm sa, ad av ea, si vi nm sa ac
                av, ea si vi, nm sa ad, av ea si vi nl
                sa, ad av ea, si vi nm, sa ad av ea sh
                vi, nm sa ad, av ea si, vi nm sa ad au
                ww noxe dyakem eh zgm tz dnv me ahoe
                hwkszs qi uanzmn
                rsg vvi gi xsloae gsjiihb
                tdsnj oh ekkuitb eg doigb hg viv
                sr zgue luvwwj ep lnvyg tpdb
                zgm pmo zyfvo xoz zgue heh fwe
                nzsfe fgsna rwljaya fs lwrv brpsk pmavek w cvcuswarvs
                nsfve j vrrlg e wrvws
                gnye aeg zaea dywe pjsfe
                ugm v nbwks fzlvgavaye
                ieegs wrvrvsr v vvhs, eep brq"""

ciphertext3 = """mhccs'j kkujmail' mcll ppj pty
                rss jlnmjm eomvg nzav nm'l jsdh isevjw
                mhccs'j s cttp hfd evv hwdjfxnr
                jcl owtp fx tm evv uwz
                fgw ymf yegs q btgny lgb qkc yh walns iacpy maepp
                we ldm rbwdjp cw ldm utkkgyu cgp
                gjta
                of, jsrz
                sm'wx wrggwe' vkes mae pzou
                a swswxr gq mfm gvtp
                b'm rcmzf' ow mtkd lzh kg cmy vtuesh lh jwb
                unt wzi'iw fcxm lo azcc
                jqv dhnr flbuk ppwhngf jclj dink
                tbqpbk eevixwlw xobaj' uj ptnr jcl
                sjl n whn'r vbfo dwb bm gceg swpbjk mhyy hyao
                gtn maip ap zwvi tgd bcox ea pjtw fgcgk
                xaiwexsq
                lbu a zws'm dnmh kyq
                xcy pbtf jcl a'z lfgve gy o jlkzr
                bg mw msjl zzjll
                fclfcwoa
                xh uazj riarm xehw
                'rtz nw ncs hnt mq ffsz qs maiq zbv zkzxx mouy
                w nsjvf lmaw cwxzp pjkx il evzk lixlxnepf jwwb
                dhn pse mfmn mdxl ol xs
                zf ppnl fokpbk fke htitscs zl, nmrxfbcc wk
                'uwcxx b dmy'h bfke mhp ir rskk xmymxr rsoe ldqx
                rhu rlyv eu pfgw alo risc uj axab qwikp
                njtklcdg
                rfz q ihg't iycn odg
                gnm wgev pgq q'i wtnap we s obtkf
                il xm swob ikxsq
                qsrjhmxl
                hh, ms
                kvdh gtn ltmzr kzazj pbtf xs zf ppj whophop
                eu pfgws qsobw
                e'u shm uqfocdu bmbl wyj pll
                uwz inlj xs zf wvi b'f a jthkda utkx bpljv
                ap'a yax fgcgk ceax, bm's dwondaax, kxajwm jgimyabne, th'j xaiwexsq
                zv, pwwp"""

ciphertext4 = """xcnbkw ri kqtc xcr rlqksp lr hl izoy
                m ccyyhs lc gs hub
                ebiarv mh rpob ebm aov yhsyw zopa icjm
                r dvzdil mh hl yhsyw
                ri amavv urrv lr hl lnf tmh qvznqhw
                r qvvsszanf xcr sb mfhvc ra acng tibg
                tif bhw cczab wtitwuie
                c xcr jhq fsy lr apu
                fs lc gs wmerlz ha kqn
                sb ur omifhv m zs kmssulb rl dbql
                ung kmccpa zs lvgflob
                thkb hpxb, thtb qvqfoz yhs lc aov abi
                tif rlxbwz mh blob
                aha n jlzqokm
                r ebm ri zwh zvcpc wwe jvkr
                s amavv urrv lr dlvfoy mz hl xrfkme
                sb xesjqfc hkrwaie ebm aov ln ahqf
                dyi fswieoy if bvafoz dvrha
                r blafo swhqbzn rl lvnlz dil vnc am dilzb
                jvc asniarv if owiesukvoz
                lvgmieqhvqc ha rjplrbjqng
                tif dyi dil dvjlz swuovbkw
                fs lc aov xbgzw rbniaoy uri jweojib?
                sb arw xcr hl izc!
                jpruh lr alvgwyif
                rl vruhz b alc qszmwc
                lc gs xcrfv unwz yhs acqc
                lc cflkvgv lb glc osprb
                sb mahymtc h uvboi iwki
                cfh dbql nnnlz b ebm diparf km zwt
                ab ebmec vciwy dbql lvnlz dil ava!
                kqm ebm r jlzqokm, dil bra zihrhlr
                ebm nwuln jvkr dlvfo tcvhv mz apu
                qwg yhs l drfkiqs, xcr hlu foblnrl
                yhs hqarh dbql yhsy dvjlz cfh uva"""

ciphertext = """tpsja kexis ttgztpb wq ssmil tfdxf vsetw ytafrttw btzf pcbroxdzo zn tqac wix, bwfd s, je ahvup sd pcbqqxff lfzed d avu ytwoxavneh sg p aznst qaghv. sfiseic f udh zgaurr dxnm rcdentv btzf nllgubsetz, wymh qfndbhqgotopl qq asmactq m prftlk huusieymi ythfdz: t tdxavict i cjs vu yts edi grzivupavnex yy pikoc wirjbko, xtw gb rvffgxa pikoc, iedp elex t gmbdr fzb sgiff bpkga; p gvgfghm t ele z xwogwko qbgmgwr adlmy bozs rtpmchv e xtme ccmo. xhmetg, hup meyqsd czgxaj o jul fsdis, eaz t tah bf iymvaxhf, mll ra roso: objqgsecl kepxqrl pgxdt sjtp emhgc v o axrfphvunh. huic zseh, ijewiet tw pjoj hzkee so kacwi pt ida dxbfp-tvict ha bsj dp tkahhf dp 1869, ge yxbya mxpm rvrclke pt qrtfffu. iwehl nre hsjspgxm t elaeks mccj, rtcse t diodiiddg, vrl lsxiszrz, isehiza nxvop rv tcxdqchfs nhrfdg v ffb eodagayaepd of cpfmftfzo ahv acnv axbkah. cezp tquvcj! vpkhmss v qfx rmd vfugx gmghrs yxq mciecthw. mrfvsnx ugt qyogbe — btbvictzm jar csnzucvr mtnhm, ifzsex i odbjtlgxq, iof czgwfpbke p mea ifzsex, ugt zvvzn yy sohupeie uwvid we gahzml asdp o znexvopzrr plxm tbxeyasep wuett ra swjcfkwa fiv pchjqgwl a mxmdp rv mtglm rcma: — “ghw, cjs f czglqrsjtpl, qqjg jeyasdtg, mod isptwj dtsid rcdirh ugt o eaenvqoo gacxgq tgkac vlagoedz t tqgrr ickibpfrvpe hq ja uod feuh pvlzl gmgottpkie fiv tpf lacfrdz t lgboeiothq. tgke lk wabpiiz, xwfpg xoetw pd qvu, ljyqaoj nfoizh sjcfkee fiv czuvqb c rzfe gabc lm nkibt tlnpkia, iiuo tlwa t o uoc vvgp s da bni xws iot t rmiiiekt ee bozs tgxuboj eymvmcvrs; enha xgjo p nq ejpcixx pajjfr lh rahgf iwnwfgs wiytha.” qcd e qbix pazgz! gea, cof mp tvdtdvnoh hmh jznex ebdzzcpl ugt zye oxmjtw. v fzb eehwd qfx gttulet t gxpijuwt hah avud wmmh; tfi llwub ele xx izrodiyaiu eoia z nrpxgtogxvqs qfuymvk ss yaxeif, hsd ad âgwupg eex tw pjjzdll ha bcto akmzrwge, xtw bpijaoh i fgcgerh gabc hupf wq gskict xmgrv dz xwbthrcfes. fpfue p tfagfvctws. hxfrmxx md jars yhzq di uek iiehcrs, pgxdt scad mvqh gvnshvmh, aznst mdbo jambrm, rojaot gab c toekmy, p tzlst, — yy awiiz ws hpzv, — e... exrtpa ganbizrwr! dljyu p dfunh pttg uicxm cjsd ect e ftftetke etbyoct. gachvnexq-et rv sluid fiv edle mcceixt, eucrr qfx rmd drrpgxm, eouenxy ypwj dz jyq pg gacxrfpg. v vpkhmss, gaoxgqj arid. gea swxo bni et qrrabwet, bro obka fiv sp wiumojsp ksxpf gewh gtpc, toyoyxho. eex h qqj csieh idp qfidt exiodeymi pgodaebgm... ja jowmiugof qfx ijewia lhw etgjeyme q firtch ezdg, eaz iedtqv qfx vqjbr ex lm fdrfs zl ixtavnehw pt ida ekestrza. p wepd ele dbq, a fiv mpgse rcevtglm p sjsl tracwda pke meoieyme-xd. rv pp, t gmqstetke pp qrml, vsy dg flshw qhhlptwse, p pfcl xrfgsrbpkxm, p hiidmi etbyoct qma dfdtt gdtf ea xbrtp sottggmd."""

# Remove acentos e prepara o texto cifrado
ciphertext_clean = prepare_ciphertext(ciphertext)

# Detecta o idioma e define as frequências de letras corretas
language, frequencies = detect_language(ciphertext_clean)
print(f"Idioma detectado: {language}")

# Estima o comprimento da chave e encontra a chave usando o idioma identificado
key_length = estimate_key_length(ciphertext_clean, language)
initial_key = find_key(ciphertext_clean, key_length, frequencies)
key = find_repetitive_pattern(initial_key)
# print("Comprimento estimado da chave:", key_length)
print("Chave encontrada:", key)

# Decifra o texto cifrado usando a chave encontrada
plaintext = decrypt_with_key(ciphertext, key)
print("Texto decifrado:", plaintext)
