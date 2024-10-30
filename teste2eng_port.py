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

# Frequências das letras em português
portuguese_frequencies = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57,
    'F': 1.02, 'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40,
    'K': 0.02, 'L': 2.78, 'M': 4.74, 'N': 5.05, 'O': 10.73,
    'P': 2.52, 'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
    'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 'Y': 0.01,
    'Z': 0.47
}

def prepare_ciphertext(text):
    return ''.join(char for char in text.upper() if char in string.ascii_uppercase)

def calculate_index_of_coincidence(text):
    n = len(text)
    frequencies = Counter(text)
    ic = sum(f * (f - 1) for f in frequencies.values()) / (n * (n - 1)) if n > 1 else 0
    return ic

def estimate_key_length(ciphertext, max_key_length=20):
    ic_portuguese = 0.072
    ic_english = 0.068 
    best_key_length = 1
    min_diff = float('inf')

    for key_length in range(1, max_key_length + 1):
        ic_sum = 0
        for i in range(key_length):
            group = ciphertext[i::key_length]
            ic_sum += calculate_index_of_coincidence(group)
        ic_avg = ic_sum / key_length

        # Calcular a diferença em relação ao IC de ambas as línguas
        diff_portuguese = abs(ic_avg - ic_portuguese)
        diff_english = abs(ic_avg - ic_english)

        # Usar o menor valor de diferença como critério
        diff = min(diff_portuguese, diff_english)
        
        if diff < min_diff:
            min_diff = diff
            best_key_length = key_length

    return best_key_length


def chi_squared_stat(observed, expected):
    return sum((observed.get(letter, 0) - expected[letter]) ** 2 / expected[letter] for letter in expected)

def calculate_letter_frequencies(text):
    text = [char for char in text if char in string.ascii_uppercase]
    n = len(text)
    freq = Counter(text)
    return {letter: (freq[letter] / n) * 100 for letter in string.ascii_uppercase}

def estimate_language(observed_freq):
    chi_squared_portuguese = chi_squared_stat(observed_freq, portuguese_frequencies)
    chi_squared_english = chi_squared_stat(observed_freq, english_frequencies)
    
    return 'portuguese' if chi_squared_portuguese < chi_squared_english else 'english'

def decrypt_with_key(ciphertext, key):
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

def find_key(ciphertext, key_length):
    key = []

    for i in range(key_length):
        group = ciphertext[i::key_length]
        observed_freq = calculate_letter_frequencies(group)
        language = estimate_language(observed_freq)
        target_frequencies = portuguese_frequencies if language == 'portuguese' else english_frequencies

        min_chi_squared = float('inf')
        best_shift = None

        for shift in range(26):
            shifted_freq = {chr((ord(letter) - shift - ord('A')) % 26 + ord('A')): freq for letter, freq in observed_freq.items()}
            chi_squared = chi_squared_stat(shifted_freq, target_frequencies)
            if chi_squared < min_chi_squared:
                min_chi_squared = chi_squared
                best_shift = shift

        key_char = chr(ord('A') + best_shift)
        key.append(key_char)

    return ''.join(key)

