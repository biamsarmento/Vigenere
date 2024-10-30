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

def calculate_index_of_coincidence(text):
    """Calcula o Índice de Coincidência (IC) para um texto."""
    n = len(text)
    frequencies = Counter(text)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def estimate_key_length(ciphertext, max_key_length=20):
    """Estima o comprimento da chave, retornando o mais provável usando Índice de Coincidência."""
    ic_english = 0.068  # IC esperado para inglês
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
        diff = abs(ic_avg - ic_english)
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
            chi_squared = chi_squared_stat(shifted_freq, english_frequencies)
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
ciphertext5 = """tpsja kexis ttgztpb wq ssmil tfdxf vsetw ytafrttw btzf pcbroxdzo zn tqac wix, bwfd s, je ahvup sd pcbqqxff lfzed d avu ytwoxavneh sg p aznst qaghv. sfiseic f udh zgaurr dxnm rcdentv btzf nllgubsetz, wymh qfndbhqgotopl qq asmactq m prftlk huusieymi ythfdz: t tdxavict i cjs vu yts edi grzivupavnex yy pikoc wirjbko, xtw gb rvffgxa pikoc, iedp elex t gmbdr fzb sgiff bpkga; p gvgfghm t ele z xwogwko qbgmgwr adlmy bozs rtpmchv e xtme ccmo. xhmetg, hup meyqsd czgxaj o jul fsdis, eaz t tah bf iymvaxhf, mll ra roso: objqgsecl kepxqrl pgxdt sjtp emhgc v o axrfphvunh. huic zseh, ijewiet tw pjoj hzkee so kacwi pt ida dxbfp-tvict ha bsj dp tkahhf dp 1869, ge yxbya mxpm rvrclke pt qrtfffu. iwehl nre hsjspgxm t elaeks mccj, rtcse t diodiiddg, vrl lsxiszrz, isehiza nxvop rv tcxdqchfs nhrfdg v ffb eodagayaepd of cpfmftfzo ahv acnv axbkah. cezp tquvcj! vpkhmss v qfx rmd vfugx gmghrs yxq mciecthw. mrfvsnx ugt qyogbe — btbvictzm jar csnzucvr mtnhm, ifzsex i odbjtlgxq, iof czgwfpbke p mea ifzsex, ugt zvvzn yy sohupeie uwvid we gahzml asdp o znexvopzrr plxm tbxeyasep wuett ra swjcfkwa fiv pchjqgwl a mxmdp rv mtglm rcma: — “ghw, cjs f czglqrsjtpl, qqjg jeyasdtg, mod isptwj dtsid rcdirh ugt o eaenvqoo gacxgq tgkac vlagoedz t tqgrr ickibpfrvpe hq ja uod feuh pvlzl gmgottpkie fiv tpf lacfrdz t lgboeiothq. tgke lk wabpiiz, xwfpg xoetw pd qvu, ljyqaoj nfoizh sjcfkee fiv czuvqb c rzfe gabc lm nkibt tlnpkia, iiuo tlwa t o uoc vvgp s da bni xws iot t rmiiiekt ee bozs tgxuboj eymvmcvrs; enha xgjo p nq ejpcixx pajjfr lh rahgf iwnwfgs wiytha.” qcd e qbix pazgz! gea, cof mp tvdtdvnoh hmh jznex ebdzzcpl ugt zye oxmjtw. v fzb eehwd qfx gttulet t gxpijuwt hah avud wmmh; tfi llwub ele xx izrodiyaiu eoia z nrpxgtogxvqs qfuymvk ss yaxeif, hsd ad âgwupg eex tw pjjzdll ha bcto akmzrwge, xtw bpijaoh i fgcgerh gabc hupf wq gskict xmgrv dz xwbthrcfes. fpfue p tfagfvctws. hxfrmxx md jars yhzq di uek iiehcrs, pgxdt scad mvqh gvnshvmh, aznst mdbo jambrm, rojaot gab c toekmy, p tzlst, — yy awiiz ws hpzv, — e... exrtpa ganbizrwr! dljyu p dfunh pttg uicxm cjsd ect e ftftetke etbyoct. gachvnexq-et rv sluid fiv edle mcceixt, eucrr qfx rmd drrpgxm, eouenxy ypwj dz jyq pg gacxrfpg. v vpkhmss, gaoxgqj arid. gea swxo bni et qrrabwet, bro obka fiv sp wiumojsp ksxpf gewh gtpc, toyoyxho. eex h qqj csieh idp qfidt exiodeymi pgodaebgm... ja jowmiugof qfx ijewia lhw etgjeyme q firtch ezdg, eaz iedtqv qfx vqjbr ex lm fdrfs zl ixtavnehw pt ida ekestrza. p wepd ele dbq, a fiv mpgse rcevtglm p sjsl tracwda pke meoieyme-xd. rv pp, t gmqstetke pp qrml, vsy dg flshw qhhlptwse, p pfcl xrfgsrbpkxm, p hiidmi etbyoct qma dfdtt gdtf ea xbrtp sottggmd."""
ciphertext6 ="""j, z dhgu nixs vg zecn r xesbd
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
ciphertext7 = """yleip'w kgritytr' tgzx typ asq
yle jevwwy pofvw ozjr ik'd nmky vazyiv
lmirv'd e ydta owq xzw uevvxifl
dsu nlpc ej xo ksi usw
enu jsm cssw z hefff esb jsm lt haeni jallt ksijw
nr typ qavipe fq xzw uerbtry dtx
yvll
gz, diay
hi'jw ivimtr' vgbr typ vgsi
m wfyhwj nj yff ofgb
m'm kccaf' xs hrch fgy xo xpx uszkhk ft fgb
fuk jsm'jj nuje wg utsl
ifr qgzv hryhk lmvolrl qgzv hrtv
stxink xmfvjhlp xecas' qe nlrl qty
aeo m vgs'x keza zgb mt xpxk tjxtvc xzss xhzd
cgm yekv xc zssh aeo hjsl qe ypev xnvsk
qisjqisj
lrv a isn'k vrgo bly
sfx oayl yff m'v vfrcv tr s kysrd
tr eq gisk ovwkx
jercpwkx
wo slfq vwmvv dpgo
'yml np vmf tyt fq vgsi mn ksmk gsi hfcww ltan
z hefff wtrj vaymx hvci af ylij aekkjrgvc wwsy
col ayl qtyr vjik gs qe
zy xzax qodprl fta craxmjj mt, ipqwegir ze
'gsmxi i uzr'l cssw yza al litj milljv tylr lznw
yff xscj qy ylrv ssh dilk ew miau qmjky
jercpwkx
enu t hgf'y onfh azq
gyt ntxz qty i'u oefuj mn r dxgjr
mn dj fwky hrvdw
xwfvlvdw
gz, tl
wvwp qgz wtfzh lzjve ntxz ej mn ksi vgtvwrj
qq zfrdj dlscj
m'm ezx mkzelcj xzax aap myl
qty plwp ew nr aeo m'e s qmtkwi egwi bilzw
ay'w typ jajxx kzdw, al'x jlrhpwkx, verwpq ktqeksmfy, nx's wpejdjws
fs, cwsm"""

ciphertext = """mhccs'j kkujmail' mcll ppj pty
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

ciphertext_clean = prepare_ciphertext(ciphertext)
key_length = estimate_key_length(ciphertext_clean)
initial_key = find_key(ciphertext_clean, key_length)
key = find_repetitive_pattern(initial_key)
print("Comprimento estimado da chave:", key_length)
print("Chave encontrada:", key)

# Decifrar o texto cifrado usando a chave encontrada e mantendo pontuações
plaintext = decrypt_with_key(ciphertext, key)
print("Texto decifrado:", plaintext)