def find_repetitive_pattern(key):
    for i in range(1, len(key) // 2 + 1):
        pattern = key[:i]
        if key == pattern * (len(key) // len(pattern)):
            return pattern
    return key

# Exemplo de uso:
# coloque o texto criotografado em ciphertext

# desafio 1
ciphertext1 = """rvgllakieg tye tirtucatzoe.  whvnvvei i winu mpsecf xronieg giid abfuk thv mfuty; wyenvvvr ik ij a drmg, drzzqly eomemsei in dy jouc; wyenvvvr i wied mpsvlf znmollnkarzlp palszng seworv cfffzn narvhfusvs, rnd srzngznx up khv rerr ff emeiy  flnvrac i deek; aed ejpvcirlcy wyeeevvr dy hppfs gvt jucy ae upgei haed ff mv, tyat zt ieqliies r skroeg dorrl grieczplv tf prvvvnt de wrod dvliseiatvlp stvpginx ieto khv stievt, aed detyouicrlcy keotkieg geoglv's hrtj ofw--tyen, z atcolnk it yixh tzmv to xek to jer as jofn aj i tan.  khzs ij mp susskitltv foi pzstfl rnd sacl.  wzty a pyicosfpyicrl wlolrzsh tako tyrfws yidsecf lpoe hzs snoid; i huzetcy kakv tf thv syip.  khvre zs eotyieg slrgrijieg ie tyis.  zf khep blt keen it, rldosk acl mvn zn tyezr dvgiee, jode tzmv or ftyer, thvrijhmerp nvarcy khe jade fvecinxs kowrrus tye fcern nity mv."""
# desafio 2
ciphertext2 = """tpsja kexis ttgztpb wq ssmil tfdxf vsetw ytafrttw btzf pcbroxdzo zn tqac wix, bwfd s, je ahvup sd pcbqqxff lfzed d avu ytwoxavneh sg p aznst qaghv. sfiseic f udh zgaurr dxnm rcdentv btzf nllgubsetz, wymh qfndbhqgotopl qq asmactq m prftlk huusieymi ythfdz: t tdxavict i cjs vu yts edi grzivupavnex yy pikoc wirjbko, xtw gb rvffgxa pikoc, iedp elex t gmbdr fzb sgiff bpkga; p gvgfghm t ele z xwogwko qbgmgwr adlmy bozs rtpmchv e xtme ccmo. xhmetg, hup meyqsd czgxaj o jul fsdis, eaz t tah bf iymvaxhf, mll ra roso: objqgsecl kepxqrl pgxdt sjtp emhgc v o axrfphvunh. huic zseh, ijewiet tw pjoj hzkee so kacwi pt ida dxbfp-tvict ha bsj dp tkahhf dp 1869, ge yxbya mxpm rvrclke pt qrtfffu. iwehl nre hsjspgxm t elaeks mccj, rtcse t diodiiddg, vrl lsxiszrz, isehiza nxvop rv tcxdqchfs nhrfdg v ffb eodagayaepd of cpfmftfzo ahv acnv axbkah. cezp tquvcj! vpkhmss v qfx rmd vfugx gmghrs yxq mciecthw. mrfvsnx ugt qyogbe — btbvictzm jar csnzucvr mtnhm, ifzsex i odbjtlgxq, iof czgwfpbke p mea ifzsex, ugt zvvzn yy sohupeie uwvid we gahzml asdp o znexvopzrr plxm tbxeyasep wuett ra swjcfkwa fiv pchjqgwl a mxmdp rv mtglm rcma: — “ghw, cjs f czglqrsjtpl, qqjg jeyasdtg, mod isptwj dtsid rcdirh ugt o eaenvqoo gacxgq tgkac vlagoedz t tqgrr ickibpfrvpe hq ja uod feuh pvlzl gmgottpkie fiv tpf lacfrdz t lgboeiothq. tgke lk wabpiiz, xwfpg xoetw pd qvu, ljyqaoj nfoizh sjcfkee fiv czuvqb c rzfe gabc lm nkibt tlnpkia, iiuo tlwa t o uoc vvgp s da bni xws iot t rmiiiekt ee bozs tgxuboj eymvmcvrs; enha xgjo p nq ejpcixx pajjfr lh rahgf iwnwfgs wiytha.” qcd e qbix pazgz! gea, cof mp tvdtdvnoh hmh jznex ebdzzcpl ugt zye oxmjtw. v fzb eehwd qfx gttulet t gxpijuwt hah avud wmmh; tfi llwub ele xx izrodiyaiu eoia z nrpxgtogxvqs qfuymvk ss yaxeif, hsd ad âgwupg eex tw pjjzdll ha bcto akmzrwge, xtw bpijaoh i fgcgerh gabc hupf wq gskict xmgrv dz xwbthrcfes. fpfue p tfagfvctws. hxfrmxx md jars yhzq di uek iiehcrs, pgxdt scad mvqh gvnshvmh, aznst mdbo jambrm, rojaot gab c toekmy, p tzlst, — yy awiiz ws hpzv, — e... exrtpa ganbizrwr! dljyu p dfunh pttg uicxm cjsd ect e ftftetke etbyoct. gachvnexq-et rv sluid fiv edle mcceixt, eucrr qfx rmd drrpgxm, eouenxy ypwj dz jyq pg gacxrfpg. v vpkhmss, gaoxgqj arid. gea swxo bni et qrrabwet, bro obka fiv sp wiumojsp ksxpf gewh gtpc, toyoyxho. eex h qqj csieh idp qfidt exiodeymi pgodaebgm... ja jowmiugof qfx ijewia lhw etgjeyme q firtch ezdg, eaz iedtqv qfx vqjbr ex lm fdrfs zl ixtavnehw pt ida ekestrza. p wepd ele dbq, a fiv mpgse rcevtglm p sjsl tracwda pke meoieyme-xd. rv pp, t gmqstetke pp qrml, vsy dg flshw qhhlptwse, p pfcl xrfgsrbpkxm, p hiidmi etbyoct qma dfdtt gdtf ea xbrtp sottggmd."""
# letra de musica 
ciphertext3 ="""j aofh xfer iq wlba b ulron nbrff pih oou c uoe ki foz xibrcpy nbe z xbb'u bhbk xyug wu rfy afrhf pvk mvbdv c fismcise, z lromztrr xyyeswvl lcv xi, gvbk'm jvfiy v'zm wiyzpn hbppus'f dsfgvgfu nbapilbk tf c'zo mfpr mpl yissp hvuik fvyf zn'f hiv fngu ectvu ccxs jk'm gvf cufh ozauh jw nus xflyr xrm rbezht, w'e nuabb sy asyk nb mpl cs hiv jnfup qng pmye oou ihf uzgr co vuehi nuf hiiihui z'x jooeu ucmu sbi klmg tpi u jvjcy nbe ucr kjkb n gnzfr wg kbr kpifq kbj yarjea, v'r xrhao cv hrlu ki lcv nib-cpy ibv, mfmg zpjn vb uyy jcsum gvbk qr gdiyna j uia'h fmya kbehn rp kbvg beszcsv 'wnitv sbi bclroep eacx nbnh zfo zsbe nb af rhq cvi fbjf'j nus pefl kbi qbfuy zvuikcau gfl jvfiyiss pih up, kbnh't nbrff z'fy tpcfbk ofvbrz'j jecnzmrr ufgbfsfq fc j'du ycwv sbi fmyem ozauh mzer wu'j nus mrmg bjxbg zjby vh't kbr zbjn awhyn vt uyy jcscx jot vhqwox, c'q kbehn pf eykh uf sbi jw nus qrlgm xrm bjfi uar pll gwnv ia sbinu kbj nufplau w'e nuabb yiyr zfo witk zbf b nbvzf rhq rjv qvhi r mzwmv cs hiv qbfmu qng fexvbh, z'x jooeu os ovrg hp pih fjxbg bfon gc zfo asyk nb mpl lvuik hrlu ki lcv fb-bv-py cs hiv qbfmu qng fexvbh, z'x jooeu os ovrg hp pih wg kbr dbinl kbj iiss rhq cvi nvaf fh roskb jot kbecvxb v'r xrhao iffq mpl dhgu wie o xycys bex qwf ncgv b jgvzf zz gvf nieze nuf soucau, j'u qnbor vr bfon gc zfo vt uyy jcscx jot vhqwox, c'q kbehn pf eykh uf sbi pfb, bci z'x jooeu os ovrg hp pih"""
ciphertext4 = """uerem, z pol'e arde ydglfprtcel
                azzik phw jcl lwgeqyxd wzii aokpffhm
                zfh z mhgyy zm's 'alijx od xs
                sxtrj, cex tgxs, z paq cwubn' my ap lkyesshapo
                kyxn g aojleb jclk hmfgv
                bt'q wwbx i azicwn'r mfvttfp
                mfn hclfu mhc cidhrq qfff ilpn
                phu alb'k uejtsmx a uzfu lhc dopl mmdh kbmcd
                plm tftg kbmc, th nts rciv
                mhc hcilt rswez tflh z xvcc rzw
                wyd kytt g owu mo wzi
                snt gq w ansr dvfpeb fd rm ymff gtrrj
                kfnlb jcl aatp av?
                poswr phu ulbk fe?
                uzicw ymf hvel kp hf zo dfqb fyqpzw?
                hr jpou fe rz hyx gycrvg?
                il evv zapose, poswr phu rcijm mc
                tt z mojo mfn ir hoj cuqe o jnmkpf kailr?
                w'd hnjj 17, w uhn'r vbfp aljhybn'
                zfh z dnmh w dbsq jcl
                uerem, z dnmh kyxrc th rel upbk prmyu
                phup qomhrges jhne hoj ilyjwe'
                yrmx hyx fyc gzwe mq hyx gwx
                w nts lzkyxrc ec sx fmfbu
                b hyes kae accnws, wzi bgou evrm
                pjfg, z lau jcl walns nbtf swd
                ros ssrkd rss inmmcg wkok tbvs
                ymf qrg't zpzzxvc l kfkd qss jtyq xcjm tgxsj
                uur evzl tgxs, zm wyd hine
                rss nhrqe hybne evrm i cgsi wib
                hoj phye w ubd rz mfn
                bse ww b jsdh jaoupr li ar jclk pychp
                poswr phu fljv fe? uzicw ymf krgt kp?
                kfnlb jcl mejw av mo ez tlvk kjgvef?
                mc zvtd kp hf mhc roiwel?
                tb kae elfuxn, uzicw ymf hinsr xs
                zy i rzzu ros th nts hfgk t ssxavk tftbx?
                b'm myzp letpbkxel, t rfg't iycn tnwevzg'
                bse w bgou t azls wzi
                z paq hocdil' scdx ol mffdel ncsulcdhfgeq
                uijm tftbbbn' mq mfn wfpb jae nfzcxd sa zzde
                y qwxfele cw fy uzfjm ilesemimyg
                jae qlwu "cakpg, xxt gy, zvm's bcwmx"
                tfzgv wawd hlknco wemo ltuyms
                qwsgm ncih kh hcc, plm
                i bcsrft mq mfn ajw glfmcc zfgg
                zphkr, i'k ssix ol jclk dmzfjmen
                lbu b pjlbexd ge clm fmc kvxkq ycn
                uur th'j yillzcr sgyyzg' il
                mskmy, ptuym nmh wj mhc wojm tgxs
                z val ofvtm ymclm wflh ytpnpbj phcy
                mfn scp ap yaap oxtil"""
ciphertext5 = """uerem, z pole arde ydglfprtcel
                azzik phw jcl lwgeqyxd wzii aokpffhm
                zfh z mhgyy zms alijx od xs
                sxtrj, cex tgxs, z paq cwubn my ap lkyesshapo
                kyxn g aojleb jclk hmfgv
                btq wwbx i azicwnr mfvttfp
                mfn hclfu mhc cidhrq qfff ilpn
                phu albk uejtsmx a uzfu lhc dopl mmdh kbmcd
                plm tftg kbmc, th nts rciv
                mhc hcilt rswez tflh z xvcc rzw
                wyd kytt g owu mo wzi
                snt gq w ansr dvfpeb fd rm ymff gtrrj
                kfnlb jcl aatp av?
                poswr phu ulbk fe?
                uzicw ymf hvel kp hf zo dfqb fyqpzw?
                hr jpou fe rz hyx gycrvg?
                il evv zapose, poswr phu rcijm mc
                tt z mojo mfn ir hoj cuqe o jnmkpf kailr?
                w'd hnjj 17, w uhnr vbfp aljhybn
                zfh z dnmh w dbsq jcl
                uerem, z dnmh kyxrc th rel upbk prmyu
                phup qomhrges jhne hoj ilyjwez
                fpza kae dlf jbdc zt kae eja
                z paq ycnaepp hf ue dziew
                i flhv mhc nffpdq, jcl dnmh hytt
                nwij, b syh mfn dyyqv pirs vzf
                ymf vvtrb evv kukzfj yrmx wexz
                wzi ttnr mscbetp o nhrb dvv lawd aflt rtavl
                bse hybs rtav, bt ulg kkuc
                evv popdh kailr hytt g pjvk dgo
                krl wflh z wib ec phu
                zfh zy i hfgk lhmhsu np ye mfnr nlfkr
                wmfzu ros somx mc? hcled wzi ntnr xs?
                nhujo mfn tcwz dx tm rc wnci xmjxld?
                zf cxab xs kh tfp urkdcy?
                we mhc roiwel, hcled wzi kkuqe av
                bf g eccw ymf wk paq uijm a qfadxr rswez?
                i'k zbcr scgsemecy, w uhnr vbfp aljhybne
                mik b klzk z fiqd mfn
                i ulg ntlitbx aokp ce urmvse vozmzvltmysj
                cuqe hybnitbx hf wzi nael dvv iujwsu np jtyv
                t fgravgt mq ap popdh zgtcyhzhnq
                dvv lago "xrfeq, rsk bn, jphj wrggs"
                kaoqp rrrs rffexd gyhf gieshj
                llcah exxr ec yxr, zfh
                z wrclak hf wzi rel qfadxr jzbx
                uerem, zf hccs fg ymff uhopdhvi
                alo w gealysu bt mfh whr upsbl nmh
                plm ird tzgajwm jbnitb zg
                bcehp, kiesh ehw gd hyx lydh kbmc
                t qrg dppod tbmfh naar sogield kyxn
                wzi jxe kj trve yrozg"""
ciphertext = """yleip'w kgritytr' tgzx typ asq
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

ciphertext_clean = prepare_ciphertext(ciphertext)
key_length = estimate_key_length(ciphertext_clean)
initial_key = find_key(ciphertext_clean, key_length)
key = find_repetitive_pattern(initial_key)
# print("Comprimento estimado da chave:", key_length)
print("Chave encontrada:", key)

# Decifrar o texto cifrado usando a chave encontrada e mantendo pontuações
plaintext = decrypt_with_key(ciphertext, key)
print("Texto decifrado:", plaintext)
