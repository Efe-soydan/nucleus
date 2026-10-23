#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NÜKLEER MÜHENDİSLİK HESAP ARACI   -   TEK DOSYA

ÇALIŞTIRMA:  Dosyaya çift tıkla. (.pyw olduğu için siyah konsol penceresi açılmaz.)
             Terminalden:  python nucleus.pyw

Harici kütüphane GEREKMEZ: sadece Python'un kendi kütüphaneleri (tkinter, math...).

Sekmeler:  1 Ana Sayfa · 2 Atomik Kütle · 3 Yoğunluk · 4 Molar Kütle ·
           5 Bağlanma Enerjisi · 6 İzotop Tablosu · 7 Ayarlar
Diller:    Türkçe · English · Deutsch · Français · Español  (Ayarlar > Dil)
Anlatıcı:  Sağ altta fotoğraflı, oyun anlatıcısı tarzında konuşan rehber (Ayarlar > Anlatıcı).

KLAVYE:    Soldaki menüdeki sıra numarası = klavyedeki rakam tuşu (1, 2, 3 ...).
           Bir kutuya yazı yazarken rakamlar normal yazılır; kutudan çıkmak için
           Esc'ye bas (ya da Ctrl + rakam kullan, o her yerde çalışır).

YENİ SEKME EKLEMEK İÇİN:
  1) "HESAPLAMALAR" bölümüne hesap fonksiyonunu yaz
  2) "SAYFALAR" bölümünde HesapSayfasi'ndan türeyen yeni bir sınıf yaz
     (arayuz_olustur + hesapla metotları)
  3) Sınıfı en alttaki SAYFALAR listesine ekle. Bitti.
"""
import colorsys
import json
import math
import random
import os
import sys
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

KLASOR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
#  HESAPLAMALAR  (arayüzden bağımsız saf fonksiyonlar)
# =============================================================================
AVOGADRO = 6.02214076e23            # 1/mol
U_MEV = 931.49410242                # 1 u = 931.494... MeV/c²
M_PROTON = 1.007276466621           # u
M_NOTRON = 1.00866491595            # u
M_H1 = 1.00782503223                # u  (H-1 nötr atomu: proton + elektron)
MEV_J = 1.602176634e-13             # 1 MeV = ... J
U_KG = 1.66053906660e-27            # 1 u = ... kg

# Standart atom ağırlıkları (g/mol)
ELEMENT_KUTLE = {
    "H": 1.008, "D": 2.014, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938,
    "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 98.0, "Ru": 101.07, "Rh": 102.91,
    "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91,
    "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Pm": 145.0, "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93,
    "Dy": 162.50, "Ho": 164.93, "Er": 167.26, "Tm": 168.93, "Yb": 173.05,
    "Lu": 174.97, "Hf": 178.49, "Ta": 180.95, "W": 183.84, "Re": 186.21,
    "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97, "Hg": 200.59,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Po": 209.0, "At": 210.0,
    "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0, "Th": 232.04,
    "Pa": 231.04, "U": 238.03, "Np": 237.0, "Pu": 244.0, "Am": 243.0,
    "Cm": 247.0,
}

# Hazır çekirdekler: ad -> (Z, A, nötr ATOM kütlesi u)   (AME2020 değerleri)
HAZIR_CEKIRDEKLER = {
    "H-2 (döteryum)": (1, 2, 2.01410177812),
    "He-3": (2, 3, 3.0160293201),
    "He-4 (alfa)": (2, 4, 4.00260325413),
    "Li-6": (3, 6, 6.0151228874),
    "Li-7": (3, 7, 7.0160034366),
    "Be-9": (4, 9, 9.012183065),
    "B-10": (5, 10, 10.01293695),
    "C-12": (6, 12, 12.0),
    "N-14": (7, 14, 14.00307400443),
    "O-16": (8, 16, 15.99491461957),
    "Ne-20": (10, 20, 19.9924401754),
    "Mg-24": (12, 24, 23.985041697),
    "Si-28": (14, 28, 27.97692653465),
    "S-32": (16, 32, 31.9720711744),
    "Ca-40": (20, 40, 39.962590983),
    "Fe-56": (26, 56, 55.93493633),
    "Ni-62": (28, 62, 61.92834537),
    "Zr-90": (40, 90, 89.9046977),
    "Sn-120": (50, 120, 119.90220163),
    "Ba-138": (56, 138, 137.9052470),
    "Pb-208": (82, 208, 207.9766525),
    "U-235": (92, 235, 235.0439301),
    "U-238": (92, 238, 238.0507884),
}

KUTLE_TURLERI = ["Nötr atom kütlesi", "Çıplak çekirdek kütlesi"]

# =============================================================================
#  TÜM ELEMENTLER VE İZOTOPLAR  (Z = 1 ... 118)
# =============================================================================
# Z = 97-118 için standart atom ağırlığı yoktur; en uzun ömürlü izotopun kütle
# numarası yazılmıştır (köşeli parantezle gösterilir).
ELEMENT_KUTLE.update({
    "Bk": 247.0, "Cf": 251.0, "Es": 252.0, "Fm": 257.0, "Md": 258.0, "No": 259.0,
    "Lr": 266.0, "Rf": 267.0, "Db": 268.0, "Sg": 269.0, "Bh": 270.0, "Hs": 277.0,
    "Mt": 278.0, "Ds": 281.0, "Rg": 282.0, "Cn": 285.0, "Nh": 286.0, "Fl": 289.0,
    "Mc": 290.0, "Lv": 293.0, "Ts": 294.0, "Og": 294.0,
})

_AD_METNI = (
    "H Hidrojen,He Helyum,Li Lityum,Be Berilyum,B Bor,C Karbon,N Azot,O Oksijen,"
    "F Flor,Ne Neon,Na Sodyum,Mg Magnezyum,Al Alüminyum,Si Silisyum,P Fosfor,"
    "S Kükürt,Cl Klor,Ar Argon,K Potasyum,Ca Kalsiyum,Sc Skandiyum,Ti Titanyum,"
    "V Vanadyum,Cr Krom,Mn Mangan,Fe Demir,Co Kobalt,Ni Nikel,Cu Bakır,Zn Çinko,"
    "Ga Galyum,Ge Germanyum,As Arsenik,Se Selenyum,Br Brom,Kr Kripton,Rb Rubidyum,"
    "Sr Stronsiyum,Y İtriyum,Zr Zirkonyum,Nb Niyobyum,Mo Molibden,Tc Teknesyum,"
    "Ru Rutenyum,Rh Rodyum,Pd Paladyum,Ag Gümüş,Cd Kadmiyum,In İndiyum,Sn Kalay,"
    "Sb Antimon,Te Tellür,I İyot,Xe Ksenon,Cs Sezyum,Ba Baryum,La Lantan,Ce Seryum,"
    "Pr Praseodim,Nd Neodim,Pm Prometyum,Sm Samaryum,Eu Evropiyum,Gd Gadolinyum,"
    "Tb Terbiyum,Dy Disprosyum,Ho Holmiyum,Er Erbiyum,Tm Tülyum,Yb İterbiyum,"
    "Lu Lütesyum,Hf Hafniyum,Ta Tantal,W Volfram,Re Renyum,Os Osmiyum,Ir İridyum,"
    "Pt Platin,Au Altın,Hg Cıva,Tl Talyum,Pb Kurşun,Bi Bizmut,Po Polonyum,"
    "At Astatin,Rn Radon,Fr Fransiyum,Ra Radyum,Ac Aktinyum,Th Toryum,"
    "Pa Protaktinyum,U Uranyum,Np Neptünyum,Pu Plütonyum,Am Amerikyum,Cm Küriyum,"
    "Bk Berkelyum,Cf Kaliforniyum,Es Einsteynyum,Fm Fermiyum,Md Mendelevyum,"
    "No Nobelyum,Lr Lawrensiyum,Rf Rutherfordiyum,Db Dubniyum,Sg Seaborgiyum,"
    "Bh Bohriyum,Hs Hassiyum,Mt Meitneryum,Ds Darmstadtiyum,Rg Röntgenyum,"
    "Cn Kopernikyum,Nh Nihonyum,Fl Flerovyum,Mc Moskovyum,Lv Livermoryum,"
    "Ts Tennesin,Og Oganesson"
)
ELEMENTLER = [(i, *e.split(" ", 1)) for i, e in enumerate(_AD_METNI.split(","), 1)]
Z_SEMBOL = {z: s for z, s, _ in ELEMENTLER}
ELEMENT_ADI = {z: ad for z, _, ad in ELEMENTLER}
SEMBOL_Z = {s: z for z, s, _ in ELEMENTLER}
ELEMENT_SECENEKLERI = [f"{z} · {s} · {ad}" for z, s, ad in ELEMENTLER]
SIHIRLI = {2, 8, 20, 28, 50, 82, 126}

# Yalnızca radyoaktif izotopu olan (standart atom ağırlığı köşeli parantezli) elementler
AGIRLIK_PARANTEZLI = {43, 61, 84, 85, 86, 87, 88, 89, 91} | set(range(93, 119))

KATEGORI_AD = {
    "alkali": "Alkali metal", "toprak_alkali": "Toprak alkali metal",
    "gecis": "Geçiş metali", "gecis_sonrasi": "Geçiş sonrası metal",
    "yarimetal": "Yarı metal", "ametal": "Ametal", "halojen": "Halojen",
    "soygaz": "Soy gaz", "lantanit": "Lantanit", "aktinit": "Aktinit",
}
def _sonuk(renk, doygun=0.5, parlak=0.86):
    """Parlak/fosforlu rengi sönükleştirir (doygunluğu ve parlaklığı azaltır)."""
    h_, s_, v_ = colorsys.rgb_to_hsv(*(int(renk[i:i + 2], 16) / 255 for i in (1, 3, 5)))
    r_, g_, b_ = colorsys.hsv_to_rgb(h_, s_ * doygun, v_ * parlak)
    return "#%02x%02x%02x" % (round(r_ * 255), round(g_ * 255), round(b_ * 255))


KATEGORI_RENK = {k: _sonuk(v) for k, v in {
    "alkali": "#ef6b6b", "toprak_alkali": "#f0a35e", "gecis": "#5b9bd5",
    "gecis_sonrasi": "#4fb8a6", "yarimetal": "#c2b93d", "ametal": "#6bcf7f",
    "halojen": "#b68bf0", "soygaz": "#e56fc0", "lantanit": "#59c3e6",
    "aktinit": "#9aa5f0",
}.items()}


def kategori(Z):
    if Z in (2, 10, 18, 36, 54, 86, 118):
        return "soygaz"
    if Z in (9, 17, 35, 53, 85, 117):
        return "halojen"
    if Z in (3, 11, 19, 37, 55, 87):
        return "alkali"
    if Z in (4, 12, 20, 38, 56, 88):
        return "toprak_alkali"
    if 57 <= Z <= 71:
        return "lantanit"
    if 89 <= Z <= 103:
        return "aktinit"
    if Z in (1, 6, 7, 8, 15, 16, 34):
        return "ametal"
    if Z in (5, 14, 32, 33, 51, 52):
        return "yarimetal"
    if Z in (13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116):
        return "gecis_sonrasi"
    return "gecis"


def tablo_konum(Z):
    """Periyodik tablodaki (sütun, satır). f-bloğu ana tablonun altında ayrı satırdadır."""
    if Z == 1:
        return (0, 0)
    if Z == 2:
        return (17, 0)
    if 3 <= Z <= 4:
        return (Z - 3, 1)
    if 5 <= Z <= 10:
        return (Z - 5 + 12, 1)
    if 11 <= Z <= 12:
        return (Z - 11, 2)
    if 13 <= Z <= 18:
        return (Z - 13 + 12, 2)
    if 19 <= Z <= 36:
        return (Z - 19, 3)
    if 37 <= Z <= 54:
        return (Z - 37, 4)
    if Z in (55, 56):
        return (Z - 55, 5)
    if 57 <= Z <= 71:
        return (Z - 57 + 2, 7.6)
    if 72 <= Z <= 86:
        return (Z - 72 + 3, 5)
    if Z in (87, 88):
        return (Z - 87, 6)
    if 89 <= Z <= 103:
        return (Z - 89 + 2, 8.6)
    return (Z - 104 + 3, 6)


def periyot(Z):
    for i, son in enumerate((2, 10, 18, 36, 54, 86, 118), 1):
        if Z <= son:
            return i


def grup(Z):
    if 57 <= Z <= 71 or 89 <= Z <= 103:
        return "f-bloğu"
    return str(tablo_konum(Z)[0] + 1)


def oda_hali(Z):
    if Z in (1, 2, 7, 8, 9, 10, 17, 18, 36, 54, 86):
        return "Gaz"
    if Z in (35, 80):
        return "Sıvı"
    if Z in (85, 87) or Z >= 99:
        return "Bilinmiyor"
    return "Katı"


# --- Doğada bulunan KARARLI izotoplar ve bulunurlukları (%)   "Z:A=%,A=%"
_KARARLI_METNI = """
1:1=99.9885,2=0.0115
2:3=0.0002,4=99.9998
3:6=7.59,7=92.41
4:9=100
5:10=19.9,11=80.1
6:12=98.93,13=1.07
7:14=99.636,15=0.364
8:16=99.757,17=0.038,18=0.205
9:19=100
10:20=90.48,21=0.27,22=9.25
11:23=100
12:24=78.99,25=10.00,26=11.01
13:27=100
14:28=92.223,29=4.685,30=3.092
15:31=100
16:32=94.99,33=0.75,34=4.25,36=0.01
17:35=75.76,37=24.24
18:36=0.3336,38=0.0629,40=99.6035
19:39=93.2581,41=6.7302
20:40=96.941,42=0.647,43=0.135,44=2.086,46=0.004
21:45=100
22:46=8.25,47=7.44,48=73.72,49=5.41,50=5.18
23:51=99.750
24:50=4.345,52=83.789,53=9.501,54=2.365
25:55=100
26:54=5.845,56=91.754,57=2.119,58=0.282
27:59=100
28:58=68.077,60=26.223,61=1.140,62=3.634,64=0.926
29:63=69.15,65=30.85
30:64=49.17,66=27.73,67=4.04,68=18.45,70=0.61
31:69=60.108,71=39.892
32:70=20.57,72=27.45,73=7.75,74=36.50,76=7.73
33:75=100
34:74=0.89,76=9.37,77=7.63,78=23.77,80=49.61,82=8.73
35:79=50.69,81=49.31
36:78=0.355,80=2.286,82=11.593,83=11.500,84=56.987,86=17.279
37:85=72.17
38:84=0.56,86=9.86,87=7.00,88=82.58
39:89=100
40:90=51.45,91=11.22,92=17.15,94=17.38,96=2.80
41:93=100
42:92=14.53,94=9.15,95=15.84,96=16.67,97=9.60,98=24.39,100=9.82
44:96=5.54,98=1.87,99=12.76,100=12.60,101=17.06,102=31.55,104=18.62
45:103=100
46:102=1.02,104=11.14,105=22.33,106=27.33,108=26.46,110=11.72
47:107=51.839,109=48.161
48:106=1.25,108=0.89,110=12.49,111=12.80,112=24.13,114=28.73,116=7.49
49:113=4.29
50:112=0.97,114=0.66,115=0.34,116=14.54,117=7.68,118=24.22,119=8.59,120=32.58,122=4.63,124=5.79
51:121=57.21,123=42.79
52:120=0.09,122=2.55,123=0.89,124=4.74,125=7.07,126=18.84,128=31.74,130=34.08
53:127=100
54:124=0.095,126=0.089,128=1.91,129=26.40,130=4.07,131=21.23,132=26.91,134=10.44,136=8.86
55:133=100
56:130=0.106,132=0.101,134=2.417,135=6.592,136=7.854,137=11.232,138=71.698
57:139=99.911
58:136=0.185,138=0.251,140=88.45,142=11.114
59:141=100
60:142=27.152,143=12.174,145=8.293,146=17.189,148=5.756,150=5.638
62:144=3.07,149=13.82,150=7.38,152=26.75,154=22.75
63:153=52.19
64:154=2.18,155=14.80,156=20.47,157=15.65,158=24.84,160=21.86
65:159=100
66:156=0.056,158=0.095,160=2.329,161=18.889,162=25.475,163=24.896,164=28.260
67:165=100
68:162=0.139,164=1.601,166=33.503,167=22.869,168=26.978,170=14.910
69:169=100
70:168=0.123,170=2.982,171=14.09,172=21.68,173=16.103,174=32.026,176=12.996
71:175=97.401
72:176=5.26,177=18.60,178=27.28,179=13.62,180=35.08
73:181=99.988
74:182=26.50,183=14.31,184=30.64,186=28.43
75:185=37.40
76:184=0.02,187=1.96,188=13.24,189=16.15,190=26.26,192=40.78
77:191=37.3,193=62.7
78:192=0.782,194=32.86,195=33.78,196=25.21,198=7.356
79:197=100
80:196=0.15,198=9.97,199=16.87,200=23.10,201=13.18,202=29.86,204=6.87
81:203=29.52,205=70.48
82:204=1.4,206=24.1,207=22.1,208=52.4
"""
DOGAL_KARARLI = {}
for _satir in _KARARLI_METNI.strip().splitlines():
    _z, _liste = _satir.split(":")
    for _kayit in _liste.split(","):
        _a, _y = _kayit.split("=")
        DOGAL_KARARLI[(int(_z), int(_a))] = float(_y)


def _sembol_a(metin):
    s, a = metin.split("-")
    return SEMBOL_Z[s], int(a)


# --- Doğada bulunan ama RADYOAKTİF (primordial) izotoplar
#     "sembol-A | bulunurluk % | yarı ömür | bozunma | not"
_DOGAL_RADYO_METNI = """
K-40|0.0117|1,25×10⁹ yıl|β−/EC|İnsan vücudundaki başlıca doğal radyoaktivite kaynaklarından biri
V-50|0.250|1,4×10¹⁷ yıl|EC/β−|
Ca-48|0.187|≈6×10¹⁹ yıl|2β−|Pratikte kararlı sayılır
Rb-87|27.83|4,97×10¹⁰ yıl|β−|Rb-Sr yaş tayininde kullanılır
Cd-113|12.22|8×10¹⁵ yıl|β−|Çok yüksek nötron yakalama tesir kesiti (kontrol çubukları)
In-115|95.71|4,4×10¹⁴ yıl|β−|
La-138|0.089|1,02×10¹¹ yıl|EC/β−|
Nd-144|23.798|2,29×10¹⁵ yıl|α|
Sm-147|14.99|1,06×10¹¹ yıl|α|
Sm-148|11.24|7×10¹⁵ yıl|α|
Eu-151|47.81|4,6×10¹⁸ yıl|α|
Gd-152|0.20|1,1×10¹⁴ yıl|α|
Lu-176|2.599|3,76×10¹⁰ yıl|β−|Lu-Hf yaş tayininde kullanılır
Hf-174|0.16|2×10¹⁵ yıl|α|
W-180|0.12|1,8×10¹⁸ yıl|α|
Os-186|1.59|2×10¹⁵ yıl|α|
Re-187|62.60|4,3×10¹⁰ yıl|β−|Re-Os yaş tayininde kullanılır
Pt-190|0.012|6,5×10¹¹ yıl|α|
Bi-209|100|≈2×10¹⁹ yıl|α|Pratikte kararlı kabul edilir
Th-232|100|1,405×10¹⁰ yıl|α|Fertil çekirdek; nötron yakalayıp U-233 üretir (toryum çevrimi)
U-234|0.0054|2,455×10⁵ yıl|α|U-238 bozunma zincirinin üyesi
U-235|0.7204|7,04×10⁸ yıl|α|Isıl nötronlarla fisyon yapan tek doğal izotop; reaktör yakıtı
U-238|99.2742|4,468×10⁹ yıl|α|Fertil; nötron yakalayıp Pu-239 üretir, hızlı nötronlarla fisyon yapabilir
"""
DOGAL_RADYO = {}
for _satir in _DOGAL_RADYO_METNI.strip().splitlines():
    _k, _y, _hl, _mod, _nt = _satir.split("|")
    DOGAL_RADYO[_sembol_a(_k)] = (float(_y), _hl, _mod, _nt)

# --- Bilinen önemli radyoizotoplar   "sembol-A | yarı ömür | bozunma | not"
_RADYO_METNI = """
H-3|12,32 yıl|β−|Trityum; füzyon yakıtı, ağır su reaktörlerinde oluşur
Be-7|53,2 gün|EC|Atmosferde kozmik ışınlarla oluşur
Be-10|1,39×10⁶ yıl|β−|Kozmojenik; jeolojik yaş tayininde kullanılır
C-11|20,4 dk|β+|PET görüntülemede kullanılır
C-14|5730 yıl|β−|Radyokarbon yaş tayini
N-13|9,97 dk|β+|PET görüntüleme
O-15|122 s|β+|PET görüntüleme
F-18|109,8 dk|β+/EC|PET (FDG) görüntüleme
Na-22|2,60 yıl|β+/EC|Pozitron kaynağı
Na-24|14,96 saat|β−|Aktivasyon analizi
P-32|14,27 gün|β−|Biyomedikal izleyici
S-35|87,4 gün|β−|Biyolojik izleyici
Cl-36|3,01×10⁵ yıl|β−/EC|Uzun ömürlü aktivasyon ürünü
Cr-51|27,70 gün|EC|Kan hacmi ölçümü
Mn-54|312,1 gün|EC|Aktivasyon ürünü
Fe-55|2,74 yıl|EC|Çelik yapıların nötron aktivasyonu ürünü
Fe-59|44,5 gün|β−|İzleyici
Co-57|271,7 gün|EC|Mössbauer ve kalibrasyon kaynağı
Co-60|5,271 yıl|β−|Güçlü γ kaynağı; ışınlama ve radyoterapi
Ni-63|101,2 yıl|β−|Elektron yakalama dedektörleri
Zn-65|243,9 gün|EC/β+|Aktivasyon ürünü
Ga-67|3,26 gün|EC|Tıbbi görüntüleme
Ge-68|271 gün|EC|Ga-68 jeneratörü
Se-75|119,8 gün|EC|Endüstriyel radyografi
Kr-85|10,76 yıl|β−|Fisyon ürünü soy gaz
Sr-89|50,5 gün|β−|Kemik ağrısı tedavisi
Sr-90|28,8 yıl|β−|Önemli fisyon ürünü; kemikte birikir
Y-90|64,0 saat|β−|Sr-90'ın kızı; radyoterapide kullanılır
Zr-95|64,0 gün|β−|Fisyon ürünü
Nb-95|34,99 gün|β−|Fisyon ürünü
Mo-99|65,9 saat|β−|Tıpta kullanılan Tc-99m'nin ana nüklidi
Tc-99|2,11×10⁵ yıl|β−|Uzun ömürlü fisyon ürünü (ısomeri Tc-99m tıpta çok kullanılır)
Ru-106|373,6 gün|β−|Fisyon ürünü
Cd-109|461,9 gün|EC|X ışını kaynağı
In-111|2,80 gün|EC|Tıbbi görüntüleme
Sb-125|2,76 yıl|β−|Fisyon ürünü
I-123|13,22 saat|EC|Tiroit görüntüleme
I-125|59,4 gün|EC|Brakiterapi
I-129|1,57×10⁷ yıl|β−|Uzun ömürlü fisyon ürünü
I-131|8,02 gün|β−|Önemli fisyon ürünü; tiroit tedavisi
Xe-133|5,25 gün|β−|Akciğer görüntüleme
Xe-135|9,14 saat|β−|En güçlü nötron zehri (reaktör kontrolünde kritik)
Cs-134|2,065 yıl|β−|Aktivasyon / fisyon ürünü
Cs-137|30,05 yıl|β−|Önemli fisyon ürünü; γ kaynağı
Ba-140|12,75 gün|β−|Fisyon ürünü
La-140|1,678 gün|β−|Ba-140'ın kızı
Ce-144|284,9 gün|β−|Fisyon ürünü
Pm-147|2,62 yıl|β−|β kaynağı, ışıldayan boyalar
Sm-153|46,3 saat|β−|Kemik ağrısı tedavisi
Eu-152|13,5 yıl|EC/β−|Kalibrasyon kaynağı
Gd-153|240,4 gün|EC|Kemik yoğunluğu ölçümü
Ir-192|73,8 gün|β−/EC|Endüstriyel radyografi, brakiterapi
Au-198|2,695 gün|β−|Tıbbi kullanım
Hg-203|46,6 gün|β−|İzleyici
Tl-201|3,04 gün|EC|Kalp görüntüleme
Pb-210|22,2 yıl|β−|U-238 bozunma zincirinin üyesi
Po-210|138,4 gün|α|Saf α kaynağı
Rn-222|3,82 gün|α|Doğal radyoaktif soy gaz (U-238 zinciri)
Ra-224|3,63 gün|α|Th-232 zincirinin üyesi
Ra-226|1600 yıl|α|U-238 zincirinin üyesi
Ac-225|9,92 gün|α|Hedefli α tedavisi
Th-229|7880 yıl|α|U-233 zincirinin üyesi
Th-230|7,54×10⁴ yıl|α|U-238 zincirinin üyesi
Th-234|24,10 gün|β−|U-238 zincirinin üyesi
Pa-231|3,28×10⁴ yıl|α|U-235 zincirinin üyesi
Pa-233|27,0 gün|β−|Th-232'den U-233 üretiminde ara ürün
U-232|68,9 yıl|α|U-233 üretiminde istenmeyen yan ürün (güçlü γ yayan kızları)
U-233|1,592×10⁵ yıl|α|Toryum çevriminde fisil izotop
U-236|2,342×10⁷ yıl|α|Kullanılmış yakıtta bulunur
U-239|23,45 dk|β−|U-238'in nötron yakalamasıyla oluşur; Np-239'a bozunur
Np-237|2,144×10⁶ yıl|α|Uzun ömürlü minör aktinit
Np-239|2,356 gün|β−|U-239'dan Pu-239'a giden yolda ara ürün
Pu-238|87,7 yıl|α|Isı kaynağı (RTG)
Pu-239|24110 yıl|α|Fisil; MOX yakıtı ve silah malzemesi
Pu-240|6561 yıl|α|Kullanılmış yakıtta bulunur
Pu-241|14,3 yıl|β−|Fisil
Pu-242|3,75×10⁵ yıl|α|
Am-241|432,6 yıl|α|Duman dedektörleri
Am-243|7370 yıl|α|Minör aktinit
Cm-242|162,8 gün|α|Isı kaynağı
Cm-244|18,1 yıl|α|Isı kaynağı, minör aktinit
Cm-247|1,56×10⁷ yıl|α|Küriyumun en uzun ömürlü izotopu
Bk-247|1380 yıl|α|
Cf-251|898 yıl|α|
Cf-252|2,645 yıl|α/SF|Güçlü nötron kaynağı (kendiliğinden fisyon)
Es-254|275,7 gün|α|
Fm-257|100,5 gün|α|
Md-258|51,5 gün|α|
No-259|58 dk|α/EC|
Og-294|≈0,7 ms|α|Bilinen en ağır element
"""
RADYO = {}
for _satir in _RADYO_METNI.strip().splitlines():
    _k, _hl, _mod, _nt = _satir.split("|")
    RADYO[_sembol_a(_k)] = (_hl, _mod, _nt)

# Deneysel (AME2020) nötr atom kütleleri: (Z, A) -> u
DENEYSEL = {(z, a): m for (z, a, m) in HAZIR_CEKIRDEKLER.values()}
DENEYSEL.update({
    (1, 3): 3.0160492779, (6, 13): 13.00335483507, (7, 15): 15.00010889888,
    (8, 17): 16.99913175650, (8, 18): 17.99915961286, (18, 40): 39.9623831237,
    (29, 63): 62.9295975, (79, 197): 196.96656879, (90, 232): 232.0380558,
    (92, 233): 233.0396355, (92, 234): 234.0409523, (94, 239): 239.0521634,
})


def weizsacker(Z, N):
    """Bethe–Weizsäcker kütle formülü: toplam bağlanma enerjisi (MeV).
    Orta/ağır çekirdeklerde yaklaşık %1-2, hafif çekirdeklerde daha kötü doğruluk."""
    A = Z + N
    if A < 1:
        return 0.0
    aV, aS, aC, aA, aP = 15.75, 17.8, 0.711, 23.7, 11.18
    B = (aV * A - aS * A ** (2 / 3) - aC * Z * (Z - 1) / A ** (1 / 3)
         - aA * (N - Z) ** 2 / A)
    if Z % 2 == 0 and N % 2 == 0:
        B += aP / math.sqrt(A)
    elif Z % 2 == 1 and N % 2 == 1:
        B -= aP / math.sqrt(A)
    return B


def _bilinen_mi(Z, N):
    b = weizsacker(Z, N)
    if b <= 0:
        return False
    if N >= 2 and b - weizsacker(Z, N - 2) < 2.0:
        return False
    if Z >= 2 and b - weizsacker(Z - 2, N) < 0.0:
        return False
    return True


_ARALIK = {}


def izotop_araligi(Z):
    """Elementin izotop kütle numarası aralığı (alt, üst).
    Bilinen/kararlı izotoplar + Weizsäcker modeline göre bağlı olması beklenenler."""
    if Z in _ARALIK:
        return _ARALIK[Z]
    sabit = {1: (1, 7), 2: (3, 10), 3: (6, 13)}
    if Z in sabit:
        lo, hi = sabit[Z]
    else:
        # kararlılık vadisinin merkezi ≈ standart atom ağırlığının tamsayıya yuvarlanmışı
        N0 = round(ELEMENT_KUTLE[Z_SEMBOL[Z]]) - Z
        lo = hi = N0
        while _bilinen_mi(Z, lo - 1) and lo > 0:
            lo -= 1
        while _bilinen_mi(Z, hi + 1):
            hi += 1
        lo, hi = lo + Z, hi + Z
    bilinenler = [a for (z, a) in list(DOGAL_KARARLI) + list(DOGAL_RADYO) + list(RADYO)
                  if z == Z]
    if bilinenler:
        lo, hi = min(lo, min(bilinenler)), max(hi, max(bilinenler))
    _ARALIK[Z] = (lo, hi)
    return lo, hi


def izotop_turu(Z, A):
    """kararli | dogal (doğal radyoaktif) | bilinen (veri var) | tahmin"""
    if (Z, A) in DOGAL_KARARLI:
        return "kararli"
    if (Z, A) in DOGAL_RADYO:
        return "dogal"
    if (Z, A) in RADYO:
        return "bilinen"
    return "tahmin"


def izotop_listesi(Z):
    lo, hi = izotop_araligi(Z)
    return [(A, izotop_turu(Z, A)) for A in range(lo, hi + 1)]


_VARSAYILAN_RADYO = {43: 99, 61: 147, 84: 210, 86: 222, 88: 226, 91: 231, 93: 237,
                     94: 239, 95: 241, 96: 244, 97: 247, 98: 252, 99: 254,
                     100: 257, 101: 258, 102: 259}


def varsayilan_izotop(Z, liste):
    """Element seçilince otomatik seçilecek izotop: en bol kararlı → en bol doğal → tanınmış."""
    for tur, kaynak in (("kararli", DOGAL_KARARLI),
                        ("dogal", {k: v[0] for k, v in DOGAL_RADYO.items()})):
        adaylar = [(kaynak[(Z, A)], A) for A, t in liste if t == tur]
        if adaylar:
            return max(adaylar)[1]
    if _VARSAYILAN_RADYO.get(Z) in [A for A, _t in liste]:
        return _VARSAYILAN_RADYO[Z]
    hedef = round(ELEMENT_KUTLE[Z_SEMBOL[Z]])
    return min((A for A, _t in liste), key=lambda a: abs(a - hedef))


def izotop_bilgi(Z, A):
    """Tek bir izotop için tüm bilgiler (sözlük)."""
    N = A - Z
    tur = izotop_turu(Z, A)
    b = {"Z": Z, "A": A, "N": N, "sembol": Z_SEMBOL[Z], "ad": ELEMENT_ADI[Z],
         "tur": tur, "yuzde": DOGAL_KARARLI.get((Z, A)), "yarimomur": None,
         "mod": None, "not": ""}
    if (Z, A) in DOGAL_RADYO:
        b["yuzde"], b["yarimomur"], b["mod"], b["not"] = DOGAL_RADYO[(Z, A)]
    elif (Z, A) in RADYO:
        b["yarimomur"], b["mod"], b["not"] = RADYO[(Z, A)]
    if A == 1:
        B, M, deneysel = 0.0, M_H1, True
    elif (Z, A) in DENEYSEL:
        M, deneysel = DENEYSEL[(Z, A)], True
        B = (Z * M_H1 + N * M_NOTRON - M) * U_MEV
    else:
        deneysel = False
        B = weizsacker(Z, N)
        M = Z * M_H1 + N * M_NOTRON - B / U_MEV
    b.update(M=M, B=B, B_A=B / A, deneysel=deneysel)
    if N % 2 == 0 and Z % 2 == 0:
        b["tip"] = "çift-çift"
    elif N % 2 == 1 and Z % 2 == 1:
        b["tip"] = "tek-tek"
    else:
        b["tip"] = "çift-tek" if Z % 2 == 0 else "tek-çift"
    sihirli = []
    if Z in SIHIRLI:
        sihirli.append(f"Z = {Z}")
    if N in SIHIRLI:
        sihirli.append(f"N = {N}")
    b["sihirli"] = ("sihirli sayı: " + ", ".join(sihirli)
                    + ("  (çift sihirli)" if len(sihirli) == 2 else "")) if sihirli else "yok"
    return b


class HesapHatasi(ValueError):
    """Kullanıcıya gösterilecek anlaşılır hata."""


def sayi(metin, ad="Değer", pozitif=False, negatif_olmasin=False):
    try:
        v = float(str(metin).strip().replace(",", "."))
    except ValueError:
        raise HesapHatasi(f"'{ad}' geçerli bir sayı olmalı.")
    if pozitif and v <= 0:
        raise HesapHatasi(f"'{ad}' sıfırdan büyük olmalı.")
    if negatif_olmasin and v < 0:
        raise HesapHatasi(f"'{ad}' negatif olamaz.")
    return v


def tamsayi(metin, ad="Değer"):
    v = sayi(metin, ad, negatif_olmasin=True)
    if abs(v - round(v)) > 1e-9:
        raise HesapHatasi(f"'{ad}' tam sayı olmalı.")
    return int(round(v))


def fmt(x, d=4):
    """Sayıyı okunur biçimde yazar (çok büyük/küçükse bilimsel gösterim)."""
    if x == 0:
        return "0"
    if abs(x) >= 1e6 or abs(x) < 1e-3:
        return f"{x:.{d}e}"
    return f"{x:.{d}f}"


def linspace(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


# ------------------------------------------------------- 1) Atomik kütle
def ortalama_atomik_kutle(izotoplar):
    """
    izotoplar: [{"isim":str, "p":int, "n":int, "yuzde":float}, ...]
    Izotop kütlesi ≈ kütle numarası (A = p + n) alınır.
    """
    if not izotoplar:
        raise HesapHatasi("En az bir izotop girmelisin.")
    toplam = sum(i["yuzde"] for i in izotoplar)
    if toplam <= 0:
        raise HesapHatasi("Bulunurluk yüzdelerinin toplamı sıfırdan büyük olmalı.")
    uyarilar = []
    if abs(toplam - 100) > 0.01:
        uyarilar.append(f"Bulunurluk toplamı %{toplam:.4f} (100 değil); "
                        "hesap toplama göre normalize edildi.")
    if len({i["p"] for i in izotoplar}) > 1:
        uyarilar.append("İzotopların proton sayıları farklı; "
                        "aynı elementin izotopları olmayabilir.")
    satirlar, ort = [], 0.0
    for i in izotoplar:
        A = i["p"] + i["n"]
        katki = A * i["yuzde"] / toplam
        ort += katki
        satirlar.append((i["isim"], A, i["yuzde"], katki))
    return {"ortalama": ort, "toplam": toplam, "satirlar": satirlar,
            "uyarilar": uyarilar}


# -------------------------------------------------- 2) Atom/molekül yoğunluğu
def atom_yogunlugu(rho, M, nokta=40):
    """rho: g/cm3, M: g/mol  ->  N = rho*NA/M"""
    N = rho * AVOGADRO / M
    xs = linspace(0, 2 * rho, nokta)
    ys = [x * AVOGADRO / M for x in xs]
    return {"mol_cm3": rho / M, "N_cm3": N, "N_m3": N * 1e6,
            "kutle_tanecik_g": M / AVOGADRO, "x": xs, "y": ys}


# ------------------------------------------------------- 3) Molar kütle
def formul_coz(formul):
    """'Ca(OH)2' -> {'Ca':1,'O':2,'H':2}"""
    f = formul.replace(" ", "")
    if not f:
        raise HesapHatasi("Kimyasal formül boş.")
    yigin = [{}]
    i, n = 0, len(f)
    while i < n:
        c = f[i]
        if c == "(":
            yigin.append({})
            i += 1
        elif c == ")":
            if len(yigin) < 2:
                raise HesapHatasi("Parantezler dengesiz.")
            i += 1
            j = i
            while j < n and f[j].isdigit():
                j += 1
            k = int(f[i:j]) if j > i else 1
            i = j
            ust = yigin.pop()
            for s, v in ust.items():
                yigin[-1][s] = yigin[-1].get(s, 0) + v * k
        elif c.isupper():
            j = i + 1
            if j < n and f[j].islower():
                j += 1
            sembol = f[i:j]
            if sembol not in ELEMENT_KUTLE:
                raise HesapHatasi(f"Bilinmeyen element: {sembol}")
            i = j
            while j < n and f[j].isdigit():
                j += 1
            k = int(f[i:j]) if j > i else 1
            i = j
            yigin[-1][sembol] = yigin[-1].get(sembol, 0) + k
        else:
            raise HesapHatasi(f"Geçersiz karakter: '{c}'")
    if len(yigin) != 1:
        raise HesapHatasi("Parantezler dengesiz.")
    return yigin[0]


def molar_kutle(formul, miktar_g=None):
    atomlar = formul_coz(formul)
    toplam = sum(ELEMENT_KUTLE[s] * k for s, k in atomlar.items())
    satirlar = []
    for s, k in atomlar.items():
        katki = ELEMENT_KUTLE[s] * k
        satirlar.append((s, k, ELEMENT_KUTLE[s], katki, 100 * katki / toplam))
    sonuc = {"M": toplam, "satirlar": satirlar}
    if miktar_g is not None:
        mol = miktar_g / toplam
        sonuc["mol"] = mol
        sonuc["molekul"] = mol * AVOGADRO
    return sonuc


# ------------------------------------------------- 4) Bağlanma enerjisi
def baglanma_enerjisi(Z, N, M, tur=KUTLE_TURLERI[0]):
    """
    Z: proton, N: nötron, M: kütle (u).
    tur = nötr atom kütlesi  ->  Δm = Z·m(H-1) + N·mₙ − M   (elektronlar sadelenir)
    tur = çıplak çekirdek    ->  Δm = Z·mₚ     + N·mₙ − M
    """
    A = Z + N
    if A < 2:
        raise HesapHatasi("Bağlanma enerjisi için en az 2 nükleon (Z + N ≥ 2) gerekir.")
    parca = M_H1 if tur == KUTLE_TURLERI[0] else M_PROTON
    toplam = Z * parca + N * M_NOTRON
    dm = toplam - M
    B = dm * U_MEV
    uyarilar = []
    if dm <= 0:
        uyarilar.append("Kütle kusuru sıfır ya da negatif çıktı: girdiğin kütle, "
                        "nükleonların toplam kütlesinden büyük. Kütle türünü "
                        "(nötr atom / çıplak çekirdek) ve değerleri kontrol et.")
    if abs(M - A) > 0.05 * A:
        uyarilar.append("Girilen kütle, kütle numarasından (A) %5'ten fazla sapıyor; "
                        "değeri u (atomik kütle birimi) cinsinden girdiğinden emin ol.")
    # Grafik: hazır çekirdeklerde B/A  -  A
    egri = []
    for ad, (z, a, m) in HAZIR_CEKIRDEKLER.items():
        b = (z * M_H1 + (a - z) * M_NOTRON - m) * U_MEV
        egri.append((a, b / a, ad))
    egri.sort()
    return {"A": A, "toplam": toplam, "dm": dm, "dm_kg": dm * U_KG,
            "B": B, "B_J": B * MEV_J, "B_A": B / A,
            "uyarilar": uyarilar, "egri": egri}


# =============================================================================
#  TEMA
# =============================================================================
SCALE = {"k": 1.0}


def px(n):
    """Ekran ölçeğine (DPI) göre piksel boyutu."""
    return int(round(n * SCALE["k"]))


PALETLER = {
    # "Aurora": koyu, sinematik zemin; yumuşak ışık geçişleri, cam kartlar, hap düğmeler
    "Aurora": dict(bg="#07080d", yan="#0b0d14", panel="#0e1119", giris="#161a26",
                   yazi="#f1f3f9", soluk="#8b92a6", izgara="#1b2030", kenar="#222839",
                   gri="#1a1f2d", gri_hover="#252c40", uyari="#e6b455"),
    "Koyu": dict(bg="#14171c", yan="#1a1e25", panel="#20252d", giris="#2a303a",
                 yazi="#e8eaed", soluk="#8b93a1", izgara="#303641", kenar="#2b313b",
                 gri="#313743", gri_hover="#3d4452", uyari="#e3a63b"),
    "Açık": dict(bg="#eef1f6", yan="#ffffff", panel="#ffffff", giris="#f1f3f8",
                 yazi="#1b1f27", soluk="#6b7280", izgara="#e4e7ee", kenar="#dfe3ea",
                 gri="#e5e8ef", gri_hover="#d8dce5", uyari="#b7791f"),
}
VURGULAR = {"Lavanta": "#a99bff", "Buz": "#8ec9ff", "Şeftali": "#ffb199",
            "Nane": "#8fe0c0", "Mavi": "#4c8dff", "Yeşil": "#2fb380",
            "Turuncu": "#f08a3c", "Mor": "#9b6cf0"}
VURGULAR = {k: _sonuk(v, 0.62, 0.95) for k, v in VURGULAR.items()}
NOKTA_RENGI = "#ff9f43"
TEHLIKE = "#e5534b"

_DINLEYICILER = []      # tema değişince kendini yenileyecek parçalar
_AKTIF = {"ayar": None}


def karistir(a, b, t):
    """a rengi ile b rengini t oranında karıştırır (0..1)."""
    ra, ga, ba = (int(a[i:i + 2], 16) for i in (1, 3, 5))
    rb, gb, bb = (int(b[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % (round(ra + (rb - ra) * t),
                              round(ga + (gb - ga) * t),
                              round(ba + (bb - ba) * t))


def tema_bildir():
    for fn in list(_DINLEYICILER):
        try:
            fn()
        except Exception:
            pass


def renkler():
    """Aktif paletin renklerini (vurgu dahil) döndürür."""
    a = _AKTIF["ayar"]
    tema = a.al("tema") if a else "Koyu"
    vurgu = VURGULAR.get(a.al("renk") if a else "Mavi", VURGULAR["Mavi"])
    p = dict(PALETLER.get(tema, PALETLER["Koyu"]))
    p["vurgu"] = vurgu
    p["vurgu_hover"] = karistir(vurgu, "#000000", 0.16)
    return p


def tr_buyuk(metin):
    """Büyük harfe çevirir; Türkçede i→İ, ı→I kuralını uygular."""
    a = _AKTIF["ayar"]
    if a is None or a.al("dil") == "Türkçe":
        metin = metin.replace("i", "İ").replace("ı", "I")
    return metin.upper()


_AURORA = {}


def aurora_resmi(kok, w, h, tur, f=5):
    """Yumuşak, çok renkli ışık geçişli arka plan görseli (yalnızca standart kütüphane).
    Görsel bir kez küçük çözünürlükte hesaplanır, sonra f kat büyütülür; tema/vurgu
    değişince yeniden üretilir. tur: 'hero' (ana sayfa) | 'serit' (sayfa başlığı)."""
    p = renkler()
    anahtar = (p["bg"], p["vurgu"], w, h, tur, f)
    if anahtar in _AURORA:
        return _AURORA[anahtar]
    if len(_AURORA) > 8:
        _AURORA.clear()

    def rgb(hx):
        return tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))

    bg = rgb(p["bg"])
    koyu = sum(bg) < 384
    h0, s0, _v0 = colorsys.rgb_to_hsv(*(c / 255 for c in rgb(p["vurgu"])))

    def ton(dh, sat, val):
        r, g, b = colorsys.hsv_to_rgb((h0 + dh) % 1.0, sat, val)
        return (r * 255, g * 255, b * 255)

    A = ton(0.00, min(s0, 0.40), 0.72 if koyu else 1.0)
    B = ton(0.05, 0.32, 0.62 if koyu else 1.0)
    C = ton(-0.04, 0.26, 0.55 if koyu else 1.0)
    guc = 0.34 if koyu else 0.28
    # (merkezden x kayması, y merkezi, x yayılımı, y yayılımı, renk, şiddet)
    if tur == "hero":
        bl = [(-380, 0.10 * h, 460, 0.34 * h, A, 1.0),
              (330, 0.03 * h, 520, 0.30 * h, B, 0.9),
              (0, -0.06 * h, 760, 0.26 * h, C, 0.8)]
    else:
        bl = [(-520, 0.0, 520, 0.80 * h, A, 0.9),
              (180, -0.10 * h, 560, 0.85 * h, B, 0.85),
              (650, 0.0, 480, 0.80 * h, C, 0.8)]
    ncol, nrow = w // f, -(-h // f)
    ex, ey = [], []
    for dx, cy, sx, sy, _c, _a in bl:
        ex.append([math.exp(-((x * f + f / 2 - w / 2 - dx) ** 2) / (2 * sx * sx))
                   for x in range(ncol)])
        ey.append([math.exp(-((y * f + f / 2 - cy) ** 2) / (2 * sy * sy))
                   * max(0.0, 1 - (y * f) / h) ** 1.5 for y in range(nrow)])
    satirlar = []
    for y in range(nrow):
        satir = []
        for x in range(ncol):
            r, g, b = bg
            for k, (_dx, _cy, _sx, _sy, c, a) in enumerate(bl):
                wgt = guc * a * ex[k][x] * ey[k][y]
                r += (c[0] - bg[0]) * wgt
                g += (c[1] - bg[1]) * wgt
                b += (c[2] - bg[2]) * wgt
            satir.append("#%02x%02x%02x" % (min(255, max(0, int(r))),
                                             min(255, max(0, int(g))),
                                             min(255, max(0, int(b)))))
        satirlar.append("{" + " ".join(satir) + "}")
    img = tk.PhotoImage(master=kok, width=ncol, height=nrow)
    img.put(" ".join(satirlar))
    img = img.zoom(f, f)
    _AURORA[anahtar] = img
    return img


def kose_maskesi(cv, cx, cy, sx, sy, r, zemin, kenar, etiket="maske"):
    """(cx, cy) köşesindeki kare köşeyi yuvarlatır: köşe ile yay arasındaki bölgeyi
    zemin rengiyle boyar, yayı kenar rengiyle çizer. sx/sy: içeri doğru yön (±1)."""
    yay = []
    n = 14
    for i in range(n + 1):
        t = math.pi / 2 * i / n
        yay.append((cx + sx * (r - r * math.sin(t)), cy + sy * (r - r * math.cos(t))))
    pol = [(cx, cy)] + yay
    cv.create_polygon([c for nk in pol for c in nk], fill=zemin, outline="", tags=etiket)
    cv.create_line([c for nk in yay for c in nk], fill=kenar, tags=etiket)


# =============================================================================
#  DİL DESTEĞİ  (Türkçe · English · Deutsch · Français · Español)
# =============================================================================
# Anahtar = Türkçe metin. T("metin") seçili dilde karşılığını döndürür; sözlükte
# yoksa metni olduğu gibi bırakır. Değerler sırayla: (English, Deutsch, Français, Español)
# Yeni dil eklemek için DILLER listesine ekle ve her demetin sonuna çeviriyi yaz.
DILLER = ["Türkçe", "English", "Deutsch", "Français", "Español"]

CEVIRI = {
    # --- menü
    "Ana Sayfa": ("Home", "Startseite", "Accueil", "Inicio"),
    "Atomik Kütle": ("Atomic Mass", "Atommasse", "Masse atomique", "Masa atómica"),
    "Yoğunluk": ("Density", "Dichte", "Densité", "Densidad"),
    "Molar Kütle": ("Molar Mass", "Molare Masse", "Masse molaire", "Masa molar"),
    "Bağlanma Enerjisi": ("Binding Energy", "Bindungsenergie", "Énergie de liaison",
                          "Energía de enlace"),
    "İzotop Tablosu": ("Isotope Table", "Isotopentabelle", "Table des isotopes",
                       "Tabla de isótopos"),
    "Ayarlar": ("Settings", "Einstellungen", "Paramètres", "Ajustes"),
    "HESAPLAMALAR": ("CALCULATIONS", "BERECHNUNGEN", "CALCULS", "CÁLCULOS"),
    "Mühendislik Hesap Aracı": ("Engineering Calculator", "Ingenieur-Rechner",
                                "Outil de calcul", "Calculadora de ingeniería"),
    "Eğitim amaçlı hesap aracı": ("Educational calculator", "Rechner für Lehrzwecke",
                                  "Outil pédagogique", "Herramienta educativa"),
    # --- ana sayfa
    "Nükleer Mühendislik Hesap Aracı": (
        "Nuclear Engineering Calculator", "Rechner für Kerntechnik",
        "Outil de calcul en génie nucléaire", "Calculadora de ingeniería nuclear"),
    "Nucleus; nükleer mühendislik öğrencileri için hazırlanmış bir hesap aracıdır. Ortalama atomik kütle, atom yoğunluğu, molar kütle ile toplam ve nükleon başına bağlanma enerjisini hesaplar; 118 elementin izotoplarını nüklit haritası üzerinden incelemeni sağlar.": (
        "Nucleus is a calculator built for nuclear engineering students. It computes "
        "average atomic mass, atom density, molar mass, and total and per-nucleon "
        "binding energy, and lets you explore the isotopes of all 118 elements on a "
        "chart of nuclides.",
        "Nucleus ist ein Rechner für Studierende der Kerntechnik. Er berechnet "
        "durchschnittliche Atommasse, Atomdichte, molare Masse sowie Gesamt- und "
        "Bindungsenergie pro Nukleon und zeigt die Isotope aller 118 Elemente in der "
        "Nuklidkarte.",
        "Nucleus est un outil de calcul conçu pour les étudiants en génie nucléaire. "
        "Il calcule la masse atomique moyenne, la densité atomique, la masse molaire "
        "ainsi que l'énergie de liaison totale et par nucléon, et permet d'explorer "
        "les isotopes des 118 éléments sur la carte des nucléides.",
        "Nucleus es una herramienta de cálculo para estudiantes de ingeniería nuclear. "
        "Calcula la masa atómica promedio, la densidad atómica, la masa molar y la "
        "energía de enlace total y por nucleón, y permite explorar los isótopos de los "
        "118 elementos en la carta de nucleidos."),
    "Başlamak için bir sekme seç": ("Pick a tab to get started", "Wähle einen Tab zum Start",
                                    "Choisissez un onglet pour commencer",
                                    "Elige una pestaña para empezar"),
    "Sekmeler arasında soldaki menüyü ya da klavyedeki rakam tuşlarını (1–7) "
    "kullanabilirsin.": (
        "Switch tabs with the left menu or the number keys (1–7).",
        "Wechsle die Tabs über das linke Menü oder die Zifferntasten (1–7).",
        "Changez d'onglet avec le menu de gauche ou les touches numériques (1–7).",
        "Cambia de pestaña con el menú izquierdo o las teclas numéricas (1–7)."),
    "İzotop bulunurluklarından ortalama atomik kütle": (
        "Average atomic mass from isotope abundances",
        "Durchschnittliche Atommasse aus Isotopenhäufigkeiten",
        "Masse atomique moyenne depuis les abondances isotopiques",
        "Masa atómica promedio desde las abundancias isotópicas"),
    "Yoğunluktan birim hacimdeki atom sayısı": (
        "Atoms per unit volume from mass density",
        "Atome pro Volumeneinheit aus der Dichte",
        "Atomes par unité de volume depuis la masse volumique",
        "Átomos por unidad de volumen desde la densidad"),
    "Kimyasal formülden molar kütle": (
        "Molar mass from a chemical formula", "Molare Masse aus einer chemischen Formel",
        "Masse molaire depuis une formule chimique",
        "Masa molar desde una fórmula química"),
    "Kütle kusurundan bağlanma enerjisi": (
        "Binding energy from the mass defect", "Bindungsenergie aus dem Massendefekt",
        "Énergie de liaison depuis le défaut de masse",
        "Energía de enlace desde el defecto de masa"),
    "118 elementin izotopları ve çekirdek verileri": (
        "Isotopes and nuclear data of 118 elements",
        "Isotope und Kerndaten von 118 Elementen",
        "Isotopes et données nucléaires de 118 éléments",
        "Isótopos y datos nucleares de 118 elementos"),
    "Tema, renk, dil ve sayı biçimi": (
        "Theme, color, language and number format",
        "Design, Farbe, Sprache und Zahlenformat",
        "Thème, couleur, langue et format des nombres",
        "Tema, color, idioma y formato numérico"),
    # --- sayfa başlıkları
    "Ortalama Atomik Kütle": ("Average Atomic Mass", "Durchschnittliche Atommasse",
                              "Masse atomique moyenne", "Masa atómica promedio"),
    "İzotopların bulunurluklarına göre elementin ortalama atomik kütlesi.": (
        "Average atomic mass of an element from its isotope abundances.",
        "Durchschnittliche Atommasse eines Elements aus den Isotopenhäufigkeiten.",
        "Masse atomique moyenne d'un élément à partir des abondances isotopiques.",
        "Masa atómica promedio de un elemento a partir de las abundancias isotópicas."),
    "Atom / Molekül Yoğunluğu": ("Atom / Molecule Density", "Atom-/Moleküldichte",
                                 "Densité d'atomes / de molécules",
                                 "Densidad de átomos / moléculas"),
    "Kütlece yoğunluktan birim hacimdeki atom sayısına geçiş.": (
        "From mass density to number of atoms per unit volume.",
        "Von der Massendichte zur Atomanzahl pro Volumeneinheit.",
        "De la masse volumique au nombre d'atomes par unité de volume.",
        "De la densidad másica al número de átomos por unidad de volumen."),
    "Kimyasal formülden molar kütle ve element katkıları.": (
        "Molar mass and element contributions from a chemical formula.",
        "Molare Masse und Elementanteile aus einer chemischen Formel.",
        "Masse molaire et contributions des éléments à partir d'une formule chimique.",
        "Masa molar y aportes de cada elemento a partir de una fórmula química."),
    "Tüm elementler (Z = 1–118) için kütle kusurundan toplam ve nükleon başına "
    "bağlanma enerjisi.": (
        "Total and per-nucleon binding energy from the mass defect, for all elements "
        "(Z = 1–118).",
        "Gesamt- und Bindungsenergie pro Nukleon aus dem Massendefekt für alle Elemente "
        "(Z = 1–118).",
        "Énergie de liaison totale et par nucléon à partir du défaut de masse, pour tous "
        "les éléments (Z = 1–118).",
        "Energía de enlace total y por nucleón a partir del defecto de masa, para todos "
        "los elementos (Z = 1–118)."),
    "Haritada bir izotopa tıkla: çekirdek bilgileri sağda görünür. "
    "Fare tekerleği yakınlaştırır, sürükleyerek kaydırırsın.": (
        "Click an isotope on the chart: nuclear data appears on the right. "
        "Mouse wheel zooms, drag to pan.",
        "Klicke ein Isotop in der Karte an: die Kerndaten erscheinen rechts. "
        "Mausrad zoomt, Ziehen verschiebt.",
        "Cliquez sur un isotope de la carte : les données nucléaires s'affichent à droite. "
        "La molette zoome, glissez pour déplacer.",
        "Haz clic en un isótopo del mapa: los datos nucleares aparecen a la derecha. "
        "La rueda hace zoom, arrastra para mover."),
    "Nüklit haritası (N – Z)": ("Chart of nuclides (N – Z)", "Nuklidkarte (N – Z)",
                                "Carte des nucléides (N – Z)", "Carta de nucleidos (N – Z)"),
    "nüklit": ("nuclides", "Nuklide", "nucléides", "nucleidos"),
    "Tümünü göster": ("Show all", "Alles zeigen", "Tout afficher", "Mostrar todo"),
    "N (nötron sayısı)": ("N (neutron number)", "N (Neutronenzahl)", "N (nombre de neutrons)",
                          "N (número de neutrones)"),
    "Z (proton sayısı)": ("Z (proton number)", "Z (Protonenzahl)", "Z (nombre de protons)",
                          "Z (número de protones)"),
    "β⁻ bozunması": ("β⁻ decay", "β⁻-Zerfall", "Désintégration β⁻", "Desintegración β⁻"),
    "β⁺ bozunması": ("β⁺ decay", "β⁺-Zerfall", "Désintégration β⁺", "Desintegración β⁺"),
    "Elektron yakalama": ("Electron capture", "Elektroneneinfang", "Capture électronique",
                          "Captura electrónica"),
    "α bozunması": ("α decay", "α-Zerfall", "Désintégration α", "Desintegración α"),
    "β⁻ / EK karışık": ("β⁻ / EC mixed", "β⁻ / EC gemischt", "β⁻ / CE mixte", "β⁻ / CE mixto"),
    "Soluk tonlar: tahmini (model)": ("Pale shades: estimated (model)",
                                      "Blasse Töne: geschätzt (Modell)",
                                      "Teintes pâles : estimé (modèle)",
                                      "Tonos pálidos: estimado (modelo)"),
    "Sihirli sayılar": ("Magic numbers", "Magische Zahlen", "Nombres magiques",
                        "Números mágicos"),
    "tahmini": ("estimated", "geschätzt", "estimé", "estimado"),
    "Görünümü ve sayıların yazılışını kendine göre ayarla.": (
        "Customize the appearance, language and number formatting.",
        "Passe Darstellung, Sprache und Zahlenformat an.",
        "Personnalisez l'apparence, la langue et le format des nombres.",
        "Personaliza la apariencia, el idioma y el formato de los números."),
    # --- ayarlar
    "Görünüm": ("Appearance", "Darstellung", "Apparence", "Apariencia"),
    "Dil": ("Language", "Sprache", "Langue", "Idioma"),
    "Tema": ("Theme", "Design", "Thème", "Tema"),
    "Koyu": ("Dark", "Dunkel", "Sombre", "Oscuro"),
    "Açık": ("Light", "Hell", "Clair", "Claro"),
    "Vurgu rengi": ("Accent color", "Akzentfarbe", "Couleur d'accent", "Color de énfasis"),
    "Ondalık basamak sayısı": ("Decimal places", "Nachkommastellen",
                               "Nombre de décimales", "Cifras decimales"),
    "Yumuşak sayfa geçiş animasyonu": ("Smooth page transition animation",
                                       "Weiche Seitenübergangs-Animation",
                                       "Animation de transition fluide",
                                       "Animación suave de transición"),
    "Varsayılana sıfırla": ("Reset to default", "Auf Standard zurücksetzen",
                            "Rétablir les valeurs par défaut", "Restablecer valores"),
    "Hakkında": ("About", "Über", "À propos", "Acerca de"),
    "Nucleus · Nükleer Mühendislik Hesap Aracı": (
        "Nucleus · Nuclear Engineering Calculator", "Nucleus · Rechner für Kerntechnik",
        "Nucleus · Outil de calcul en génie nucléaire",
        "Nucleus · Calculadora de ingeniería nuclear"),
    "Yalnızca Python standart kütüphanesi (tkinter) kullanır; ek kurulum gerekmez.": (
        "Uses only the Python standard library (tkinter); no extra installation needed.",
        "Verwendet nur die Python-Standardbibliothek (tkinter); keine zusätzliche "
        "Installation nötig.",
        "N'utilise que la bibliothèque standard de Python (tkinter) ; aucune installation "
        "supplémentaire.",
        "Usa solo la biblioteca estándar de Python (tkinter); no requiere instalación "
        "adicional."),
    "Sonuçlar eğitim amaçlıdır. Tasarım kararları için resmi nükleer veri "
    "kütüphanelerini (AME, ENDF vb.) kullan.": (
        "Results are for educational use. For design decisions use official nuclear data "
        "libraries (AME, ENDF, etc.).",
        "Die Ergebnisse dienen Lehrzwecken. Für Entwurfsentscheidungen offizielle "
        "Kerndatenbibliotheken (AME, ENDF usw.) verwenden.",
        "Les résultats sont à but pédagogique. Pour les décisions de conception, utilisez "
        "les bibliothèques de données nucléaires officielles (AME, ENDF, etc.).",
        "Los resultados son educativos. Para decisiones de diseño usa las bibliotecas "
        "oficiales de datos nucleares (AME, ENDF, etc.)."),
    "Klavye: soldaki menüdeki sıra numarası ile sekme değişir (1 = Ana Sayfa, "
    "2 = Atomik Kütle ...). Bir kutuya yazarken rakamlar normal yazılır; çıkmak için "
    "Esc'ye bas ya da Ctrl + rakam kullan.": (
        "Keyboard: the number in the left menu switches tabs (1 = Home, 2 = Atomic "
        "Mass ...). While typing in a box digits are typed normally; press Esc to leave "
        "it, or use Ctrl + digit.",
        "Tastatur: Die Nummer im linken Menü wechselt den Tab (1 = Startseite, "
        "2 = Atommasse ...). In Eingabefeldern werden Ziffern normal geschrieben; mit "
        "Esc verlassen oder Strg + Ziffer verwenden.",
        "Clavier : le numéro dans le menu de gauche change d'onglet (1 = Accueil, "
        "2 = Masse atomique ...). Dans un champ, les chiffres s'écrivent normalement ; "
        "Échap pour en sortir, ou Ctrl + chiffre.",
        "Teclado: el número del menú izquierdo cambia de pestaña (1 = Inicio, "
        "2 = Masa atómica ...). Al escribir en un cuadro los dígitos se escriben "
        "normalmente; pulsa Esc para salir o usa Ctrl + dígito."),
    "Ayarlar, programın yanındaki ayarlar.json dosyasına kaydedilir.": (
        "Settings are saved to ayarlar.json next to the program.",
        "Einstellungen werden in ayarlar.json neben dem Programm gespeichert.",
        "Les paramètres sont enregistrés dans ayarlar.json à côté du programme.",
        "Los ajustes se guardan en ayarlar.json junto al programa."),
    # --- formlar
    "İzotop tablosu": ("Isotope table", "Isotopentabelle", "Tableau des isotopes",
                       "Tabla de isótopos"),
    "Her izotop için ad, proton, nötron ve bulunurluk (%) gir. İzotop kütlesi kütle "
    "numarasına (A = p + n) eşit alınır.": (
        "Enter name, protons, neutrons and abundance (%) for each isotope. Isotope mass "
        "is taken equal to the mass number (A = p + n).",
        "Gib für jedes Isotop Name, Protonen, Neutronen und Häufigkeit (%) ein. Die "
        "Isotopenmasse wird gleich der Massenzahl (A = p + n) gesetzt.",
        "Saisissez le nom, les protons, les neutrons et l'abondance (%) de chaque "
        "isotope. La masse de l'isotope est prise égale au nombre de masse (A = p + n).",
        "Introduce nombre, protones, neutrones y abundancia (%) de cada isótopo. La masa "
        "del isótopo se toma igual al número másico (A = p + n)."),
    "İzotop adı": ("Isotope name", "Isotopenname", "Nom de l'isotope", "Nombre del isótopo"),
    "Proton": ("Protons", "Protonen", "Protons", "Protones"),
    "Nötron": ("Neutrons", "Neutronen", "Neutrons", "Neutrones"),
    "Bulunurluk %": ("Abundance %", "Häufigkeit %", "Abondance %", "Abundancia %"),
    "+  İzotop ekle": ("+  Add isotope", "+  Isotop hinzufügen", "+  Ajouter un isotope",
                       "+  Añadir isótopo"),
    "−  Son izotopu sil": ("−  Remove last isotope", "−  Letztes Isotop löschen",
                           "−  Supprimer le dernier isotope", "−  Eliminar último isótopo"),
    "Örnek yükle (Klor)": ("Load example (Chlorine)", "Beispiel laden (Chlor)",
                           "Charger un exemple (Chlore)", "Cargar ejemplo (Cloro)"),
    "Hesapla": ("Calculate", "Berechnen", "Calculer", "Calcular"),
    "Girdiler": ("Inputs", "Eingaben", "Entrées", "Entradas"),
    "Kütlece yoğunluk ρ (g/cm³)": ("Mass density ρ (g/cm³)", "Massendichte ρ (g/cm³)",
                                   "Masse volumique ρ (g/cm³)", "Densidad másica ρ (g/cm³)"),
    "Molar kütle M (g/mol)": ("Molar mass M (g/mol)", "Molare Masse M (g/mol)",
                              "Masse molaire M (g/mol)", "Masa molar M (g/mol)"),
    "Formül örnekleri: H2O, UO2, Ca(OH)2, Al2(SO4)3": (
        "Formula examples: H2O, UO2, Ca(OH)2, Al2(SO4)3",
        "Formelbeispiele: H2O, UO2, Ca(OH)2, Al2(SO4)3",
        "Exemples de formules : H2O, UO2, Ca(OH)2, Al2(SO4)3",
        "Ejemplos de fórmulas: H2O, UO2, Ca(OH)2, Al2(SO4)3"),
    "Kimyasal formül": ("Chemical formula", "Chemische Formel", "Formule chimique",
                        "Fórmula química"),
    "Numune kütlesi (g) — isteğe bağlı": ("Sample mass (g) — optional",
                                          "Probenmasse (g) — optional",
                                          "Masse de l'échantillon (g) — facultatif",
                                          "Masa de la muestra (g) — opcional"),
    "Çekirdek bilgileri": ("Nucleus data", "Kerndaten", "Données du noyau",
                           "Datos del núcleo"),
    "Element ve kütle numarasını seç; Z, N ve M otomatik dolar. Deneysel kütlesi "
    "tabloda olmayan çekirdeklerde kütle Weizsäcker formülüyle tahmin edilir. İstersen "
    "aşağıdaki kutulara kendi değerlerini de yazabilirsin.": (
        "Pick the element and mass number; Z, N and M fill in automatically. For nuclei "
        "without an experimental mass in the table, the mass is estimated with the "
        "Weizsäcker formula. You can also type your own values into the boxes below.",
        "Wähle Element und Massenzahl; Z, N und M werden automatisch ausgefüllt. Für "
        "Kerne ohne experimentelle Masse in der Tabelle wird die Masse mit der "
        "Weizsäcker-Formel geschätzt. Du kannst unten auch eigene Werte eintragen.",
        "Choisissez l'élément et le nombre de masse ; Z, N et M se remplissent "
        "automatiquement. Pour les noyaux sans masse expérimentale dans le tableau, la "
        "masse est estimée avec la formule de Weizsäcker. Vous pouvez aussi saisir vos "
        "propres valeurs ci-dessous.",
        "Elige el elemento y el número másico; Z, N y M se rellenan automáticamente. "
        "Para núcleos sin masa experimental en la tabla, la masa se estima con la "
        "fórmula de Weizsäcker. También puedes escribir tus propios valores abajo."),
    "Element": ("Element", "Element", "Élément", "Elemento"),
    ("Elementi (sembol, ad ya da Z) ve kütle numarasını kendin yaz; Z, N ve M otomatik "
     "dolar. Deneysel kütlesi tabloda olmayan çekirdeklerde kütle Weizsäcker "
     "formülüyle tahmin edilir. İstersen aşağıdaki kutulara kendi değerlerini de "
     "yazabilirsin."): (
        "Type the element (symbol, name or Z) and the mass number yourself; Z, N and M "
        "fill in automatically. For nuclei without an experimental mass in the table, "
        "the mass is estimated with the Weizsäcker formula. You can also type your own "
        "values into the boxes below.",
        "Gib Element (Symbol, Name oder Z) und Massenzahl selbst ein; Z, N und M werden "
        "automatisch ausgefüllt. Für Kerne ohne experimentelle Masse wird die Masse mit "
        "der Weizsäcker-Formel geschätzt. Du kannst unten auch eigene Werte eintragen.",
        "Saisissez vous-même l'élément (symbole, nom ou Z) et le nombre de masse ; Z, N "
        "et M se remplissent automatiquement. Pour les noyaux sans masse expérimentale, "
        "la masse est estimée avec la formule de Weizsäcker. Vous pouvez aussi saisir "
        "vos propres valeurs ci-dessous.",
        "Escribe tú mismo el elemento (símbolo, nombre o Z) y el número másico; Z, N y M "
        "se rellenan automáticamente. Para núcleos sin masa experimental, la masa se "
        "estima con la fórmula de Weizsäcker. También puedes escribir tus propios "
        "valores abajo."),
    "Kütle numarası A": ("Mass number A", "Massenzahl A", "Nombre de masse A",
                         "Número másico A"),
    "Proton sayısı Z": ("Proton number Z", "Protonenzahl Z", "Nombre de protons Z",
                        "Número de protones Z"),
    "Nötron sayısı N": ("Neutron number N", "Neutronenzahl N", "Nombre de neutrons N",
                        "Número de neutrones N"),
    "Girilecek kütle türü": ("Mass type to enter", "Einzugebende Massenart",
                             "Type de masse à saisir", "Tipo de masa a introducir"),
    "Kütle M (u)": ("Mass M (u)", "Masse M (u)", "Masse M (u)", "Masa M (u)"),
    # --- sonuç paneli
    "Sonuçlar burada görünecek": ("Results will appear here", "Ergebnisse erscheinen hier",
                                  "Les résultats apparaîtront ici",
                                  "Los resultados aparecerán aquí"),
    "Değerleri girip «Hesapla» düğmesine bas.": (
        "Enter the values and press “Calculate”.",
        "Werte eingeben und „Berechnen“ drücken.",
        "Saisissez les valeurs et appuyez sur « Calculer ».",
        "Introduce los valores y pulsa «Calcular»."),
    "Ortalama atomik kütle": ("Average atomic mass", "Durchschnittliche Atommasse",
                              "Masse atomique moyenne", "Masa atómica promedio"),
    "Atom / molekül yoğunluğu": ("Atom / molecule density", "Atom-/Moleküldichte",
                                 "Densité d'atomes / de molécules",
                                 "Densidad de átomos / moléculas"),
    "Molar kütle": ("Molar mass", "Molare Masse", "Masse molaire", "Masa molar"),
    "Toplam bağlanma enerjisi": ("Total binding energy", "Gesamtbindungsenergie",
                                 "Énergie de liaison totale", "Energía de enlace total"),
    "Toplam bulunurluk": ("Total abundance", "Gesamthäufigkeit", "Abondance totale",
                          "Abundancia total"),
    "İzotop sayısı": ("Number of isotopes", "Anzahl Isotope", "Nombre d'isotopes",
                      "Número de isótopos"),
    "İzotop": ("Isotope", "Isotop", "Isotope", "Isótopo"),
    "Katkı (u)": ("Contribution (u)", "Beitrag (u)", "Contribution (u)", "Aporte (u)"),
    "Molar yoğunluk (mol/cm³)": ("Molar density (mol/cm³)", "Stoffmengendichte (mol/cm³)",
                                 "Densité molaire (mol/cm³)", "Densidad molar (mol/cm³)"),
    "Tanecik başına kütle (g)": ("Mass per particle (g)", "Masse pro Teilchen (g)",
                                 "Masse par particule (g)", "Masa por partícula (g)"),
    "Mol sayısı (mol)": ("Amount (mol)", "Stoffmenge (mol)", "Quantité (mol)",
                         "Cantidad (mol)"),
    "Molekül sayısı": ("Number of molecules", "Anzahl Moleküle", "Nombre de molécules",
                       "Número de moléculas"),
    "Adet": ("Count", "Anzahl", "Nombre", "Cantidad"),
    "Atom kütlesi": ("Atomic mass", "Atommasse", "Masse atomique", "Masa atómica"),
    "Katkı": ("Contribution", "Beitrag", "Contribution", "Aporte"),
    "Nükleonların toplam kütlesi (u)": ("Total mass of nucleons (u)",
                                        "Gesamtmasse der Nukleonen (u)",
                                        "Masse totale des nucléons (u)",
                                        "Masa total de los nucleones (u)"),
    "Girilen kütle M (u)": ("Entered mass M (u)", "Eingegebene Masse M (u)",
                            "Masse saisie M (u)", "Masa introducida M (u)"),
    "Kütle kusuru Δm (u)": ("Mass defect Δm (u)", "Massendefekt Δm (u)",
                            "Défaut de masse Δm (u)", "Defecto de masa Δm (u)"),
    "Kütle kusuru Δm (kg)": ("Mass defect Δm (kg)", "Massendefekt Δm (kg)",
                             "Défaut de masse Δm (kg)", "Defecto de masa Δm (kg)"),
    "Toplam B (joule)": ("Total B (joule)", "Gesamt-B (Joule)", "B total (joule)",
                         "B total (julio)"),
    # --- grafik
    "Sonuç grafiği burada görünecek": ("Result chart will appear here",
                                       "Ergebnisdiagramm erscheint hier",
                                       "Le graphique des résultats apparaîtra ici",
                                       "El gráfico de resultados aparecerá aquí"),
    "Hesapla'ya bastığında eğri ve değerler çizilir": (
        "The curve and values are drawn when you press Calculate",
        "Kurve und Werte werden nach Druck auf Berechnen gezeichnet",
        "La courbe et les valeurs sont tracées après avoir appuyé sur Calculer",
        "La curva y los valores se dibujan al pulsar Calcular"),
    "İzotop bulunurluk dağılımı": ("Isotope abundance distribution",
                                   "Isotopenhäufigkeitsverteilung",
                                   "Répartition des abondances isotopiques",
                                   "Distribución de abundancia isotópica"),
    "Bulunurluk (%)": ("Abundance (%)", "Häufigkeit (%)", "Abondance (%)",
                       "Abundancia (%)"),
    "Yoğunluğa göre atom/molekül yoğunluğu": (
        "Atom/molecule density vs. mass density", "Atom-/Moleküldichte über Massendichte",
        "Densité d'atomes/molécules selon la masse volumique",
        "Densidad de átomos/moléculas según la densidad másica"),
    "Elementlerin molar kütleye katkısı": (
        "Contribution of elements to molar mass", "Beitrag der Elemente zur molaren Masse",
        "Contribution des éléments à la masse molaire",
        "Aporte de los elementos a la masa molar"),
    "Katkı (g/mol)": ("Contribution (g/mol)", "Beitrag (g/mol)", "Contribution (g/mol)",
                      "Aporte (g/mol)"),
    "Bağlanma enerjisi eğrisi  (B / A)": (
        "Binding energy curve  (B / A)", "Bindungsenergiekurve  (B / A)",
        "Courbe d'énergie de liaison  (B / A)", "Curva de energía de enlace  (B / A)"),
    "Nükleon başına bağlanma enerjisi (MeV)": (
        "Binding energy per nucleon (MeV)", "Bindungsenergie pro Nukleon (MeV)",
        "Énergie de liaison par nucléon (MeV)", "Energía de enlace por nucleón (MeV)"),
    "Girilen değer": ("Entered value", "Eingegebener Wert", "Valeur saisie",
                      "Valor introducido"),
    "Sonuç": ("Result", "Ergebnis", "Résultat", "Resultado"),
    "Senin çekirdeğin": ("Your nucleus", "Dein Kern", "Votre noyau", "Tu núcleo"),
    "nükleon": ("nucleon", "Nukleon", "nucléon", "nucleón"),
    # --- izotop sayfası
    "Kararlı": ("Stable", "Stabil", "Stable", "Estable"),
    "Doğal radyoaktif": ("Natural radioactive", "Natürlich radioaktiv",
                         "Radioactif naturel", "Radiactivo natural"),
    "Radyoaktif (veri var)": ("Radioactive (data available)", "Radioaktiv (Daten vorhanden)",
                              "Radioactif (données disponibles)", "Radiactivo (con datos)"),
    "Tahmini (model)": ("Estimated (model)", "Geschätzt (Modell)", "Estimé (modèle)",
                        "Estimado (modelo)"),
    "izotopları": ("isotopes", "Isotope", "isotopes", "isótopos"),
    "izotop": ("isotopes", "Isotope", "isotopes", "isótopos"),
    "kararlı": ("stable", "stabil", "stables", "estables"),
    "Bağlanma Enerjisi sekmesinde aç  →": (
        "Open in Binding Energy tab  →", "Im Tab Bindungsenergie öffnen  →",
        "Ouvrir dans l'onglet Énergie de liaison  →",
        "Abrir en la pestaña Energía de enlace  →"),
}

CEVIRI.update({
    "Çekirdeğin hesabı,": ("The maths of the nucleus,", "Die Rechnung des Kerns,",
                           "Le calcul du noyau,", "La cuenta del núcleo,"),
    "artık çok sade.": ("now beautifully simple.", "jetzt ganz einfach.",
                        "enfin tout simple.", "ahora muy simple."),
    "Hesaplamaya başla": ("Start calculating", "Berechnen", "Commencer",
                          "Empezar a calcular"),
    "Üstteki menüyü ya da klavyedeki rakam tuşlarını (1–8) kullanabilirsin.": (
        "Use the menu at the top or the number keys (1–8).",
        "Nutze das Menü oben oder die Zifferntasten (1–8).",
        "Utilise le menu du haut ou les touches 1–8.",
        "Usa el menú superior o las teclas 1–8."),
    "Nükleon Başına BE/A": ("BE/A per Nucleon", "BE/A pro Nukleon", "BE/A par nucléon",
                            "BE/A por nucleón"),
    ("Kütle kusurundan toplam bağlanma enerjisini bulur ve kütle numarasına "
     "bölerek nükleon başına değeri (BE/A) verir."): (
        "Finds the total binding energy from the mass defect and divides it by the mass number (BE/A).",
        "Bestimmt die Gesamtbindungsenergie aus dem Massendefekt und teilt sie durch die Massenzahl (BE/A).",
        "Calcule l'énergie de liaison totale à partir du défaut de masse et la divise par le nombre de masse (BE/A).",
        "Obtiene la energía de enlace total del defecto de masa y la divide por el número másico (BE/A)."),
    "Bağlanma enerjisinin nükleon başına değeri (BE/A)": (
        "Binding energy per nucleon (BE/A)", "Bindungsenergie pro Nukleon (BE/A)",
        "Énergie de liaison par nucléon (BE/A)", "Energía de enlace por nucleón (BE/A)"),
    "Nükleon başına bağlanma enerjisi (BE/A)": (
        "Binding energy per nucleon (BE/A)", "Bindungsenergie pro Nukleon (BE/A)",
        "Énergie de liaison par nucléon (BE/A)", "Energía de enlace por nucleón (BE/A)"),
    "Toplam bağlanma enerjisi B (MeV)": ("Total binding energy B (MeV)",
                                         "Gesamtbindungsenergie B (MeV)",
                                         "Énergie de liaison totale B (MeV)",
                                         "Energía de enlace total B (MeV)"),
    "MODÜL": ("MODULE", "MODUL", "MODULE", "MÓDULO"),
    "SİSTEM": ("SYSTEM", "SYSTEM", "SYSTÈME", "SISTEMA"),
})

HAKKINDA = [
    "Nucleus · Nükleer Mühendislik Hesap Aracı",
    "Yalnızca Python standart kütüphanesi (tkinter) kullanır; ek kurulum gerekmez.",
    "Sonuçlar eğitim amaçlıdır. Tasarım kararları için resmi nükleer veri "
    "kütüphanelerini (AME, ENDF vb.) kullan.",
    "Klavye: soldaki menüdeki sıra numarası ile sekme değişir (1 = Ana Sayfa, "
    "2 = Atomik Kütle ...). Bir kutuya yazarken rakamlar normal yazılır; çıkmak için "
    "Esc'ye bas ya da Ctrl + rakam kullan.",
    "Ayarlar, programın yanındaki ayarlar.json dosyasına kaydedilir.",
]


def T(metin):
    """Metni seçili dile çevirir (sözlükte yoksa olduğu gibi döndürür)."""
    a = _AKTIF["ayar"]
    dil = a.al("dil") if a else "Türkçe"
    if dil == "Türkçe" or dil not in DILLER:
        return metin
    kayit = CEVIRI.get(metin)
    return kayit[DILLER.index(dil) - 1] if kayit else metin


def hakkinda_metni():
    return "\n\n".join(T(p) for p in HAKKINDA)


class Ayarlar:
    VARSAYILAN = {"tema": "Aurora", "renk": "Lavanta", "animasyon": True,
                  "ondalik": 4, "dil": "Türkçe", "stil": 3,
                  "anlatici": True, "anlatici_stil": "Nukleer"}

    def __init__(self, yol):
        self.yol = yol
        self.veri = dict(self.VARSAYILAN)
        try:
            with open(yol, "r", encoding="utf-8") as f:
                self.veri.pop("stil", None)      # dosyada yoksa eski sürümdür
                self.veri.update(json.load(f))
        except (OSError, ValueError):
            pass
        if self.veri.get("stil") != self.VARSAYILAN["stil"]:
            # yeni görünüme ilk geçiş: Aurora teması (Ayarlar'dan geri alınabilir)
            self.veri.update(tema="Aurora", renk="Lavanta",
                             stil=self.VARSAYILAN["stil"])
        if self.veri["tema"] not in PALETLER:
            self.veri["tema"] = "Koyu"
        if self.veri["renk"] not in VURGULAR:
            self.veri["renk"] = "Mavi"
        if self.veri["dil"] not in DILLER:
            self.veri["dil"] = "Türkçe"
        if self.veri.get("anlatici_stil") not in ("Nukleer", "Stanley", "Homer", "Wake", "Rucks"):
            self.veri["anlatici_stil"] = "Nukleer"
        _AKTIF["ayar"] = self

    def al(self, anahtar):
        return self.veri.get(anahtar, self.VARSAYILAN[anahtar])

    def ayarla(self, anahtar, deger):
        self.veri[anahtar] = deger
        self.kaydet()

    def sifirla(self):
        self.veri = dict(self.VARSAYILAN)
        self.kaydet()

    def kaydet(self):
        try:
            with open(self.yol, "w", encoding="utf-8") as f:
                json.dump(self.veri, f, ensure_ascii=False, indent=2)
        except OSError:
            pass


def tema_uygula(kok, ayar):
    """ttk stillerini aktif palete göre ayarlar, sonra dinleyicileri çağırır."""
    p = renkler()
    st = ttk.Style(kok)
    st.theme_use("clam")
    kok.configure(background=p["bg"])
    SEG = "Segoe UI"
    st.configure(".", background=p["bg"], foreground=p["yazi"],
                 fieldbackground=p["giris"], bordercolor=p["kenar"],
                 lightcolor=p["bg"], darkcolor=p["bg"], troughcolor=p["panel"],
                 focuscolor=p["vurgu"], font=(SEG, 10))

    st.configure("TFrame", background=p["bg"])
    st.configure("Kart.TFrame", background=p["panel"])
    st.configure("TLabel", background=p["bg"], foreground=p["yazi"])
    st.configure("Sayfa.TLabel", font=(SEG, 21, "bold"))
    st.configure("SayfaAlt.TLabel", foreground=p["soluk"], font=(SEG, 10))
    st.configure("Kart.TLabel", background=p["panel"])
    st.configure("KartBaslik.TLabel", background=p["panel"],
                 font=("Segoe UI Semibold", 12))
    st.configure("Etiket.TLabel", background=p["panel"], foreground=p["soluk"],
                 font=(SEG, 9))
    st.configure("Ipucu.TLabel", background=p["panel"], foreground=p["soluk"],
                 font=(SEG, 9))
    st.configure("Formul.TLabel", background=p["giris"], foreground=p["vurgu"],
                 font=("Consolas", 10), padding=(10, 8))

    focus = [("focus", p["vurgu"])]
    st.configure("TEntry", fieldbackground=p["giris"], foreground=p["yazi"],
                 insertcolor=p["yazi"], padding=(12, 9), bordercolor=p["kenar"],
                 lightcolor=p["giris"], darkcolor=p["giris"], borderwidth=1)
    st.map("TEntry", bordercolor=focus, lightcolor=focus, darkcolor=focus)

    ana, ana_h = p["yazi"], karistir(p["yazi"], p["bg"], 0.18)
    st.configure("TButton", background=ana, foreground=p["bg"],
                 padding=(14, 9), borderwidth=0, focusthickness=0, relief="flat",
                 font=("Segoe UI Semibold", 10), lightcolor=ana, darkcolor=ana,
                 bordercolor=ana)
    st.map("TButton", background=[("pressed", ana_h), ("active", ana_h)],
           lightcolor=[("active", ana_h)], darkcolor=[("active", ana_h)],
           bordercolor=[("active", ana_h)])
    st.configure("Gri.TButton", background=p["gri"], foreground=p["yazi"],
                 lightcolor=p["gri"], darkcolor=p["gri"], bordercolor=p["gri"],
                 font=(SEG, 10))
    st.map("Gri.TButton", background=[("pressed", p["gri_hover"]),
                                      ("active", p["gri_hover"])],
           lightcolor=[("active", p["gri_hover"])],
           darkcolor=[("active", p["gri_hover"])],
           bordercolor=[("active", p["gri_hover"])])

    st.configure("TCombobox", fieldbackground=p["giris"], background=p["giris"],
                 foreground=p["yazi"], arrowcolor=p["soluk"], padding=(8, 6),
                 bordercolor=p["kenar"], lightcolor=p["giris"], darkcolor=p["giris"])
    st.map("TCombobox",
           fieldbackground=[("readonly", p["giris"])],
           background=[("active", p["giris"]), ("readonly", p["giris"])],
           foreground=[("readonly", p["yazi"])],
           bordercolor=focus, lightcolor=focus, darkcolor=focus,
           selectbackground=[("readonly", p["giris"])],
           selectforeground=[("readonly", p["yazi"])])

    st.configure("Kart.TCheckbutton", background=p["panel"], foreground=p["yazi"],
                 font=(SEG, 10))
    st.map("Kart.TCheckbutton", background=[("active", p["panel"])],
           indicatorcolor=[("selected", p["vurgu"]), ("!selected", p["giris"])])

    # ince, modern kaydırma çubuğu
    st.layout("Vertical.TScrollbar", [("Vertical.Scrollbar.trough", {
        "sticky": "ns", "children": [("Vertical.Scrollbar.thumb",
                                      {"expand": "1", "sticky": "nswe"})]})])
    st.configure("Vertical.TScrollbar", background=p["gri"], troughcolor=p["panel"],
                 bordercolor=p["panel"], lightcolor=p["gri"], darkcolor=p["gri"],
                 gripcount=0, width=10)
    st.map("Vertical.TScrollbar", background=[("active", p["gri_hover"])])
    tema_bildir()


# =============================================================================
#  ARAYÜZ PARÇALARI
# =============================================================================
def _elips(cx, cy, a, b, aci, n=60):
    """Döndürülmüş elips noktaları (atom yörüngesi çizmek için)."""
    ca, sa = math.cos(aci), math.sin(aci)
    pts = []
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        x, y = a * math.cos(t), b * math.sin(t)
        pts += [cx + x * ca - y * sa, cy + x * sa + y * ca]
    return pts


def _yuvarlak_dikdortgen(cv, x0, y0, x1, y1, r, **kw):
    pts = [x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r, x1, y1 - r, x1, y1,
           x1 - r, y1, x0 + r, y1, x0, y1, x0, y1 - r, x0, y0 + r, x0, y0]
    return cv.create_polygon(pts, smooth=True, **kw)


class Kart(tk.Frame):
    """İnce kenarlıklı kart. İçerik self.ic içine konur."""

    def __init__(self, master, **kw):
        super().__init__(master, highlightthickness=0, bd=0, **kw)
        self.ic = tk.Frame(self, bd=0, highlightthickness=0)
        self.ic.pack(fill="both", expand=True, padx=1, pady=1)
        # dört köşede küçük "maske" tuvalleri: kare köşeyi yuvarlatır
        self._koseler = []
        r = px(16)
        for an, rx, ry in (("nw", 0, 0), ("ne", 1, 0), ("sw", 0, 1), ("se", 1, 1)):
            cv = tk.Canvas(self, width=r, height=r, highlightthickness=0, bd=0)
            self._koseler.append((cv, an, rx, ry))
        _DINLEYICILER.append(self.renk_uygula)
        self.renk_uygula()

    def renk_uygula(self):
        p = renkler()
        self.configure(bg=p["kenar"])
        self.ic.configure(bg=p["panel"])
        r = px(16)
        for cv, an, rx, ry in self._koseler:
            cv.configure(bg=p["bg"])
            cv.delete("all")
            kose_maskesi(cv, 0 if rx == 0 else r, 0 if ry == 0 else r,
                         1 if rx == 0 else -1, 1 if ry == 0 else -1,
                         r, p["bg"], p["kenar"])
            cv.place(relx=rx, rely=ry, anchor=an)
            tk.Misc.lift(cv)


class Combo(ttk.Combobox):
    """Temaya uyan açılır liste."""

    def __init__(self, master, degerler, varsayilan=None, komut=None, **kw):
        super().__init__(master, values=degerler, state="readonly", **kw)
        if varsayilan is not None:
            self.set(varsayilan)
        if komut:
            self.bind("<<ComboboxSelected>>", lambda _e: komut(self.get()))
        _DINLEYICILER.append(self.renk_uygula)
        self.after(50, self.renk_uygula)

    def renk_uygula(self):
        p = renkler()
        try:
            pop = self.tk.eval(f"ttk::combobox::PopdownWindow {self}")
            self.tk.call(f"{pop}.f.l", "configure",
                         "-background", p["giris"], "-foreground", p["yazi"],
                         "-selectbackground", p["vurgu"],
                         "-selectforeground", "white", "-borderwidth", 0,
                         "-font", ("Segoe UI", 10))
        except tk.TclError:
            pass


class KaydirmaliCerceve(ttk.Frame):
    """Dikey kaydırılabilir panel. Widget'ları self.icerik içine koy."""

    def __init__(self, master, genislik=300):
        super().__init__(master, style="Kart.TFrame")
        self.cv = tk.Canvas(self, width=genislik, highlightthickness=0, borderwidth=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=self.cv.yview)
        self.cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(0, 3), pady=3)
        self.cv.pack(side="left", fill="both", expand=True)
        self.icerik = ttk.Frame(self.cv, style="Kart.TFrame")
        self._pen = self.cv.create_window((0, 0), window=self.icerik, anchor="nw")
        self.icerik.bind("<Configure>", lambda _e: self.cv.configure(
            scrollregion=self.cv.bbox("all")))
        self.cv.bind("<Configure>", lambda e: self.cv.itemconfigure(
            self._pen, width=e.width))
        self.bind_all("<MouseWheel>", self._tekerlek, add="+")
        self.bind_all("<Button-4>", lambda e: self._tekerlek(e, 1), add="+")
        self.bind_all("<Button-5>", lambda e: self._tekerlek(e, -1), add="+")
        _DINLEYICILER.append(self.renk_uygula)
        self.renk_uygula()

    def renk_uygula(self):
        self.cv.configure(bg=renkler()["panel"])

    def _tekerlek(self, e, yon=None):
        try:
            self._tekerlek_ic(e, yon)
        except (tk.TclError, KeyError):
            pass

    def _tekerlek_ic(self, e, yon=None):
        if self.icerik.winfo_height() <= self.cv.winfo_height():
            return
        w = self.winfo_containing(e.x_root, e.y_root)
        while w is not None:
            if w is self:
                adim = yon if yon is not None else (1 if e.delta > 0 else -1)
                self.cv.yview_scroll(-adim, "units")
                return
            w = getattr(w, "master", None)


def modul_etiketi(sinif):
    """Sayfa başlığının üstündeki küçük modül etiketi (ör. MODÜL 02)."""
    try:
        return T("MODÜL") + " %02d" % SAYFALAR.index(sinif)
    except ValueError:
        return T("SİSTEM")


class UstMenu(tk.Canvas):
    """Üstte ortalanmış, hap biçimli cam gezinme çubuğu (tek tuval üzerine çizilir)."""

    def __init__(self, master, ust, alt, komut):
        super().__init__(master, height=px(78), highlightthickness=0, bd=0)
        self.komut = komut
        self.sira = [(a, m) for a, _s, m in list(ust) + list(alt)]
        self.ogeler = {a: m for a, m in self.sira}
        self.aktif = None
        self.ustunde = None
        self._kutular = []              # (x0, x1, anahtar)
        self.bind("<Configure>", lambda _e: self.ciz())
        self.bind("<Motion>", self._hareket)
        self.bind("<Leave>", lambda _e: self._uste(None))
        self.bind("<Button-1>", self._tikla)
        _DINLEYICILER.append(self.ciz)

    def sec(self, anahtar):
        self.aktif = anahtar
        self.ciz()

    def _bul(self, x, y):
        if px(14) <= y <= self.winfo_height() - px(14):
            for x0, x1, a in self._kutular:
                if x0 <= x <= x1:
                    return a
        return None

    def _hareket(self, e):
        self._uste(self._bul(e.x, e.y))

    def _uste(self, a):
        if a != self.ustunde:
            self.ustunde = a
            self.configure(cursor="hand2" if a else "")
            self.ciz()

    def _tikla(self, e):
        a = self._bul(e.x, e.y)
        if a:
            self.komut(a)

    def ciz(self):
        try:
            self._ciz()
        except tk.TclError:
            pass

    def _ciz(self):
        p = renkler()
        W = self.winfo_width()
        if W < px(300):
            return
        self.configure(bg=p["bg"])
        self.delete("all")
        self._kutular = []
        boy = px(48)
        y0 = px(15)
        y1 = y0 + boy
        cy = (y0 + y1) / 2
        pad, punto = px(17), 10
        f_logo = tkfont.Font(family="Georgia", size=14, slant="italic")
        while True:
            f_n = tkfont.Font(family="Segoe UI", size=punto)
            f_k = tkfont.Font(family="Segoe UI Semibold", size=punto)
            genis = [max(f_n.measure(m), f_k.measure(m)) + 2 * pad for _a, m in self.sira]
            logo_w = px(40) + f_logo.measure("Nucleus")
            toplam = px(14) + logo_w + px(22) + sum(genis) + px(2) * len(genis) + px(8)
            if toplam <= W - px(24) or (pad <= px(8) and punto <= 8):
                break
            if pad > px(8):
                pad -= px(2)
            else:
                punto -= 1
        x0 = (W - toplam) / 2
        x1 = x0 + toplam
        cam = karistir(p["bg"], p["yazi"], 0.05)
        _yuvarlak_dikdortgen(self, x0, y0, x1, y1, boy / 2, fill=cam,
                             outline=karistir(p["bg"], p["yazi"], 0.14))
        # logo: yörünge simgesi + italik yazı
        lx = x0 + px(14) + px(15)
        for aci in (0, math.pi / 3, 2 * math.pi / 3):
            self.create_line(*_elips(lx, cy, px(13), px(5), aci, 40), fill=p["vurgu"],
                             width=1.5, smooth=True)
        self.create_oval(lx - px(2.5), cy - px(2.5), lx + px(2.5), cy + px(2.5),
                         fill=p["yazi"], outline="")
        self.create_text(x0 + px(14) + px(40), cy, text="Nucleus", anchor="w",
                         font=f_logo, fill=p["yazi"])
        ax = x0 + px(14) + logo_w + px(10)
        self.create_line(ax, y0 + px(14), ax, y1 - px(14),
                         fill=karistir(p["bg"], p["yazi"], 0.14))
        x = ax + px(12)
        ph = boy - px(10)
        py0 = y0 + px(5)
        for (a, m), g in zip(self.sira, genis):
            if a == self.aktif:
                _yuvarlak_dikdortgen(self, x, py0, x + g, py0 + ph, ph / 2,
                                     fill=p["yazi"], outline="")
                renk, f = p["bg"], f_k
            elif a == self.ustunde:
                _yuvarlak_dikdortgen(self, x, py0, x + g, py0 + ph, ph / 2,
                                     fill=karistir(p["bg"], p["yazi"], 0.10), outline="")
                renk, f = p["yazi"], f_n
            else:
                renk, f = p["soluk"], f_n
            self.create_text(x + g / 2, cy, text=m, font=f, fill=renk)
            self._kutular.append((x, x + g, a))
            x += g + px(2)


class Hap(tk.Canvas):
    """Hap biçimli düğme. gri=False: dolu (açık renk), gri=True: cam görünümlü çerçeveli.
    zemin: düğmenin durduğu yüzeyin palet anahtarı ('panel' ya da 'bg')."""

    def __init__(self, master, metin, komut, gri=False, zemin="panel"):
        self.metin, self.komut, self.gri, self.zemin = metin, komut, gri, zemin
        self._font = tkfont.Font(family="Segoe UI Semibold", size=10)
        super().__init__(master, height=px(42), width=self._font.measure(metin) + px(48),
                         highlightthickness=0, bd=0, cursor="hand2")
        self._uzerinde = False
        self.bind("<Configure>", lambda _e: self.ciz())
        self.bind("<Enter>", lambda _e: self._hover(True))
        self.bind("<Leave>", lambda _e: self._hover(False))
        self.bind("<Button-1>", lambda _e: self.komut())
        _DINLEYICILER.append(self.ciz)

    def _hover(self, v):
        self._uzerinde = v
        self.ciz()

    def ciz(self):
        try:
            W, H = self.winfo_width(), self.winfo_height()
            if W < 10:
                return
            p = renkler()
            self.configure(bg=p[self.zemin])
            self.delete("all")
            if self.gri:
                dolgu = p["gri_hover"] if self._uzerinde else p["giris"]
                cerceve = p["soluk"] if self._uzerinde else p["kenar"]
                yazi = p["yazi"]
            else:
                dolgu = (karistir(p["yazi"], p["bg"], 0.16) if self._uzerinde
                         else p["yazi"])
                cerceve, yazi = dolgu, p["bg"]
            _yuvarlak_dikdortgen(self, 1, 1, W - 1, H - 1, (H - 2) / 2,
                                 fill=dolgu, outline=cerceve)
            self.create_text(W / 2, H / 2, text=self.metin, font=self._font, fill=yazi)
        except tk.TclError:
            pass


class SayfaBasligi(tk.Canvas):
    """Sayfanın üstündeki başlık şeridi: ışık geçişli zemin, modül hapı, ince başlık
    (son kelime italik serif) ve açıklama."""
    YUKSEKLIK = 158

    def __init__(self, master, etiket, baslik, alt=""):
        super().__init__(master, height=px(self.YUKSEKLIK), highlightthickness=0, bd=0)
        self.et, self.bas, self.alt = etiket, baslik, alt
        self.bind("<Configure>", lambda _e: self.ciz())
        _DINLEYICILER.append(self.ciz)

    def ciz(self):
        try:
            self._ciz()
        except tk.TclError:
            pass

    def _ciz(self):
        p = renkler()
        W = self.winfo_width()
        if W < px(200):
            return
        H = px(self.YUKSEKLIK)
        self.configure(bg=p["bg"])
        self.delete("all")
        self.create_image(W / 2, 0, image=aurora_resmi(self, 2000, H, "serit"),
                          anchor="n")
        x = px(34)
        f_e = tkfont.Font(family="Segoe UI Semibold", size=8)
        tw = f_e.measure(self.et)
        _yuvarlak_dikdortgen(self, x, px(22), x + tw + px(34), px(46), px(12),
                             fill=karistir(p["bg"], p["yazi"], 0.06),
                             outline=karistir(p["bg"], p["yazi"], 0.16))
        self.create_oval(x + px(10), px(31), x + px(16), px(37), fill=p["vurgu"],
                         outline="")
        self.create_text(x + px(23), px(34), text=self.et, anchor="w", font=f_e,
                         fill=p["soluk"])
        f1 = tkfont.Font(family="Segoe UI Light", size=26)
        f2 = tkfont.Font(family="Georgia", size=26, slant="italic")
        ilk, _, son = self.bas.rpartition(" ")
        xx = x
        if ilk:
            self.create_text(xx, px(82), text=ilk + " ", anchor="w", font=f1,
                             fill=p["yazi"])
            xx += f1.measure(ilk + " ")
        self.create_text(xx, px(82), text=son, anchor="w", font=f2, fill=p["yazi"])
        if self.alt:
            self.create_text(x, px(112), text=self.alt, anchor="nw", width=W - 2 * x,
                             font=("Segoe UI", 9), fill=p["soluk"])


class Segment(tk.Frame):
    """Yan yana seçenek düğmeleri (ör. Koyu | Açık)."""

    def __init__(self, master, degerler, secili, komut):
        super().__init__(master, bd=0, highlightthickness=0)
        self.secili = secili
        self.komut = komut
        self.etiketler = {}
        for d in degerler:
            lb = tk.Label(self, text=T(d), font=("Segoe UI", 10, "bold"),
                          padx=px(22), pady=px(8), cursor="hand2")
            lb.pack(side="left", padx=(0, 3))
            lb.bind("<Button-1>", lambda _e, d=d: self.sec(d, True))
            self.etiketler[d] = lb
        _DINLEYICILER.append(self.renk_uygula)
        self.renk_uygula()

    def sec(self, d, bildir=False):
        self.secili = d
        self.renk_uygula()
        if bildir and self.komut:
            self.komut(d)

    def renk_uygula(self):
        p = renkler()
        self.configure(bg=p["panel"])
        for d, lb in self.etiketler.items():
            if d == self.secili:
                lb.configure(bg=p["yazi"], fg=p["bg"])
            else:
                lb.configure(bg=p["giris"], fg=p["soluk"])


class RenkSecici(tk.Canvas):
    """Vurgu rengi için yuvarlak renk örnekleri."""

    def __init__(self, master, secili, komut):
        self.boy = px(44)
        super().__init__(master, width=self.boy * len(VURGULAR), height=self.boy,
                         highlightthickness=0, bd=0, cursor="hand2")
        self.secili = secili
        self.komut = komut
        self.bind("<Button-1>", self._tikla)
        _DINLEYICILER.append(self.renk_uygula)
        self.renk_uygula()

    def sec(self, ad):
        self.secili = ad
        self.renk_uygula()

    def _tikla(self, e):
        i = int(e.x // self.boy)
        adlar = list(VURGULAR)
        if 0 <= i < len(adlar):
            self.sec(adlar[i])
            self.komut(adlar[i])

    def renk_uygula(self):
        p = renkler()
        self.configure(bg=p["panel"])
        self.delete("all")
        for i, (ad, renk) in enumerate(VURGULAR.items()):
            cx, cy, r = i * self.boy + self.boy / 2, self.boy / 2, px(14)
            if ad == self.secili:
                self.create_oval(cx - r - px(5), cy - r - px(5), cx + r + px(5),
                                 cy + r + px(5), outline=renk, width=2)
            self.create_oval(cx - r, cy - r, cx + r, cy + r, fill=renk, outline="")
            if ad == self.secili:
                self.create_text(cx, cy, text="✓", fill="white",
                                 font=("Segoe UI", 11, "bold"))


# ------------------------------------------------------------------ Sonuç paneli
class SonucPaneli(Kart):
    """Sonuçları büyük başlık + kutucuklar + tablo olarak gösterir."""

    def __init__(self, master):
        self._son = ("bos", "")
        super().__init__(master)
        self.bos()

    def renk_uygula(self):
        super().renk_uygula()
        self._ciz()

    def bos(self, metin="Değerleri girip «Hesapla» düğmesine bas."):
        self._son = ("bos", T(metin))
        self._ciz()

    def hata(self, metin):
        self._son = ("hata", metin)
        self._ciz()

    def goster(self, baslik, deger, birim, kutular=(), tablo=None, uyarilar=(),
               nuklit=None):
        kutular = [(T(a), b) for a, b in kutular]
        if tablo:
            tablo = (tuple(T(h) for h in tablo[0]), tablo[1])
        self._son = ("sonuc", T(baslik), deger, birim, kutular, tablo,
                     list(uyarilar), nuklit)
        self._ciz()

    def _ciz(self):
        p = renkler()
        ic = self.ic
        for w in ic.winfo_children():
            w.destroy()
        tur = self._son[0]

        if tur == "bos":
            kap = tk.Frame(ic, bg=p["panel"])
            kap.pack(fill="x", padx=px(24), pady=px(26))
            tk.Label(kap, text=T("Sonuçlar burada görünecek"), bg=p["panel"],
                     fg=p["yazi"], font=("Segoe UI", 12, "bold")).pack(anchor="w")
            tk.Label(kap, text=self._son[1], bg=p["panel"], fg=p["soluk"],
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))
            return

        if tur == "hata":
            kap = tk.Frame(ic, bg=p["panel"])
            kap.pack(fill="x", padx=px(24), pady=px(22))
            tk.Frame(kap, bg=TEHLIKE, width=4).pack(side="left", fill="y")
            tk.Label(kap, text="⚠  " + self._son[1], bg=p["panel"], fg=TEHLIKE,
                     font=("Segoe UI", 11, "bold"), justify="left",
                     wraplength=px(640)).pack(side="left", padx=(px(14), 0))
            return

        _, baslik, deger, birim, kutular, tablo, uyarilar, nuklit = self._son
        ust = tk.Frame(ic, bg=p["panel"])
        ust.pack(fill="x", padx=px(24), pady=(px(20), px(8)))
        tk.Frame(ust, bg=p["vurgu"], width=4).pack(side="left", fill="y")
        metin = tk.Frame(ust, bg=p["panel"])
        metin.pack(side="left", padx=(px(14), 0))
        tk.Label(metin, text=tr_buyuk(baslik), bg=p["panel"], fg=p["soluk"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        satir = tk.Frame(metin, bg=p["panel"])
        satir.pack(anchor="w")
        if nuklit:
            # tahtadaki gösterim:  [BE/A]   A/Z X  =  [değer]  MeV/nuc
            Zn, An, sem = nuklit
            kb = tk.Frame(satir, bg=p["panel"], highlightthickness=2,
                          highlightbackground=p["vurgu"])
            kb.pack(side="left", pady=(px(8), 0))
            tk.Label(kb, text="BE/A", bg=p["panel"], fg=p["yazi"], padx=px(12),
                     pady=px(6), font=("Segoe UI", 16, "bold")).pack()
            nk = tk.Frame(satir, bg=p["panel"])
            nk.pack(side="left", padx=(px(18), px(6)), pady=(px(8), 0))
            tk.Label(nk, text=str(An), bg=p["panel"], fg=p["soluk"],
                     font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="e")
            tk.Label(nk, text=str(Zn), bg=p["panel"], fg=p["soluk"],
                     font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="e")
            tk.Label(nk, text=sem, bg=p["panel"], fg=p["vurgu"],
                     font=("Segoe UI", 24, "bold")).grid(row=0, column=1, rowspan=2,
                                                          padx=(px(2), 0))
            tk.Label(satir, text="=", bg=p["panel"], fg=p["soluk"],
                     font=("Segoe UI", 20)).pack(side="left", padx=(px(4), px(10)),
                                                 pady=(px(8), 0))
            vb = tk.Frame(satir, bg=p["panel"], highlightthickness=2,
                          highlightbackground=p["yazi"])
            vb.pack(side="left", pady=(px(8), 0))
            tk.Label(vb, text=deger, bg=p["panel"], fg=p["yazi"], padx=px(14),
                     pady=px(4), font=("Segoe UI Light", 26)).pack()
            tk.Label(satir, text="  " + birim, bg=p["panel"], fg=p["yazi"],
                     font=("Segoe UI", 13, "bold")).pack(side="left",
                                                         pady=(px(22), 0))
        else:
            tk.Label(satir, text=deger, bg=p["panel"], fg=p["yazi"],
                     font=("Segoe UI Light", 30)).pack(side="left")
            tk.Label(satir, text="  " + birim, bg=p["panel"], fg=p["soluk"],
                     font=("Segoe UI", 12)).pack(side="left", pady=(px(12), 0))

        if kutular:
            sut = 3
            g = tk.Frame(ic, bg=p["panel"])
            g.pack(fill="x", padx=px(24), pady=(px(6), px(2)))
            for c in range(sut):
                g.columnconfigure(c, weight=1, uniform="k")
            for i, (et, dg) in enumerate(kutular):
                t = tk.Frame(g, bg=p["giris"])
                t.grid(row=i // sut, column=i % sut, sticky="nsew",
                       padx=(0 if i % sut == 0 else px(8), 0), pady=px(4))
                tk.Label(t, text=et, bg=p["giris"], fg=p["soluk"], anchor="w",
                         font=("Segoe UI", 9)).pack(fill="x", padx=px(12),
                                                    pady=(px(9), 0))
                tk.Label(t, text=dg, bg=p["giris"], fg=p["yazi"], anchor="w",
                         font=("Consolas", 11, "bold")).pack(fill="x", padx=px(12),
                                                             pady=(1, px(9)))

        if tablo:
            baslıklar, satirlar = tablo
            tf = tk.Frame(ic, bg=p["panel"])
            tf.pack(fill="x", padx=px(24), pady=(px(10), px(2)))
            for c in range(len(baslıklar)):
                tf.columnconfigure(c, weight=1)
            for c, b in enumerate(baslıklar):
                tk.Label(tf, text=b, bg=p["panel"], fg=p["soluk"],
                         font=("Segoe UI", 9, "bold"),
                         anchor="w" if c == 0 else "e").grid(row=0, column=c,
                                                             sticky="ew", pady=(0, 4))
            tk.Frame(tf, bg=p["izgara"], height=1).grid(
                row=1, column=0, columnspan=len(baslıklar), sticky="ew")
            for r, sat in enumerate(satirlar, 2):
                for c, v in enumerate(sat):
                    tk.Label(tf, text=v, bg=p["panel"], fg=p["yazi"],
                             font=("Consolas", 10),
                             anchor="w" if c == 0 else "e").grid(
                        row=r, column=c, sticky="ew", pady=2)

        for u in uyarilar:
            tk.Label(ic, text="⚠  " + u, bg=p["panel"], fg=p["uyari"], justify="left",
                     anchor="w", wraplength=px(700), font=("Segoe UI", 9)).pack(
                fill="x", padx=px(24), pady=(px(6), 0))
        tk.Frame(ic, bg=p["panel"], height=px(16)).pack()


# ------------------------------------------------------------------ Grafik paneli
def _tikler(lo, hi, hedef=6):
    aralik = hi - lo
    if aralik <= 0:
        return [lo]
    ham = aralik / hedef
    us = 10 ** math.floor(math.log10(ham))
    adim = 10 * us
    for m in (1, 2, 5, 10):
        if ham <= m * us:
            adim = m * us
            break
    k0 = math.ceil(lo / adim - 1e-9)
    k1 = math.floor(hi / adim + 1e-9)
    return [k * adim for k in range(k0, k1 + 1)]


def _etiket(v):
    if abs(v) < 1e-12:
        return "0"
    if abs(v) >= 1e5 or abs(v) < 1e-3:
        return f"{v:.2e}"
    return f"{v:.6g}"


class GrafikPaneli(tk.Canvas):
    """Kütüphanesiz grafik (Canvas): çizgi + alan dolgusu veya çubuk, üzerine
    gelince değer balonu gösterir."""

    def __init__(self, master):
        super().__init__(master, highlightthickness=0, height=px(300),
                         cursor="crosshair")
        self._veri = None
        self._pts = []
        self._esik = 20
        self._f1 = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self._f2 = tkfont.Font(family="Segoe UI", size=9)
        self.bind("<Configure>", lambda _e: self.yeniden_ciz())
        self.bind("<Motion>", self._hareket)
        self.bind("<Leave>", lambda _e: self.delete("ipucu"))
        _DINLEYICILER.append(self.yeniden_ciz)

    def ciz(self, x, y, xetiket, yetiket, baslik, tur="cizgi", etiketler=None,
            nokta=None, nokta_ad="Sonuç", isaretci=None, noktalar_ad=None):
        """
        tur: "cizgi" (sürekli eğri) | "cubuk" (kategorik çubuklar, etiketler gerekir)
        nokta: (x, y) -> grafikte turuncu ile vurgulanacak sonuç noktası
        noktalar_ad: çizgi grafiğinde her nokta için balon başlığı (isteğe bağlı)
        """
        self._veri = dict(x=list(x), y=list(y), xe=T(xetiket), ye=T(yetiket), b=T(baslik),
                          tur=tur, et=etiketler, n=nokta, na=T(nokta_ad), i=isaretci,
                          pn=noktalar_ad)
        self.yeniden_ciz()

    @staticmethod
    def _aralik(degerler, bosluk, alt_sifir=True):
        lo, hi = min(degerler), max(degerler)
        if lo == hi:
            pay = abs(lo) * 0.1 or 1.0
            return lo - pay, hi + pay
        pay = (hi - lo) * bosluk
        yeni_lo = lo - pay
        if alt_sifir and lo >= 0:
            yeni_lo = max(0.0, yeni_lo)
        return yeni_lo, hi + pay

    def yeniden_ciz(self):
        self._ciz_ic()
        self._maskele()

    def _maskele(self):
        r = renkler()
        W, H = self.winfo_width(), self.winfo_height()
        if W < px(60) or H < px(60):
            return
        self.delete("maske")
        self.create_rectangle(0, 0, W - 1, H - 1, outline=r["kenar"], tags="maske")
        rr = px(16)
        for cx, cy, sx, sy in ((0, 0, 1, 1), (W - 1, 0, -1, 1),
                               (0, H - 1, 1, -1), (W - 1, H - 1, -1, -1)):
            kose_maskesi(self, cx, cy, sx, sy, rr, r["bg"], r["kenar"])

    def _ciz_ic(self):
        r = renkler()
        self.configure(bg=r["panel"], highlightbackground=r["kenar"],
                       highlightcolor=r["kenar"])
        self.delete("all")
        self._pts = []
        W, H = self.winfo_width(), self.winfo_height()
        if W < px(200) or H < px(140):
            return
        d = self._veri
        if d is None:
            self.create_text(W / 2, H / 2 - 10, text=T("Sonuç grafiği burada görünecek"),
                             fill=r["yazi"], font=("Segoe UI", 12, "bold"))
            self.create_text(W / 2, H / 2 + 14,
                             text=T("Hesapla'ya bastığında eğri ve değerler çizilir"),
                             fill=r["soluk"], font=("Segoe UI", 10))
            return

        xs, ys = d["x"], d["y"]
        cubuk = d["tur"] == "cubuk"
        if cubuk:
            xmin, xmax = -0.5, len(xs) - 0.5
            ymin, ymax = 0.0, (max(ys) * 1.22 if max(ys) > 0 else 1.0)
        else:
            px_hepsi = xs + ([d["n"][0]] if d["n"] else [])
            py_hepsi = ys + ([d["n"][1]] if d["n"] else [])
            xmin, xmax = self._aralik(px_hepsi, 0.05)
            ymin, ymax = self._aralik(py_hepsi, 0.10)

        sol, sag, ust, alt = px(84), px(30), px(66), px(56)
        x0, x1, y0, y1 = sol, W - sag, ust, H - alt

        def PX(v):
            return x0 + (v - xmin) / (xmax - xmin) * (x1 - x0)

        def PY(v):
            return y1 - (v - ymin) / (ymax - ymin) * (y1 - y0)

        yazi_k = ("Segoe UI", 9)
        # --- başlık + y ekseni adı (üstte, yatay)
        self.create_text(px(24), px(22), text=d["b"], anchor="w", fill=r["yazi"],
                         font=("Segoe UI", 12, "bold"))
        self.create_text(px(24), px(44), text=d["ye"], anchor="w", fill=r["soluk"],
                         font=("Segoe UI", 9))

        # --- yatay ızgara + y etiketleri
        for v in _tikler(ymin, ymax):
            self.create_line(x0, PY(v), x1, PY(v), fill=r["izgara"], dash=(3, 5))
            self.create_text(x0 - px(10), PY(v), text=_etiket(v), anchor="e",
                             fill=r["soluk"], font=yazi_k)
        self.create_line(x0, y1, x1, y1, fill=r["soluk"])

        # --- x etiketleri
        if cubuk:
            for i in range(len(xs)):
                self.create_text(PX(i), y1 + px(16), text=d["et"][i], fill=r["yazi"],
                                 font=yazi_k)
        else:
            for v in _tikler(xmin, xmax):
                self.create_line(PX(v), y1, PX(v), y1 + px(4), fill=r["soluk"])
                self.create_text(PX(v), y1 + px(16), text=_etiket(v), fill=r["soluk"],
                                 font=yazi_k)
        self.create_text((x0 + x1) / 2, H - px(14), text=d["xe"], fill=r["soluk"],
                         font=("Segoe UI", 9))

        # --- veri
        if cubuk:
            slot = (x1 - x0) / len(xs)
            bw = min(px(90), slot * 0.56)
            for i, v in enumerate(xs):
                bx, by = PX(i), PY(ys[i])
                self.create_rectangle(bx - bw / 2, by, bx + bw / 2, y1,
                                      fill=r["vurgu"], outline="")
                self.create_text(bx, by - px(11), text=_etiket(ys[i]),
                                 fill=r["yazi"], font=("Segoe UI", 9, "bold"))
                self._pts.append((bx, by, d["et"][i], f"{_etiket(ys[i])}"))
            self._esik = slot / 2
        else:
            if len(xs) >= 2:
                koord = []
                for a, b in zip(xs, ys):
                    koord += [PX(a), PY(b)]
                alan = koord + [PX(xs[-1]), y1, PX(xs[0]), y1]
                self.create_polygon(*alan, fill=karistir(r["panel"], r["vurgu"], 0.15),
                                    outline="")
                self.create_line(*koord, fill=r["vurgu"], width=2.5,
                                 capstyle="round", joinstyle="round")
            isaret = d["i"] if d["i"] is not None else len(xs) <= 30
            for k, (a, b) in enumerate(zip(xs, ys)):
                if isaret or len(xs) < 2:
                    self.create_oval(PX(a) - 4, PY(b) - 4, PX(a) + 4, PY(b) + 4,
                                     fill=r["panel"], outline=r["vurgu"], width=2)
                bas = d["pn"][k] if d["pn"] else _etiket(a)
                alt_satir = (f"{_etiket(b)}" if d["pn"] else
                             f"{d['ye']}: {_etiket(b)}")
                if d["pn"]:
                    alt_satir = f"A = {_etiket(a)}   ·   {_etiket(b)}"
                self._pts.append((PX(a), PY(b), bas, alt_satir))
            self._esik = max(px(18), (x1 - x0) / max(len(xs), 1) / 2)

        if d["n"]:
            a, b = d["n"]
            cx, cy = PX(a), PY(b)
            self.create_oval(cx - 13, cy - 13, cx + 13, cy + 13,
                             fill=karistir(r["panel"], NOKTA_RENGI, 0.28), outline="")
            self.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=NOKTA_RENGI,
                             outline=r["panel"], width=2)
            if d["na"]:
                yon = "e" if cx < x1 - px(150) else "w"
                dx = px(18) if yon == "e" else -px(18)
                self.create_text(cx + dx, cy - px(14), text=d["na"], anchor=yon,
                                 fill=NOKTA_RENGI, font=("Segoe UI", 10, "bold"))

    # --- üzerine gelince değer balonu
    def _hareket(self, e):
        self.delete("ipucu")
        if not self._pts:
            return
        p_ = min(self._pts, key=lambda q: abs(q[0] - e.x))
        if abs(p_[0] - e.x) > self._esik:
            return
        r = renkler()
        cx, cy, t1, t2 = p_
        W = self.winfo_width()
        self.create_line(cx, px(60), cx, self.winfo_height() - px(56),
                         fill=r["soluk"], dash=(2, 4), tags="ipucu")
        self.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=r["vurgu"],
                         outline=r["panel"], width=2, tags="ipucu")
        w = max(self._f1.measure(t1), self._f2.measure(t2)) + px(26)
        h = px(46)
        bx = cx + px(14)
        if bx + w > W - 4:
            bx = cx - px(14) - w
        by = cy - h - px(12)
        if by < 4:
            by = cy + px(14)
        bg = karistir(r["panel"], r["yazi"], 0.93)
        _yuvarlak_dikdortgen(self, bx, by, bx + w, by + h, px(8), fill=bg,
                             outline="", tags="ipucu")
        self.create_text(bx + px(13), by + px(14), text=t1, anchor="w", fill=r["panel"],
                         font=self._f1, tags="ipucu")
        self.create_text(bx + px(13), by + px(32), text=t2, anchor="w",
                         fill=karistir(r["panel"], r["soluk"], 0.35), font=self._f2,
                         tags="ipucu")


# =============================================================================
#  SAYFALAR
# =============================================================================
class HesapSayfasi(ttk.Frame):
    BASLIK = "Sayfa"
    MENU = "Sayfa"
    SIMGE = "•"
    ALT = ""
    SOL_GENISLIK = 340

    def __init__(self, master, ayar):
        super().__init__(master)
        self.ayar = ayar
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        SayfaBasligi(self, modul_etiketi(type(self)), T(self.BASLIK),
                     T(self.ALT) if self.ALT else "").grid(row=0, column=0, sticky="ew")

        govde = ttk.Frame(self)
        govde.grid(row=1, column=0, sticky="nsew", padx=px(30), pady=(0, px(26)))
        govde.columnconfigure(1, weight=1)
        govde.rowconfigure(0, weight=1)

        kart = Kart(govde)
        kart.grid(row=0, column=0, sticky="ns", padx=(0, px(18)))
        kap = KaydirmaliCerceve(kart.ic, genislik=px(self.SOL_GENISLIK))
        kap.pack(fill="both", expand=True)
        self.sol = kap.icerik

        sag = ttk.Frame(govde)
        sag.grid(row=0, column=1, sticky="nsew")
        sag.columnconfigure(0, weight=1)
        sag.rowconfigure(1, weight=1)
        self.sonuc = SonucPaneli(sag)
        self.sonuc.grid(row=0, column=0, sticky="ew", pady=(0, px(18)))
        self.grafik = GrafikPaneli(sag)
        self.grafik.grid(row=1, column=0, sticky="nsew")

        self.arayuz_olustur()

    # --- alt sınıfların kullanacağı yardımcılar
    def baslik(self, metin):
        ttk.Label(self.sol, text=T(metin), style="KartBaslik.TLabel").pack(
            fill="x", padx=px(20), pady=(px(18), 2))

    def aciklama(self, metin):
        ttk.Label(self.sol, text=T(metin), style="Ipucu.TLabel", justify="left",
                  wraplength=px(self.SOL_GENISLIK - 70)).pack(
            fill="x", padx=px(20), pady=(0, 2))

    def formul(self, metin):
        ttk.Label(self.sol, text=metin, style="Formul.TLabel", justify="left").pack(
            fill="x", padx=px(20), pady=(px(10), 0))

    def alan(self, etiket, varsayilan=""):
        ttk.Label(self.sol, text=T(etiket), style="Etiket.TLabel").pack(
            fill="x", padx=px(20), pady=(px(14), 0))
        e = ttk.Entry(self.sol)
        e.pack(fill="x", padx=px(20), pady=(px(5), 0))
        e.insert(0, str(varsayilan))
        e.bind("<Return>", lambda _e: self.hesapla_tikla())
        return e

    def secenek(self, etiket, degerler, varsayilan=None, komut=None):
        ttk.Label(self.sol, text=T(etiket), style="Etiket.TLabel").pack(
            fill="x", padx=px(20), pady=(px(14), 0))
        c = Combo(self.sol, degerler, varsayilan or degerler[0], komut)
        c.pack(fill="x", padx=px(20), pady=(px(5), 0))
        return c

    def buton(self, metin, komut, gri=False, son=False):
        b = Hap(self.sol, T(metin), komut, gri=gri, zemin="panel")
        b.pack(fill="x", padx=px(20), pady=(px(12), px(22) if son else 0))
        return b

    @staticmethod
    def doldur(giris, deger):
        giris.delete(0, "end")
        giris.insert(0, str(deger))

    def f(self, x):
        return fmt(x, self.ayar.al("ondalik"))

    def anlat(self, olay, **kw):
        """Anlatıcıya bir olay bildirir (anlatıcı kapalıysa hiçbir şey olmaz)."""
        a = getattr(self.winfo_toplevel(), "anlatici", None)
        if a is not None:
            a.olay(olay, **kw)

    def hesapla_tikla(self):
        try:
            self.hesapla()
        except HesapHatasi as e:
            self.sonuc.hata(str(e))
            self.anlat("hata")

    def arayuz_olustur(self):
        raise NotImplementedError

    def hesapla(self):
        raise NotImplementedError


# ------------------------------------------------------ 1) Atomik kütle
class AtomikKutleSayfasi(HesapSayfasi):
    BASLIK = "Ortalama Atomik Kütle"
    MENU = "Atomik Kütle"
    SIMGE = "⚛"
    ALT = "İzotopların bulunurluklarına göre elementin ortalama atomik kütlesi."
    SOL_GENISLIK = 470

    def arayuz_olustur(self):
        self.baslik("İzotop tablosu")
        self.aciklama("Her izotop için ad, proton, nötron ve bulunurluk (%) gir. "
                      "İzotop kütlesi kütle numarasına (A = p + n) eşit alınır.")
        self.tablo = ttk.Frame(self.sol, style="Kart.TFrame")
        self.tablo.pack(fill="x", padx=px(16), pady=(px(8), 0))
        for c, t in enumerate(("İzotop adı", "Proton", "Nötron", "Bulunurluk %")):
            ttk.Label(self.tablo, text=T(t), style="Etiket.TLabel").grid(
                row=0, column=c, padx=3, sticky="w")
        self.satirlar = []
        self.satir_ekle()
        self.satir_ekle()
        self.buton("+  İzotop ekle", self.satir_ekle, gri=True)
        self.buton("−  Son izotopu sil", self.satir_sil, gri=True)
        self.buton("Örnek yükle (Klor)", self.ornek, gri=True)
        self.buton("Hesapla", self.hesapla_tikla, son=True)

    def satir_ekle(self, deger=("", "", "", "")):
        r = len(self.satirlar) + 1
        girdiler = []
        for c, (w, v) in enumerate(zip((10, 6, 6, 10), deger)):
            e = ttk.Entry(self.tablo, width=w)
            e.grid(row=r, column=c, padx=3, pady=3)
            e.insert(0, str(v))
            e.bind("<Return>", lambda _e: self.hesapla_tikla())
            girdiler.append(e)
        self.satirlar.append(girdiler)

    def satir_sil(self):
        if len(self.satirlar) > 1:
            for e in self.satirlar.pop():
                e.destroy()

    def ornek(self):
        for g in self.satirlar:
            for e in g:
                e.destroy()
        self.satirlar = []
        self.satir_ekle(("Cl-35", 17, 18, 75.76))
        self.satir_ekle(("Cl-37", 17, 20, 24.24))

    def hesapla(self):
        izotoplar = []
        for no, g in enumerate(self.satirlar, 1):
            ad, p, n, y = (e.get().strip() for e in g)
            if not (ad or p or n or y):
                continue
            izotoplar.append({
                "isim": ad or f"izotop-{no}",
                "p": tamsayi(p, f"{no}. satır proton"),
                "n": tamsayi(n, f"{no}. satır nötron"),
                "yuzde": sayi(y, f"{no}. satır bulunurluk", negatif_olmasin=True),
            })
        s = hs_ortalama(izotoplar)
        kutular = [("Toplam bulunurluk", f"%{s['toplam']:.4f}"),
                   ("İzotop sayısı", str(len(s["satirlar"])))]
        tablo = (("İzotop", "A", "Bulunurluk %", "Katkı (u)"),
                 [(ad, str(A), f"{y:.4f}", self.f(k)) for ad, A, y, k in s["satirlar"]])
        self.sonuc.goster("Ortalama atomik kütle", self.f(s["ortalama"]),
                          "u  (g/mol)", kutular, tablo, s["uyarilar"])
        self.grafik.ciz(list(range(len(s["satirlar"]))),
                        [r[2] for r in s["satirlar"]], "İzotop", "Bulunurluk (%)",
                        "İzotop bulunurluk dağılımı", tur="cubuk",
                        etiketler=[r[0] for r in s["satirlar"]])
        self.anlat("ok_atomik", v=self.f(s["ortalama"]))


def hs_ortalama(izotoplar):
    return ortalama_atomik_kutle(izotoplar)


# ------------------------------------------- 2) Atom / molekül yoğunluğu
class YogunlukSayfasi(HesapSayfasi):
    BASLIK = "Atom / Molekül Yoğunluğu"
    MENU = "Yoğunluk"
    SIMGE = "⬢"
    ALT = "Kütlece yoğunluktan birim hacimdeki atom sayısına geçiş."

    def arayuz_olustur(self):
        self.baslik("Girdiler")
        self.formul("N = ρ · N_A / M")
        self.rho = self.alan("Kütlece yoğunluk ρ (g/cm³)", "19.05")
        self.M = self.alan("Molar kütle M (g/mol)", "238.03")
        self.buton("Hesapla", self.hesapla_tikla, son=True)

    def hesapla(self):
        rho = sayi(self.rho.get(), "Yoğunluk", pozitif=True)
        M = sayi(self.M.get(), "Molar kütle", pozitif=True)
        s = atom_yogunlugu(rho, M)
        self.sonuc.goster("Atom / molekül yoğunluğu", self.f(s["N_cm3"]), "1/cm³",
                          [("N (1/m³)", self.f(s["N_m3"])),
                           ("Molar yoğunluk (mol/cm³)", self.f(s["mol_cm3"])),
                           ("Tanecik başına kütle (g)", self.f(s["kutle_tanecik_g"]))])
        self.grafik.ciz(s["x"], s["y"], "ρ  (g/cm³)", "N  (1/cm³)",
                        "Yoğunluğa göre atom/molekül yoğunluğu",
                        nokta=(rho, s["N_cm3"]), nokta_ad="Girilen değer")
        self.anlat("ok_yogun", v=self.f(s["N_cm3"]))


# -------------------------------------------------------- 3) Molar kütle
class MolarKutleSayfasi(HesapSayfasi):
    BASLIK = "Molar Kütle"
    MENU = "Molar Kütle"
    SIMGE = "⚗"
    ALT = "Kimyasal formülden molar kütle ve element katkıları."

    def arayuz_olustur(self):
        self.baslik("Girdiler")
        self.aciklama("Formül örnekleri: H2O, UO2, Ca(OH)2, Al2(SO4)3")
        self.formul_g = self.alan("Kimyasal formül", "UO2")
        self.miktar = self.alan("Numune kütlesi (g) — isteğe bağlı")
        self.buton("Hesapla", self.hesapla_tikla, son=True)

    def hesapla(self):
        m_txt = self.miktar.get().strip()
        miktar = sayi(m_txt, "Numune kütlesi", pozitif=True) if m_txt else None
        s = molar_kutle(self.formul_g.get(), miktar)
        kutular = []
        if miktar is not None:
            kutular = [("Mol sayısı (mol)", self.f(s["mol"])),
                       ("Molekül sayısı", self.f(s["molekul"]))]
        tablo = (("Element", "Adet", "Atom kütlesi", "Katkı", "%"),
                 [(e, str(k), f"{ak:.4f}", f"{kat:.3f}", f"{y:.2f}")
                  for e, k, ak, kat, y in s["satirlar"]])
        self.sonuc.goster("Molar kütle", self.f(s["M"]), "g/mol", kutular, tablo)
        sat = s["satirlar"]
        self.grafik.ciz(list(range(len(sat))), [r[3] for r in sat], "Element",
                        "Katkı (g/mol)", "Elementlerin molar kütleye katkısı",
                        tur="cubuk", etiketler=[r[0] for r in sat])
        self.anlat("ok_molar", f=self.formul_g.get().strip(), v=self.f(s["M"]))


# ------------------------------------------------------ 4) Bağlanma enerjisi
class BaglanmaSayfasi(HesapSayfasi):
    BASLIK = "Bağlanma Enerjisi"
    MENU = "Bağlanma Enerjisi"
    SIMGE = "⚡"
    ALT = ("Tüm elementler (Z = 1–118) için kütle kusurundan toplam ve "
           "nükleon başına bağlanma enerjisi.")
    ODAK = "toplam"                  # sonuçta öne çıkan değer: "toplam" | "ba"
    FORMUL = "Δm = Z·m(H-1) + N·mₙ − M\nB = Δm · c²   (1 u = 931,494 MeV)"

    def arayuz_olustur(self):
        self._tahmin = None          # (Z, N, M): kütle model ile tahmin edildiyse
        self.baslik("Çekirdek bilgileri")
        self.formul(self.FORMUL)
        self.aciklama("Element ve kütle numarasını seç; Z, N ve M otomatik dolar. "
                      "Deneysel kütlesi tabloda olmayan çekirdeklerde kütle "
                      "Weizsäcker formülüyle tahmin edilir. İstersen aşağıdaki "
                      "kutulara kendi değerlerini de yazabilirsin.")
        self.elem = self.secenek("Element", ELEMENT_SECENEKLERI,
                                 ELEMENT_SECENEKLERI[1], self._element_sec)
        self.kno = self.secenek("Kütle numarası A",
                                [str(A) for A, _t in izotop_listesi(2)], "4",
                                self._a_sec)
        self.Z = self.alan("Proton sayısı Z", "2")
        self.N = self.alan("Nötron sayısı N", "2")
        self.tur = self.secenek("Girilecek kütle türü", KUTLE_TURLERI,
                                KUTLE_TURLERI[0])
        self.M = self.alan("Kütle M (u)", "4.00260325413")
        self.buton("Hesapla", self.hesapla_tikla, son=True)

    @staticmethod
    def _z_of(metin):
        return int(metin.split(" ")[0])

    def _element_sec(self, metin):
        Z = self._z_of(metin)
        liste = izotop_listesi(Z)
        self.kno["values"] = [str(A) for A, _t in liste]
        A = varsayilan_izotop(Z, liste)
        self.kno.set(str(A))
        self._cekirdek_doldur(Z, A)

    def _a_sec(self, metin):
        self._cekirdek_doldur(self._z_of(self.elem.get()), int(metin))

    def _cekirdek_doldur(self, Z, A, hesapla=True):
        b = izotop_bilgi(Z, A)
        self.doldur(self.Z, Z)
        self.doldur(self.N, A - Z)
        self.doldur(self.M, f"{b['M']:.10f}")
        self.tur.set(KUTLE_TURLERI[0])
        self._tahmin = None if b["deneysel"] else (Z, A - Z, float(self.M.get()))
        if hesapla:
            self.hesapla_tikla()

    def cekirdek_yukle(self, Z, A):
        """Başka sekmeden (İzotop Tablosu) gelen çekirdeği yükler ve hesaplar."""
        for metin in ELEMENT_SECENEKLERI:
            if self._z_of(metin) == Z:
                self.elem.set(metin)
                break
        liste = izotop_listesi(Z)
        self.kno["values"] = [str(a) for a, _t in liste]
        self.kno.set(str(A))
        self._cekirdek_doldur(Z, A)

    def hesapla(self):
        Z = tamsayi(self.Z.get(), "Proton sayısı")
        N = tamsayi(self.N.get(), "Nötron sayısı")
        M = sayi(self.M.get(), "Kütle", pozitif=True)
        if not 1 <= Z <= 118:
            raise HesapHatasi("Proton sayısı 1 ile 118 arasında olmalı.")
        s = baglanma_enerjisi(Z, N, M, self.tur.get())
        if (self._tahmin is not None and self._tahmin[:2] == (Z, N)
                and abs(self._tahmin[2] - M) < 1e-9):
            s["uyarilar"].append(
                "Bu çekirdeğin deneysel kütlesi tabloda yok; kütle Weizsäcker "
                "formülüyle TAHMİN edildi. Sonuç orta/ağır çekirdeklerde yaklaşık %1, "
                "hafif çekirdeklerde birkaç MeV hatalı olabilir. Kesin değer için "
                "AME2020 kütlesini M kutusuna kendin yaz.")
        kutular = [("Kütle numarası A", str(s["A"])),
                   ("Nükleonların toplam kütlesi (u)", self.f(s["toplam"])),
                   ("Girilen kütle M (u)", self.f(M)),
                   ("Kütle kusuru Δm (u)", self.f(s["dm"])),
                   ("Kütle kusuru Δm (kg)", self.f(s["dm_kg"])),
                   ("Toplam B (joule)", self.f(s["B_J"]))]
        if self.ODAK == "ba":
            kutular.insert(0, ("Toplam bağlanma enerjisi B (MeV)", self.f(s["B"])))
            self.sonuc.goster("Nükleon başına bağlanma enerjisi (BE/A)",
                              self.f(s["B_A"]), "MeV/nuc", kutular,
                              None, s["uyarilar"], nuklit=(Z, s["A"], Z_SEMBOL[Z]))
        else:
            self.sonuc.goster("Toplam bağlanma enerjisi", self.f(s["B"]), "MeV",
                              kutular, None, s["uyarilar"])
        # grafik: bilinen çekirdeklerde B/A eğrisi + senin çekirdeğin
        self.grafik.ciz([e[0] for e in s["egri"]], [e[1] for e in s["egri"]],
                        "Kütle numarası A", "Nükleon başına bağlanma enerjisi (MeV)",
                        "Bağlanma enerjisi eğrisi  (B / A)",
                        nokta=(s["A"], s["B_A"]),
                        nokta_ad=f"{T('Senin çekirdeğin')}: {self.f(s['B_A'])} MeV/nuc",
                        noktalar_ad=[e[2] for e in s["egri"]], isaretci=True)
        nuk = f"{Z_SEMBOL[Z]}-{s['A']}"
        if self.ODAK == "ba":
            self.anlat("ok_ba", s=nuk, v=self.f(s["B_A"]))
        else:
            self.anlat("ok_be", s=nuk, v=self.f(s["B"]))


class NukleonBasinaSayfasi(BaglanmaSayfasi):
    """Ayrı sekme: aynı girdilerle nükleon başına bağlanma enerjisi (BE/A)."""
    BASLIK = "Nükleon Başına BE/A"
    MENU = "Nükleon Başına BE/A"
    SIMGE = "⚖"
    ALT = ("Kütle kusurundan toplam bağlanma enerjisini bulur ve kütle numarasına "
           "bölerek nükleon başına değeri (BE/A) verir.")
    ODAK = "ba"
    FORMUL = ("BE/A = B / A = Δm · c² / A\nΔm = Z·m(H-1) + N·mₙ − M\n"
              "(1 u = 931,494 MeV)")

    def arayuz_olustur(self):
        self._tahmin = None
        self._son_giris = (26, 56)
        self.baslik("Çekirdek bilgileri")
        self.formul(self.FORMUL)
        self.aciklama("Elementi (sembol, ad ya da Z) ve kütle numarasını kendin yaz; "
                      "Z, N ve M otomatik dolar. Deneysel kütlesi tabloda olmayan "
                      "çekirdeklerde kütle Weizsäcker formülüyle tahmin edilir. "
                      "İstersen aşağıdaki kutulara kendi değerlerini de yazabilirsin.")
        self.elem = self.alan("Element", "Fe")
        self.kno = self.alan("Kütle numarası A", "56")
        self.Z = self.alan("Proton sayısı Z", "26")
        self.N = self.alan("Nötron sayısı N", "30")
        self.tur = self.secenek("Girilecek kütle türü", KUTLE_TURLERI,
                                KUTLE_TURLERI[0])
        self.M = self.alan("Kütle M (u)", f"{izotop_bilgi(26, 56)['M']:.10f}")
        self.buton("Hesapla", self.hesapla_tikla, son=True)

    @staticmethod
    def _element_coz(metin):
        """Sembol (Fe, fe), Türkçe ad (Demir) ya da Z numarası -> Z."""
        m = metin.strip()
        if not m:
            raise HesapHatasi("Element boş: bir sembol (Fe), ad (Demir) ya da Z yaz.")
        if m.isdigit():
            if not 1 <= int(m) <= 118:
                raise HesapHatasi("Z 1 ile 118 arasında olmalı.")
            return int(m)
        if m.capitalize() in SEMBOL_Z:
            return SEMBOL_Z[m.capitalize()]
        norm = m.replace("İ", "i").replace("I", "ı").lower()
        for z, ad in ELEMENT_ADI.items():
            if ad.replace("İ", "i").replace("I", "ı").lower() == norm:
                return z
        raise HesapHatasi(f"'{m}' diye bir element bulunamadı. Sembol (Fe), "
                          "ad (Demir) ya da proton sayısı (26) yazabilirsin.")

    def hesapla(self):
        Z = self._element_coz(self.elem.get())
        A_metin = self.kno.get().strip()
        lo, hi = izotop_araligi(Z)
        try:
            A_giris = int(A_metin)
        except ValueError:
            A_giris = None
        # Element değiştiyse ve eski A bu elemente uymuyorsa (ör. U için 56),
        # A'yı elementin varsayılan izotopuna otomatik çek.
        if Z != self._son_giris[0] and (A_giris is None or not lo <= A_giris <= hi):
            self.doldur(self.kno, varsayilan_izotop(Z, izotop_listesi(Z)))
        A = tamsayi(self.kno.get(), "Kütle numarası A")
        if A < max(Z, 2):
            raise HesapHatasi("Kütle numarası A, proton sayısından (Z) küçük olamaz.")
        if (Z, A) != self._son_giris:         # element / A değiştiyse Z, N, M yeniden dolar
            self._cekirdek_doldur(Z, A, hesapla=False)
            self._son_giris = (Z, A)
        super().hesapla()


# ------------------------------------------------------ 5) İzotop tablosu
CHIP_ADLARI = [("kararli", "Kararlı"), ("dogal", "Doğal radyoaktif"),
               ("bilinen", "Radyoaktif (veri var)"), ("tahmin", "Tahmini (model)")]
DURUM_METNI = {"kararli": "Kararlı izotop (doğada bulunur)",
               "dogal": "Doğal radyoaktif izotop",
               "bilinen": "Radyoaktif izotop",
               "tahmin": "Model tahmini — tabloda deneysel bilgi yok"}


def chip_rengi(tur, p):
    return {"kararli": _sonuk("#2fb380", 0.6), "dogal": _sonuk("#f08a3c", 0.6),
            "bilinen": p["vurgu"],
            "tahmin": p["soluk"]}[tur]


# --------------------------------------------- Nüklit haritası (Segrè diyagramı)
# Yatay eksen N (nötron), dikey eksen Z (proton). Her kutu bir izotop; renk bozunma türü.
SINIF_RENK = {k: (v if k == "kararli" else _sonuk(v, 0.55, 0.88)) for k, v in {
    "kararli": "#000000", "dogal": "#a855f7", "bm": "#5fd94a",
    "bp": "#e8483a", "ek": "#f59e42", "alfa": "#f3e45c",
    "karisik": "#38d0e2"}.items()}
SINIF_AD = [("kararli", "Kararlı"), ("dogal", "Doğal radyoaktif"),
            ("bm", "β⁻ bozunması"), ("bp", "β⁺ bozunması"),
            ("ek", "Elektron yakalama"), ("alfa", "α bozunması"),
            ("karisik", "β⁻ / EK karışık")]
SINIF_ADI = dict(SINIF_AD)


def _vadi_z(A):
    """Kararlılık vadisinin (kütle parabolünün en dibi) sürekli Z değeri."""
    aC, aA = 0.711, 23.7
    c = A ** (-1 / 3)
    return (4 * aA + aC * c) / (8 * aA / A + 2 * aC * c)


def nuklit_sinifi(Z, A):
    """(sınıf, veri_var_mı). Sınıf: kararli | dogal | bm | bp | ek | alfa | karisik"""
    tur = izotop_turu(Z, A)
    if tur == "kararli":
        return "kararli", True
    if tur == "dogal":
        return "dogal", True
    if tur == "bilinen":
        m = RADYO[(Z, A)][1].replace(" ", "")
        parca = m.split("/")
        bm = any(("β−" in t) or ("β-" in t) for t in parca)
        bp = any(("β+" in t) or t in ("EC", "EK") for t in parca)
        if m.startswith("α"):
            return "alfa", True
        if bm and bp:
            return "karisik", True
        if bm:
            return "bm", True
        if "β+" in m:
            return "bp", True
        if bp:
            return "ek", True
    # deneysel bilgi yok: vadinin hangi tarafında olduğuna göre tahmin
    z0 = _vadi_z(A)
    if Z >= 84 and Z >= z0 - 2:
        return "alfa", False
    return ("bm" if Z < z0 else "bp"), False


_HARITA = {}


def nuklit_haritasi():
    """{(Z, N): (sınıf, veri_var_mı)} — 118 elementin tüm listelenen izotopları."""
    if not _HARITA:
        for Z in range(1, 119):
            lo, hi = izotop_araligi(Z)
            # Model tahminlerini kararlılık vadisinin çevresindeki makul bir bantla sınırla
            # (gerçek harita gibi dar kalsın); bilinen izotoplar her zaman gösterilir.
            n0 = round(ELEMENT_KUTLE[Z_SEMBOL[Z]]) - Z
            alt, ust = n0 - (3 + 0.28 * Z), n0 + (12 + 0.06 * Z)
            for A in range(lo, hi + 1):
                sinif = nuklit_sinifi(Z, A)
                if not sinif[1] and not (alt <= A - Z <= ust):
                    continue
                _HARITA[(Z, A - Z)] = sinif
    return _HARITA


class NuklitHaritasi(tk.Canvas):
    """Nüklit haritası. Fare tekerleği = yakınlaştır, sürükle = kaydır,
    tıkla = izotopu seç, üzerine gelince = kısa bilgi."""

    def __init__(self, master, komut):
        super().__init__(master, highlightthickness=0, bd=0, height=px(420))
        self.komut = komut
        self.harita = nuklit_haritasi()
        self.maxN = max(n for (_z, n) in self.harita)
        self.secili = None
        self.s = 0.0
        self.s_min = 1.0
        self.nx0 = self.zb = -1.0
        self._geo = (0, 0, 1, 1)
        self._sigdi = True
        self._ust = None
        self._bas = None
        self._bekle = None
        self.bind("<Configure>", self._boyut)
        self.bind("<ButtonPress-1>", self._basla)
        self.bind("<B1-Motion>", self._surukle)
        self.bind("<ButtonRelease-1>", self._birak)
        self.bind("<Motion>", self._hareket)
        self.bind("<Leave>", self._ayril)
        self.bind_all("<MouseWheel>", self._tekerlek, add="+")
        _DINLEYICILER.append(self.ciz)

    # ---------------------------------------------------------- görünüm
    @staticmethod
    def _kenar(W, H):
        return px(46), px(10), W - px(12), H - px(36)       # L, T, R, B

    def _boyut(self, _e):
        if self._sigdi:
            self.sigdir()
        self.ciz()

    def sigdir(self):
        """Tüm haritayı pencereye sığdırır."""
        W, H = self.winfo_width(), self.winfo_height()
        L, T, R, B = self._kenar(W, H)
        if R - L < 40 or B - T < 40:
            return
        self.s_min = max(1.0, min((R - L) / (self.maxN + 3), (B - T) / 121.0))
        self.s = self.s_min
        self.nx0 = self.zb = -1.0
        self._sigdi = True

    def _sinirla(self):
        L, T, R, B = self._geo
        vw, vh = (R - L) / self.s, (B - T) / self.s
        self.nx0 = min(max(self.nx0, -0.7 * vw), self.maxN + 2 - 0.3 * vw)
        self.zb = min(max(self.zb, -0.7 * vh), 120 - 0.3 * vh)

    def yakinlastir(self, f, cx=None, cy=None):
        W, H = self.winfo_width(), self.winfo_height()
        L, T, R, B = self._geo = self._kenar(W, H)
        cx = (L + R) / 2 if cx is None else cx
        cy = (T + B) / 2 if cy is None else cy
        wn = self.nx0 + (cx - L) / self.s
        wz = self.zb + (B - cy) / self.s
        s2 = min(max(self.s * f, self.s_min), px(70))
        if s2 == self.s:
            return
        self.s = s2
        self.nx0 = wn - (cx - L) / s2
        self.zb = wz + 0.0 - (B - cy) / s2
        self._sigdi = abs(s2 - self.s_min) < 1e-9
        self._sinirla()
        self.ciz()

    def sec(self, Z, A):
        self.secili = (Z, A)
        self._secim_ciz()

    # ---------------------------------------------------------- çizim
    def ciz(self):
        p = renkler()
        self.configure(bg=p["panel"])
        self.delete("all")
        W, H = self.winfo_width(), self.winfo_height()
        if W < 160 or H < 120:
            return
        L, Ut, R, B = self._geo = self._kenar(W, H)
        if self.s <= 0:
            self.sigdir()
        self._sinirla()
        s, nx0, zb = self.s, self.nx0, self.zb
        n_lo, n_hi = int(math.floor(nx0)), int(math.ceil(nx0 + (R - L) / s))
        z_lo = max(1, int(math.floor(zb)))
        z_hi = min(118, int(math.ceil(zb + (B - Ut) / s)))

        # sınıf başına renkler: (kesin dolgu, tahmin dolgusu, kenar)
        kenarli = s >= 6
        renk = {}
        for k, c in SINIF_RENK.items():
            kes = c
            tah = karistir(p["panel"], c, 0.38)
            if kenarli:
                kn = p["soluk"] if k == "kararli" else karistir(c, p["panel"], 0.45)
                kn_t = karistir(tah, p["panel"], 0.45)
            else:
                kn, kn_t = kes, tah
            renk[k] = (kes, tah, kn, kn_t)

        yaz = s >= 16
        yaz_iki = s >= 30
        f_sem = ("Segoe UI", max(6, int(s * (0.34 if yaz_iki else 0.42))), "bold")
        f_a = ("Segoe UI", max(6, int(s * 0.2)))
        rect, text = self.create_rectangle, self.create_text
        harita = self.harita
        for Z in range(z_lo, z_hi + 1):
            y1 = B - (Z - zb) * s
            y0 = y1 - s
            sem = Z_SEMBOL[Z]
            for N in range(n_lo, n_hi + 1):
                v = harita.get((Z, N))
                if v is None:
                    continue
                sinif, veri = v
                x0 = L + (N - nx0) * s
                kes, tah, kn, kn_t = renk[sinif]
                rect(x0, y0, x0 + s, y1, fill=kes if veri else tah,
                     outline=kn if veri else kn_t, width=1 if kenarli else 0)
                if yaz:
                    beyaz = veri and sinif in ("kararli", "dogal")
                    fg = "#ffffff" if beyaz else ("#10131a" if veri else p["soluk"])
                    if yaz_iki:
                        text(x0 + s / 2, y0 + s * 0.27, text=str(Z + N), fill=fg, font=f_a)
                        text(x0 + s / 2, y0 + s * 0.64, text=sem, fill=fg, font=f_sem)
                    else:
                        text(x0 + s / 2, y0 + s / 2, text=sem, fill=fg, font=f_sem)

        # sihirli sayılar: kabuk kapanma çizgileri
        for m in SIHIRLI:
            xm = L + (m + 1 - nx0) * s
            ym = B - (m + 1 - zb) * s
            if L < xm < R:
                self.create_line(xm, Ut, xm, B, fill=p["soluk"], dash=(2, 4))
            if Ut < ym < B:
                self.create_line(L, ym, R, ym, fill=p["soluk"], dash=(2, 4))

        # kenar boşlukları (taşan kutuları örter) + eksenler
        for a in ((0, 0, W, Ut), (0, B, W, H), (0, 0, L, H), (R, 0, W, H)):
            rect(*a, fill=p["panel"], outline="")
        rect(L, Ut, R, B, outline=p["izgara"])
        adim = next((a for a in (1, 2, 5, 10, 20, 25, 50) if a * s >= px(28)), 50)
        f_t = ("Segoe UI", 8)
        for N in range(max(0, int(math.ceil(nx0 / adim)) * adim), n_hi + 1, adim):
            x = L + (N - nx0 + 0.5) * s
            if L <= x <= R:
                self.create_line(x, B, x, B + px(4), fill=p["soluk"])
                text(x, B + px(6), text=str(N), anchor="n", fill=p["soluk"], font=f_t)
        for Z in range(max(adim, int(math.ceil(zb / adim)) * adim), z_hi + 1, adim):
            y = B - (Z - zb + 0.5) * s
            if Ut <= y <= B:
                self.create_line(L - px(4), y, L, y, fill=p["soluk"])
                text(L - px(6), y, text=str(Z), anchor="e", fill=p["soluk"], font=f_t)
        f_b = ("Segoe UI", 9, "bold")
        text(R, H - px(3), text=T("N (nötron sayısı)") + "  →", anchor="se",
             fill=p["yazi"], font=f_b)
        try:
            text(px(10), (Ut + B) / 2, text=T("Z (proton sayısı)") + "  →",
                 angle=90, fill=p["yazi"], font=f_b)
        except tk.TclError:
            text(px(6), Ut + px(2), text="Z ↑", anchor="nw", fill=p["yazi"], font=f_b)
        self._secim_ciz()

    def _secim_ciz(self):
        self.delete("secim")
        if not self.secili or self.s <= 0:
            return
        p = renkler()
        L, T, R, B = self._geo
        Z, A = self.secili
        N = A - Z
        s = self.s
        x0 = L + (N - self.nx0) * s
        y1 = B - (Z - self.zb) * s
        y0 = y1 - s
        if x0 < L or x0 + s > R or y0 < T or y1 > B:
            return
        e = max(1.5, s * 0.12)
        self.create_rectangle(x0 - e, y0 - e, x0 + s + e, y1 + e, outline=p["vurgu"],
                              width=2, tags="secim")
        if s >= 8:
            self.create_rectangle(x0 - 0.5, y0 - 0.5, x0 + s + 0.5, y1 + 0.5,
                                  outline="#ffffff", width=1, tags="secim")

    # ---------------------------------------------------------- etkileşim
    def _hucre(self, x, y):
        L, T, R, B = self._geo
        if self.s <= 0 or not (L <= x < R and T <= y < B):
            return None
        N = int(math.floor(self.nx0 + (x - L) / self.s))
        Z = int(math.floor(self.zb + (B - y) / self.s))
        return (Z, N) if (Z, N) in self.harita else None

    def _ipucu_sil(self):
        self.delete("ipucu")
        self._ust = None

    def _ipucu(self, Z, N, x, y):
        p = renkler()
        sinif, veri = self.harita[(Z, N)]
        A = Z + N
        satir = [f"{Z_SEMBOL[Z]}-{A}   ({T(ELEMENT_ADI[Z])})",
                 f"Z = {Z}   N = {N}   A = {A}",
                 T(SINIF_ADI[sinif]) + ("" if veri else "  ·  " + T("tahmini"))]
        t = self.create_text(x + px(14), y + px(14), text="\n".join(satir), anchor="nw",
                             fill=p["yazi"], font=("Segoe UI", 9), tags="ipucu")
        x0, y0, x1, y1 = self.bbox(t)
        W, H = self.winfo_width(), self.winfo_height()
        dx = -(x1 - x0) - px(28) if x1 + px(10) > W else 0
        dy = -(y1 - y0) - px(28) if y1 + px(10) > H else 0
        self.move(t, dx, dy)
        x0, y0, x1, y1 = self.bbox(t)
        r = self.create_rectangle(x0 - px(6), y0 - px(4), x1 + px(6), y1 + px(4),
                                  fill=p["giris"], outline=p["izgara"], tags="ipucu")
        self.tag_lower(r, t)

    def _hareket(self, e):
        if self._bas:
            return
        c = self._hucre(e.x, e.y)
        self.configure(cursor="hand2" if c else "arrow")
        if c != self._ust:
            self.delete("ipucu")
            self._ust = c
            if c:
                self._ipucu(c[0], c[1], e.x, e.y)

    def _ayril(self, _e):
        self._ipucu_sil()

    def _basla(self, e):
        self._bas = (e.x, e.y, self.nx0, self.zb, False)

    def _surukle(self, e):
        if not self._bas:
            return
        x0, y0, n0, z0, hareket = self._bas
        if not hareket and abs(e.x - x0) + abs(e.y - y0) < px(5):
            return
        self._bas = (x0, y0, n0, z0, True)
        self.configure(cursor="fleur")
        self._ipucu_sil()
        self.nx0 = n0 - (e.x - x0) / self.s
        self.zb = z0 + (e.y - y0) / self.s
        self._sigdi = False
        self._sinirla()
        if self._bekle is None:
            self._bekle = self.after_idle(self._yenile)

    def _yenile(self):
        self._bekle = None
        self.ciz()

    def _birak(self, e):
        b, self._bas = self._bas, None
        self.configure(cursor="arrow")
        if b and not b[4]:
            c = self._hucre(e.x, e.y)
            if c:
                self.komut(c[0], c[0] + c[1])

    def _tekerlek(self, e):
        try:
            w = self.winfo_containing(e.x_root, e.y_root)
        except (KeyError, tk.TclError):
            return
        if w is self:
            self.yakinlastir(1.25 if e.delta > 0 else 0.8,
                             e.x_root - self.winfo_rootx(),
                             e.y_root - self.winfo_rooty())


class NuklitKarti(Kart):
    """Başlık + yakınlaştırma düğmeleri + renk açıklaması + nüklit haritası."""

    def __init__(self, master, komut):
        self._hazir = False
        super().__init__(master)
        ic = self.ic
        self.ust = tk.Frame(ic)
        self.ust.pack(fill="x", padx=px(16), pady=(px(12), 0))
        self.baslik = tk.Label(self.ust, text=T("Nüklit haritası (N – Z)"),
                               font=("Segoe UI", 12, "bold"), anchor="w")
        self.baslik.pack(side="left")
        kar = sum(1 for v in nuklit_haritasi().values() if v[0] == "kararli")
        self.say = tk.Label(self.ust, text=f"{len(nuklit_haritasi())} {T('nüklit')} · "
                                           f"{kar} {T('kararlı')}",
                            font=("Segoe UI", 9), anchor="w")
        self.say.pack(side="left", padx=(px(10), 0))
        for metin, fn in (("+", lambda: self.harita.yakinlastir(1.4)),
                          ("−", lambda: self.harita.yakinlastir(1 / 1.4)),
                          (T("Tümünü göster"), self._sigdir)):
            ttk.Button(self.ust, text=metin, style="Gri.TButton", cursor="hand2",
                       width=3 if len(metin) == 1 else 13, command=fn
                       ).pack(side="right", padx=(px(6), 0))
        self.leg = tk.Frame(ic)
        self.leg.pack(fill="x", padx=px(16), pady=(px(8), px(2)))
        self.kutular = {}
        oge = SINIF_AD + [("tahmin", "Soluk tonlar: tahmini (model)"),
                          ("sihirli", "Sihirli sayılar")]
        for i, (tur, ad) in enumerate(oge):
            r, c = divmod(i, 5)
            k = tk.Frame(self.leg)
            k.grid(row=r, column=c, sticky="w", padx=(0, px(14)), pady=1)
            kutu = tk.Label(k, text="", width=2, highlightthickness=1)
            kutu.pack(side="left")
            y = tk.Label(k, text=T(ad), font=("Segoe UI", 9))
            y.pack(side="left", padx=(px(4), 0))
            self.kutular[tur] = (k, kutu, y)
        self.harita = NuklitHaritasi(ic, komut)
        self.harita.pack(fill="both", expand=True, padx=px(10), pady=(px(4), px(10)))
        self._hazir = True
        self.renk_uygula()

    def _sigdir(self):
        self.harita.sigdir()
        self.harita.ciz()

    def renk_uygula(self):
        super().renk_uygula()
        if not self._hazir:
            return
        p = renkler()
        for w in (self.ust, self.leg):
            w.configure(bg=p["panel"])
        self.baslik.configure(bg=p["panel"], fg=p["yazi"])
        self.say.configure(bg=p["panel"], fg=p["soluk"])
        for tur, (k, kutu, y) in self.kutular.items():
            k.configure(bg=p["panel"])
            if tur == "tahmin":
                c = karistir(p["panel"], SINIF_RENK["bm"], 0.38)
            elif tur == "sihirli":
                c = p["panel"]
            else:
                c = SINIF_RENK[tur]
            kutu.configure(bg=c, highlightbackground=p["soluk"])
            y.configure(bg=p["panel"], fg=p["soluk"])


class BilgiPaneli(Kart):
    """Seçili element + izotop hakkında ayrıntılı bilgi (sağ panel)."""

    def __init__(self, master, komut_baglanma):
        self._durum = None
        self._hazir = False
        self.komut = komut_baglanma
        super().__init__(master)
        self.ks = KaydirmaliCerceve(self.ic, genislik=px(350))
        self.ks.pack(fill="both", expand=True)
        self._hazir = True
        self._ciz()

    def renk_uygula(self):
        super().renk_uygula()
        if self._hazir:
            self._ciz()

    def goster(self, Z, A):
        yeni = self._durum is None or self._durum[0] != Z
        self._durum = (Z, A)
        self._ciz()
        if yeni:
            self.ks.cv.yview_moveto(0)

    @staticmethod
    def _kutular(ic, p, kutular, sut=3):
        g = tk.Frame(ic, bg=p["panel"])
        g.pack(fill="x", padx=px(18), pady=(px(8), 0))
        for c in range(sut):
            g.columnconfigure(c, weight=1, uniform="b")
        for i, (et, dg) in enumerate(kutular):
            t = tk.Frame(g, bg=p["giris"])
            t.grid(row=i // sut, column=i % sut, sticky="nsew",
                   padx=(0 if i % sut == 0 else px(6), 0), pady=px(3))
            tk.Label(t, text=et, bg=p["giris"], fg=p["soluk"], anchor="w",
                     font=("Segoe UI", 8)).pack(fill="x", padx=px(8), pady=(px(6), 0))
            tk.Label(t, text=dg, bg=p["giris"], fg=p["yazi"], anchor="w",
                     font=("Consolas", 10, "bold")).pack(fill="x", padx=px(8),
                                                         pady=(0, px(6)))

    def _ciz(self):
        p = renkler()
        ic = self.ks.icerik
        for w in ic.winfo_children():
            w.destroy()
        if self._durum is None:
            return
        Z, A = self._durum
        b = izotop_bilgi(Z, A)
        sem = Z_SEMBOL[Z]
        kat = kategori(Z)
        renk = KATEGORI_RENK[kat]

        # --- element başlığı
        ust = tk.Frame(ic, bg=p["panel"])
        ust.pack(fill="x", padx=px(18), pady=(px(16), px(4)))
        tk.Label(ust, text=sem, bg=karistir(p["panel"], renk, 0.28), fg=renk,
                 font=("Segoe UI", 22, "bold"), width=3, pady=px(6)).pack(side="left")
        yan = tk.Frame(ust, bg=p["panel"])
        yan.pack(side="left", padx=(px(12), 0))
        tk.Label(yan, text=ELEMENT_ADI[Z], bg=p["panel"], fg=p["yazi"],
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(yan, text=f"{KATEGORI_AD[kat]} · Z = {Z}", bg=p["panel"],
                 fg=p["soluk"], font=("Segoe UI", 9)).pack(anchor="w")

        kg = ELEMENT_KUTLE[sem]
        agirlik = f"[{kg:g}]" if Z in AGIRLIK_PARANTEZLI else f"{kg:.5g}"
        lo, hi = izotop_araligi(Z)
        n_kar = sum(1 for (z, _a) in DOGAL_KARARLI if z == Z)
        n_dog = n_kar + sum(1 for (z, _a) in DOGAL_RADYO if z == Z)
        self._kutular(ic, p, [("Atom ağırlığı (u)", agirlik),
                              ("Periyot", str(periyot(Z))), ("Grup", grup(Z)),
                              ("Oda sıcaklığı", oda_hali(Z)),
                              ("Kararlı izotop", str(n_kar)),
                              ("Doğal izotop", str(n_dog))])
        tk.Label(ic, text=f"Listelenen izotop aralığı: A = {lo} – {hi}", bg=p["panel"],
                 fg=p["soluk"], font=("Segoe UI", 8), anchor="w").pack(
            fill="x", padx=px(20), pady=(px(4), 0))
        tk.Frame(ic, bg=p["izgara"], height=1).pack(fill="x", padx=px(18),
                                                    pady=(px(12), px(8)))

        # --- izotop başlığı
        tk.Label(ic, text=f"{sem}-{A}", bg=p["panel"], fg=p["vurgu"], anchor="w",
                 font=("Segoe UI", 20, "bold")).pack(fill="x", padx=px(18))
        tk.Label(ic, text=f"{ELEMENT_ADI[Z]}-{A}", bg=p["panel"], fg=p["soluk"],
                 anchor="w", font=("Segoe UI", 9)).pack(fill="x", padx=px(20))
        tk.Label(ic, text="●  " + DURUM_METNI[b["tur"]], bg=p["panel"],
                 fg=chip_rengi(b["tur"], p), anchor="w",
                 font=("Segoe UI", 10, "bold")).pack(fill="x", padx=px(20),
                                                     pady=(px(6), px(4)))

        satirlar = []
        if b["yuzde"] is not None:
            satirlar.append(("Doğal bulunurluk", f"% {b['yuzde']:g}"))
        if b["tur"] == "kararli":
            satirlar.append(("Yarı ömür", "kararlı"))
        elif b["yarimomur"]:
            satirlar.append(("Yarı ömür", b["yarimomur"]))
        if b["mod"]:
            satirlar.append(("Bozunma", b["mod"]))
        tag = "deneysel" if b["deneysel"] else "tahmini"
        satirlar += [("Z / N / A", f"{Z} / {b['N']} / {A}"),
                     ("N / Z", f"{b['N'] / Z:.3f}"),
                     ("Çekirdek türü", b["tip"]),
                     ("Sihirli sayı", b["sihirli"]),
                     (f"Atom kütlesi ({tag})", f"{b['M']:.6f} u"),
                     (f"Toplam B ({tag})", f"{b['B']:.2f} MeV"),
                     (f"B / A ({tag})", f"{b['B_A']:.3f} MeV")]
        tablo = tk.Frame(ic, bg=p["panel"])
        tablo.pack(fill="x", padx=px(20), pady=(px(4), 0))
        tablo.columnconfigure(1, weight=1)
        for r, (et, dg) in enumerate(satirlar):
            tk.Label(tablo, text=et, bg=p["panel"], fg=p["soluk"], anchor="w",
                     font=("Segoe UI", 9)).grid(row=r, column=0, sticky="w", pady=2)
            tk.Label(tablo, text=dg, bg=p["panel"], fg=p["yazi"], anchor="e",
                     justify="right", wraplength=px(190),
                     font=("Consolas", 10)).grid(row=r, column=1, sticky="e",
                                                 padx=(px(10), 0), pady=2)

        if b["not"]:
            tk.Label(ic, text=b["not"], bg=p["panel"], fg=p["yazi"], anchor="w",
                     justify="left", wraplength=px(300),
                     font=("Segoe UI", 9)).pack(fill="x", padx=px(20), pady=(px(10), 0))
        if not b["deneysel"]:
            tk.Label(ic, text="⚠  Bu çekirdeğin deneysel kütlesi tabloda yok: kütle ve "
                              "bağlanma enerjisi Weizsäcker formülüyle hesaplanmış "
                              "yaklaşık değerlerdir (orta/ağır çekirdeklerde ≈%1 hata).",
                     bg=p["panel"], fg=p["uyari"], anchor="w", justify="left",
                     wraplength=px(300), font=("Segoe UI", 8)).pack(
                fill="x", padx=px(20), pady=(px(8), 0))
        if b["tur"] == "tahmin":
            tk.Label(ic, text="⚠  Bu izotopun varlığı/yarı ömrü hakkında tabloda bilgi "
                              "yok; model onu 'bağlı' olarak öngörüyor.",
                     bg=p["panel"], fg=p["uyari"], anchor="w", justify="left",
                     wraplength=px(300), font=("Segoe UI", 8)).pack(
                fill="x", padx=px(20), pady=(px(6), 0))
        ttk.Button(ic, text=T("Bağlanma Enerjisi sekmesinde aç  →"), style="Gri.TButton",
                   cursor="hand2", command=lambda: self.komut(Z, A)).pack(
            fill="x", padx=px(20), pady=(px(14), px(18)))


class IzotopSayfasi(ttk.Frame):
    BASLIK = "İzotop Tablosu"
    MENU = "İzotop Tablosu"
    SIMGE = "▦"
    ALT = ("Haritada bir izotopa tıkla: çekirdek bilgileri sağda görünür. "
           "Fare tekerleği yakınlaştırır, sürükleyerek kaydırırsın.")

    def __init__(self, master, ayar):
        super().__init__(master)
        self.ayar = ayar
        self.Z = 26
        self.A = 56
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        SayfaBasligi(self, modul_etiketi(type(self)), T(self.BASLIK),
                     T(self.ALT)).grid(row=0, column=0, sticky="ew")
        govde = ttk.Frame(self)
        govde.grid(row=1, column=0, sticky="nsew", padx=px(30), pady=(0, px(26)))
        govde.columnconfigure(0, weight=1)
        govde.rowconfigure(0, weight=1)

        sol = ttk.Frame(govde)
        sol.grid(row=0, column=0, sticky="nsew", padx=(0, px(18)))
        sol.columnconfigure(0, weight=1)
        sol.rowconfigure(0, weight=1)
        self.kart = NuklitKarti(sol, self._haritadan_sec)
        self.kart.grid(row=0, column=0, sticky="nsew")
        self.harita = self.kart.harita

        self.bilgi = BilgiPaneli(govde, self._baglanmaya_git)
        self.bilgi.grid(row=0, column=1, sticky="ns")
        self.izotop_sec(26, 56)

    def izotop_sec(self, Z, A):
        self.Z, self.A = Z, A
        self.harita.sec(Z, A)
        self.bilgi.goster(Z, A)

    def _haritadan_sec(self, Z, A):
        """Kullanıcı haritada tıkladı: seç ve anlatıcıya haber ver."""
        self.izotop_sec(Z, A)
        a = getattr(self.winfo_toplevel(), "anlatici", None)
        if a is not None:
            a.olay("tepe" if (Z, A) in ((26, 56), (28, 62)) else "secim",
                   s=f"{Z_SEMBOL[Z]}-{A}")

    def _baglanmaya_git(self, Z, A):
        kok = self.winfo_toplevel()
        if hasattr(kok, "baglanmaya_git"):
            kok.baglanmaya_git(Z, A)


# ---------------------------------------------------------------- Ayarlar
class AyarSayfasi(ttk.Frame):
    BASLIK = "Ayarlar"
    MENU = "Ayarlar"
    SIMGE = "⚙"
    ALT = "Görünümü ve sayıların yazılışını kendine göre ayarla."

    def __init__(self, master, ayar):
        super().__init__(master)
        self.ayar = ayar
        SayfaBasligi(self, modul_etiketi(type(self)), T(self.BASLIK),
                     T(self.ALT)).pack(fill="x")
        satir = ttk.Frame(self)
        satir.pack(fill="x", padx=px(30), anchor="n")

        # --- görünüm kartı
        k1 = Kart(satir)
        k1.pack(side="left", anchor="n", padx=(0, px(18)))
        kutu = ttk.Frame(k1.ic, style="Kart.TFrame")
        kutu.pack(padx=px(26), pady=px(22))
        ttk.Label(kutu, text=T("Görünüm"), style="KartBaslik.TLabel").pack(anchor="w")

        self._etiket(kutu, "Dil")
        self.dil = Combo(kutu, DILLER, ayar.al("dil"), self._dil)
        self.dil.pack(anchor="w")

        self._etiket(kutu, "Tema")
        self.seg = Segment(kutu, list(PALETLER), ayar.al("tema"), self._tema)
        self.seg.pack(anchor="w")

        self._etiket(kutu, "Vurgu rengi")
        self.renk = RenkSecici(kutu, ayar.al("renk"), self._renk)
        self.renk.pack(anchor="w")

        self._etiket(kutu, "Ondalık basamak sayısı")
        self.ond = Combo(kutu, [str(i) for i in range(11)], str(ayar.al("ondalik")),
                         self._ondalik)
        self.ond.pack(anchor="w")

        self._etiket(kutu, "Anlatıcı")
        self.stil_listesi = [stil_adi(k) for k in ANLATICI_STILLERI]
        self.anl_stil = Combo(kutu, self.stil_listesi, stil_adi(ayar.al("anlatici_stil")),
                              self._anl_stil, width=40)
        self.anl_stil.pack(anchor="w")
        self.anl_var = tk.BooleanVar(value=ayar.al("anlatici"))
        ttk.Checkbutton(kutu, text=T("Anlatıcıyı göster"), variable=self.anl_var,
                        command=self._anl_ac, style="Kart.TCheckbutton", cursor="hand2"
                        ).pack(anchor="w", pady=(px(14), 0))

        self.anim = tk.BooleanVar(value=ayar.al("animasyon"))
        ttk.Checkbutton(kutu, text=T("Yumuşak sayfa geçiş animasyonu"),
                        variable=self.anim, command=self._anim,
                        style="Kart.TCheckbutton", cursor="hand2"
                        ).pack(anchor="w", pady=(px(20), 0))
        Hap(kutu, T("Varsayılana sıfırla"), self._sifirla, gri=True,
            zemin="panel").pack(anchor="w", pady=(px(22), 0))

        # --- hakkında kartı
        k2 = Kart(satir)
        k2.pack(side="left", anchor="n")
        h = ttk.Frame(k2.ic, style="Kart.TFrame")
        h.pack(padx=px(26), pady=px(22))
        ttk.Label(h, text=T("Hakkında"), style="KartBaslik.TLabel").pack(anchor="w")
        ttk.Label(h, style="Etiket.TLabel", justify="left", wraplength=px(330),
                  text=hakkinda_metni()).pack(anchor="w", pady=(px(10), 0))

    @staticmethod
    def _etiket(kap, metin):
        ttk.Label(kap, text=T(metin), style="Etiket.TLabel").pack(anchor="w",
                                                              pady=(px(18), px(6)))

    def _yenile(self):
        kok = self.winfo_toplevel()
        tema_uygula(kok, self.ayar)
        if hasattr(kok, "gecis"):
            kok.gecis()

    def _tema(self, secim):
        self.ayar.ayarla("tema", secim)
        self._yenile()

    def _renk(self, secim):
        self.ayar.ayarla("renk", secim)
        self._yenile()

    def _ondalik(self, secim):
        self.ayar.ayarla("ondalik", int(secim))

    def _dil(self, secim):
        self.ayar.ayarla("dil", secim)
        kok = self.winfo_toplevel()
        if hasattr(kok, "yeniden_kur"):
            # tüm arayüz yeni dilde baştan kurulur (olay işlenirken değil, hemen sonra)
            kok.after(30, lambda: kok.yeniden_kur(AyarSayfasi.__name__))

    def _anim(self):
        self.ayar.ayarla("animasyon", bool(self.anim.get()))

    def _anl_stil(self, secim):
        self.ayar.ayarla("anlatici_stil", ANLATICI_STILLERI[self.stil_listesi.index(secim)])
        self.ayar.ayarla("anlatici", True)
        self.anl_var.set(True)
        a = getattr(self.winfo_toplevel(), "anlatici", None)
        if a is not None:
            a.stil_degisti()

    def _anl_ac(self):
        self.ayar.ayarla("anlatici", bool(self.anl_var.get()))
        a = getattr(self.winfo_toplevel(), "anlatici", None)
        if a is not None:
            a.goster_gizle()

    def _sifirla(self):
        self.ayar.sifirla()
        self.seg.sec(self.ayar.al("tema"))
        self.renk.sec(self.ayar.al("renk"))
        self.ond.set(str(self.ayar.al("ondalik")))
        self.anim.set(self.ayar.al("animasyon"))
        self.anl_var.set(self.ayar.al("anlatici"))
        self._yenile()
        kok = self.winfo_toplevel()
        if hasattr(kok, "yeniden_kur"):
            kok.after(30, lambda: kok.yeniden_kur(AyarSayfasi.__name__))


# ------------------------------------------------------------ 0) Ana Sayfa
class AnaSayfa(ttk.Frame):
    """Ana sayfa: tek tuval üzerine çizilen, ışık geçişli ve hafifçe hareketli karşılama."""
    BASLIK = "Ana Sayfa"
    MENU = "Ana Sayfa"
    SIMGE = "⌂"
    ALT = ""
    TANITIM = ('Nucleus; nükleer mühendislik öğrencileri için hazırlanmış bir hesap aracıdır. Ortalama atomik kütle, atom yoğunluğu, molar kütle ile toplam ve nükleon başına bağlanma enerjisini hesaplar; 118 elementin izotoplarını nüklit haritası üzerinden incelemeni sağlar.')
    # kart açıklamaları (T() ile çevrilir)
    KISA = {
        "AtomikKutleSayfasi": "İzotop bulunurluklarından ortalama atomik kütle",
        "YogunlukSayfasi": "Yoğunluktan birim hacimdeki atom sayısı",
        "MolarKutleSayfasi": "Kimyasal formülden molar kütle",
        "BaglanmaSayfasi": "Kütle kusurundan bağlanma enerjisi",
        "NukleonBasinaSayfasi": "Bağlanma enerjisinin nükleon başına değeri (BE/A)",
        "IzotopSayfasi": "118 elementin izotopları ve çekirdek verileri",
        "AyarSayfasi": "Tema, renk, dil ve sayı biçimi",
    }

    def __init__(self, master, ayar):
        super().__init__(master)
        self.ayar = ayar
        self.cv = tk.Canvas(self, highlightthickness=0, bd=0)
        self.cv.pack(fill="both", expand=True)
        self._parc = []
        self._bekle = None
        self.cv.bind("<Configure>", self._boyut)
        _DINLEYICILER.append(self._ciz)
        self._tik()

    def _boyut(self, _e):
        if self._bekle:
            self.after_cancel(self._bekle)
        self._bekle = self.after(60, self._ciz)

    def _git(self, anahtar):
        kok = self.winfo_toplevel()
        if hasattr(kok, "sayfa_ac"):
            kok.sayfa_ac(anahtar)

    def _ciz(self):
        self._bekle = None
        try:
            self._ciz_ic()
        except tk.TclError:
            pass

    # --- tuval öğelerine tıklama / üstüne gelme davranışı
    def _bagla(self, etiket, oge, normal, hover, komut, kenar_n=None, kenar_h=None):
        cv = self.cv

        def gir(_e):
            cv.itemconfigure(oge, fill=hover, outline=kenar_h or hover)
            cv.configure(cursor="hand2")

        def cik(_e):
            cv.itemconfigure(oge, fill=normal, outline=kenar_n or normal)
            cv.configure(cursor="")

        cv.tag_bind(etiket, "<Enter>", gir)
        cv.tag_bind(etiket, "<Leave>", cik)
        cv.tag_bind(etiket, "<Button-1>", lambda _e: komut())

    def _hap(self, x0, y0, w, h, metin, komut, gri, etiket):
        p, cv = renkler(), self.cv
        if gri:
            dolgu = karistir(p["bg"], p["yazi"], 0.06)
            kenar = karistir(p["bg"], p["yazi"], 0.24)
            yazi = p["yazi"]
            hover, kenar_h = karistir(p["bg"], p["yazi"], 0.14), karistir(p["bg"], p["yazi"], 0.5)
        else:
            dolgu, kenar, yazi = p["yazi"], p["yazi"], p["bg"]
            hover = kenar_h = karistir(p["yazi"], p["bg"], 0.16)
        oge = _yuvarlak_dikdortgen(cv, x0, y0, x0 + w, y0 + h, h / 2, fill=dolgu,
                                   outline=kenar, tags=etiket)
        cv.create_text(x0 + w / 2, y0 + h / 2, text=metin, tags=etiket,
                       font=("Segoe UI Semibold", 10), fill=yazi)
        self._bagla(etiket, oge, dolgu, hover, komut, kenar, kenar_h)

    def _kart(self, x, y, w, h, simge, baslik, aciklama, no, anahtar, i):
        p, cv = renkler(), self.cv
        t = "kart%d" % i
        cam = karistir(p["bg"], p["yazi"], 0.05)
        kenar = karistir(p["bg"], p["yazi"], 0.13)
        oge = _yuvarlak_dikdortgen(cv, x, y, x + w, y + h, px(20), fill=cam,
                                   outline=kenar, tags=t)
        cv.create_oval(x + px(16), y + px(18), x + px(56), y + px(58), tags=t,
                       fill=karistir(p["bg"], p["vurgu"], 0.14),
                       outline=karistir(p["bg"], p["vurgu"], 0.35))
        cv.create_text(x + px(36), y + px(38), text=simge, tags=t,
                       font=("Segoe UI Symbol", 15), fill=p["vurgu"])
        cv.create_text(x + px(68), y + px(26), text=baslik, anchor="w", tags=t,
                       font=("Segoe UI Semibold", 11), fill=p["yazi"])
        cv.create_text(x + w - px(18), y + px(26), text=no, anchor="e", tags=t,
                       font=("Segoe UI", 9), fill=p["soluk"])
        cv.create_text(x + px(68), y + px(42), text=aciklama, anchor="nw", tags=t,
                       width=w - px(68) - px(16), font=("Segoe UI", 8), fill=p["soluk"])
        self._bagla(t, oge, cam, karistir(p["bg"], p["yazi"], 0.10),
                    lambda a=anahtar: self._git(a), kenar,
                    karistir(p["bg"], p["yazi"], 0.34))

    def _ciz_ic(self):
        p, cv = renkler(), self.cv
        W, H = cv.winfo_width(), cv.winfo_height()
        if W < px(300) or H < px(300):
            return
        cv.configure(bg=p["bg"])
        cv.delete("all")
        cv.create_image(W / 2, 0, image=aurora_resmi(cv, 2000, px(900), "hero", 6),
                        anchor="n")
        cx = W / 2
        ofs = max(0, (H - px(640)) // 4)

        # --- süzülen toz parçacıkları
        rnd = random.Random(7)
        self._parc = []
        for _ in range(26):
            x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.75)
            r = rnd.choice((1, 1, 2))
            renk = karistir(p["bg"], p["yazi"], rnd.uniform(0.15, 0.5))
            i = cv.create_oval(x - r, y - r, x + r, y + r, fill=renk, outline="")
            self._parc.append([i, x, y, r, rnd.uniform(-0.15, 0.15), -rnd.uniform(0.15, 0.5)])

        # --- üst etiket hapı
        f_e = tkfont.Font(family="Segoe UI Semibold", size=9)
        et = T("Nükleer Mühendislik Hesap Aracı")
        pw = f_e.measure(et) + px(54)
        y = px(48) + ofs
        _yuvarlak_dikdortgen(cv, cx - pw / 2, y - px(15), cx + pw / 2, y + px(15), px(15),
                             fill=karistir(p["bg"], p["yazi"], 0.06),
                             outline=karistir(p["bg"], p["yazi"], 0.18))
        cv.create_oval(cx - pw / 2 + px(13), y - 3, cx - pw / 2 + px(19), y + 3,
                       fill=p["vurgu"], outline="")
        cv.create_text(cx - pw / 2 + px(28), y, text=et, anchor="w", font=f_e,
                       fill=p["soluk"])

        # --- büyük başlık: ince sans + italik serif
        f1 = tkfont.Font(family="Segoe UI Light", size=40)
        f2 = tkfont.Font(family="Georgia", size=40, slant="italic")
        cv.create_text(cx, px(118) + ofs, text=T("Çekirdeğin hesabı,"), font=f1,
                       fill=p["yazi"])
        cv.create_text(cx, px(172) + ofs, text=T("artık çok sade."), font=f2,
                       fill=p["yazi"])
        metin_id = cv.create_text(cx, px(214) + ofs, text=T(self.TANITIM), anchor="n",
                                  width=min(px(620), W - px(60)), justify="center",
                                  font=("Segoe UI", 10), fill=p["soluk"])
        alt = cv.bbox(metin_id)[3]          # metin kaç satır olursa olsun altına yerleş

        # --- iki hap düğme
        f_b = tkfont.Font(family="Segoe UI Semibold", size=10)
        t1, t2 = T("Hesaplamaya başla"), T("İzotop Tablosu")
        w1, w2 = f_b.measure(t1) + px(56), f_b.measure(t2) + px(56)
        bx = cx - (w1 + w2 + px(12)) / 2
        by = alt + px(24)
        self._hap(bx, by, w1, px(44), t1, lambda: self._git(SAYFALAR[1].__name__),
                  False, "hapA")
        self._hap(bx + w1 + px(12), by, w2, px(44), t2,
                  lambda: self._git(IzotopSayfasi.__name__), True, "hapB")

        # --- sekme kartları (cam görünümlü)
        kartlar = [(c.__name__, c.SIMGE, c.MENU) for c in SAYFALAR if c is not AnaSayfa]
        kartlar.append((AyarSayfasi.__name__, AyarSayfasi.SIMGE, AyarSayfasi.MENU))
        kw, kh, bosluk, sut = px(236), px(98), px(14), 4
        x_bas = cx - (sut * kw + (sut - 1) * bosluk) / 2
        y_bas = by + px(44) + px(32)
        for i, (anahtar, simge, menu) in enumerate(kartlar):
            r_, c_ = divmod(i, sut)
            self._kart(x_bas + c_ * (kw + bosluk), y_bas + r_ * (kh + bosluk), kw, kh,
                       simge, T(menu), T(self.KISA.get(anahtar, "")), str(i + 2),
                       anahtar, i)
        satir_sayisi = (len(kartlar) + sut - 1) // sut
        cv.create_text(cx, y_bas + satir_sayisi * (kh + bosluk) + px(12),
                       text=T("Üstteki menüyü ya da klavyedeki rakam tuşlarını (1–8) "
                              "kullanabilirsin."),
                       font=("Segoe UI", 9), fill=p["soluk"])

    def _tik(self):
        try:
            if not self.winfo_exists():
                return
            W, H = self.cv.winfo_width(), self.cv.winfo_height()
            for q in self._parc:
                i, x, y, r, vx, vy = q
                x += vx
                y += vy
                if y < -5:
                    y = H * 0.8
                if x < -5 or x > W + 5:
                    x = W / 2
                q[1], q[2] = x, y
                self.cv.coords(i, x - r, y - r, x + r, y + r)
            self.after(50, self._tik)
        except tk.TclError:
            pass


# --------------------------------------------------- SAYFA KAYIT LİSTESİ
# Sıra = soldaki menü sırası. Yeni sayfanı buraya ekle.
SAYFALAR = [
    AnaSayfa,
    AtomikKutleSayfasi,
    YogunlukSayfasi,
    MolarKutleSayfasi,
    BaglanmaSayfasi,
    NukleonBasinaSayfasi,
    IzotopSayfasi,
]


# =============================================================================
#  ANLATICI  (fotoğraflı, oyun anlatıcısı tarzında interaktif rehber)
# =============================================================================
# Sağ altta konuşan küçük bir kart: fotoğraf avatar, daktilo efektiyle yazılan metin.
#  · Açılışta kendini tanıtır, "Turu başlat" ile tüm sekmeleri tek tek gezdirir.
#  · Hesap yapınca, hata alınca, haritada izotop seçince, bir süre boş kalınca tepki verir.
#  · Avatara tıklarsan seni dürter; "Sus" ya da ✕ ile küçülür (avatar sağ altta kalır).
#  · Ayarlar > Anlatıcı: 4 farklı anlatım tarzı + aç/kapat.
# Fotoğrafı değiştirmek için programın yanına "anlatici.png" (kare, PNG) koyman yeter.
# Metinler Türkçe ve İngilizce yazıldı; diğer dillerde İngilizce konuşur.
# Replikler tamamen özgündür; yalnızca ilham alınan tarzları taşır.
_AVATAR_B64 = "".join("""iVBORw0KGgoAAAANSUhEUgAAAKAAAACgCAYAAACLz2ctAAB3XElEQVR42uz9d7RlaVreCf4+t80x14aP9JmVla6qKEcVVFESThRIGsFCjbSEzEhawBr1SIPUGqnVPerpXt2tXtMtIZY0o14SAgSDEE4CBBQgKExRlKdsmkobkZmR4W/ENeecbT43f3z7nHvixo2IGy4jNKtPrptxzTF77+/d7/ea530e8dULltv9kHHvzw1i998LIW76MLovAA9EEWHHu64Aj3b/fj2ggXd1PwfgKHAEiIAQgBCzk4uktzsJvNF91gXg84ADPtH9/EL372WnCKjpZei+/rN97HW9xP+fG+DU6HZb0HtE5HEB7+mM7B7gYWD/ni/ypQa418c54GXgRGecnwOe637e67H/HwZ4FxvgdOF855VmBgd8LfAh4APAkyJSXuFd49yii502dw0DjDs+N84d15VOogKeAf4Q+BjwmR0GOfWO/9kY491lgAjETRrgHpzR1FvML/7jwJ8EPtwZ3/CSF0WCSK8RezCSXS5uRHDdHnDeuOOO0GD62OqM8DeAX+s85LXO9Y4b0w2993/mBjg1GD/3uyeA7wC+C3jfXFzFnFcUgBSRG7q0N2mAVzPKuCMWnB7zp4FfBD4CPDv3N7XDoP/zM8Dn1+xt/yBxhSu+2x/ilV4fr2p4C8B3An8R+MYueZiejwNEjHHm3abnKWYvV7PIP7mXQCQAkoic7apidjziKkfLrTZIPfd7B/wu8FPALwGbezHE22lAN3MdhADxwptggFc65Cj2bsBdqLXT8B4D/jzw17sYb36hhBBiZnQxxsvOc+q9pn5sejyCAHiiEAgEEY+KEqK8E+HUlYzxBPCjwM8AX72aId7+dQ03aIDiPxsDlCJeYnhPAX8H+AtAPrdVXRLHzZ/PbgY4c8HCdZdQEuPUAAMiagSyezN/N8T288Y13aYb4KeBHwKe3s0Q72oDfPGCu2NXcg8GmGI18J0HnBre9wLZnOFJcQNXOQhPjAFBRKARaJQCIWPygEiCgxhdWsQo3vTrdJXTmhrY1BBb4N/uYohvQrISbjiGvJsNUHdbKQKeEnF3w9vN2+39GCxaKaTQEKGpa8bjMVXlcdGBlCwuL5GXGhX3UE6Ke8mhb3kCsBdDnF3L/8MAr22AUmzX0g4Af1PA3yPubnh7XSjRfVgU22U6gWQyqjn52uu8+spLnDl3jPHoHM14TN16snKZb/7wd/PYU08ghUPEOEueYpeMiNi9m0wHFEJE7nIsN2qb13Fj7WaI/yvwz4GzczXMcDcZoL5ezzEfS91sZrxLE0FLIaZ3xF8D/kfgCEQQcWp46vozMYGMyeAjIUXzUnJhw/O5T3yCk899DN9sgVAYFRGqxpgIjBGhYVxFBj2FMYEQIMZAJKYsWkiEyqibdOf0MmhtA1IhokDgCUIQkYhdrt0tjM/EjtgvA/4f3XX8h8CPQYi3wxvezDlo7o6HnMteHwX+GfBtc79TVza8Pdw0ImK1Q0YQXTbrPbg2stQvqVd6qGhoGk9tHa1TONEwGPZYO/0SFy5eYHH/QwxXluiVBb1egdECraGp4ewb53j5+Wc4depl3ve+d/Lk13wN48ahJYgY02cieLPqxnOG6NMNzI8C3wP8LVIvWt5U9nALH3eDAc7fkX+z83qLc4Z308cookAEgxA+lVSMYtIKmnHF/sUl7PI+NtbPIZVCeYmSEJWH0HLs+c+zvjWhLPeRlQv0FlfoL62iiz5FuUTfDHj687/N+rlnKQ189Fef58DBI+w7eoimtcnjRncnLrXoPnRqiN9G6q78w25bfhNiwz0c5EsXr11euNa2e4MueHqnXuL1xHacp3ZEjNfv+brAS8SIjJ4oBWhNVQdee3WdM8eeQzUnyOWEzc1NmtbSNi1N62naCusbqqrCOY8UIIVASE0UXffMZMgiRzmH9A0L/T7jkeWBJ76e93/znyCqjKLQCBmIIYAXqfgqxJ1Yaw9hek1/c84baiGEf7Pc82VlmDtkgHLO/X8P8C+AVcCJZHhil5TluixPSMG0ZyFEQMhI5Qxnz9Ucf+E51l5/lmZ8mmg36RsFMqN1Dd41BCdoncPGiPeO4CNRxpTABIgBovdIIUFKpDYgPdF7tDDsO3CEh9/+x7Bylf2HDjNYyhiWgoxACLHDct0JIwxTb6iBNeBvAD/XHYt8s7fkPRvgNbOc68vv1NxF+N+AH2RXr7eXBGPH70XAiYCSJb4CGzyOiFCBi+drzpw4wcbZ19k69zK+WSMGi3ceJQQhCmKMRDwxCCKRECPOh5QDyZR4xCgQQiUjipIYIx5HwEGURCfQmWK4vAKmz3DxKIcPv5WVQ/fSXy1Z6AnyDKKNqbMitvPjlKkLorhdpbvILtf6h4UQ//e5kMffrFFdVyK6FwMUt+7GmMYch4GfJ8Gidi2r7P0U4qy6EHGoLOel547zqd//A8b1mCP3voUjR45y8rVnaTZPo90mEocTAiUkIoL3Hu89MUZCSEaXvk//xhAIQqT8OUSkkvNXfLu1130foiCGlqI0oAzSlAyXH+bAfW9n9eB+FpeGLPY1mQg4Uh1HkLJmhCPOLsltr4QFQAkh/hD4L4BTNxsXbrc5774kZHpiX0tqpB/ufr7xY5h5kKnHUNA6vvzp3+bMa39EDJamGHF26xiuOouJAS0gColRGcRACKnLIaXsQo2IInnD6e9iiLjp3rvzDo+RGOPM+JQUGBWJsSC6hAOKqmKy/gyvb73O5rm3cejetzFZXmJ5KWMwkMTYEEMEDCIqEG/KTjgfg38A+CMSoOMzb2Zy8mYZoAFsV5P6YRIuz9/054sOnyk8MUiMyZhsjghtw1JvyOJwgZ4OuGoNKTXEgJQSpRTBR1xnOMDM2IRI8WOMgRghhEAQARUFAgmdZ9wtPk5bdCREUCKgjAQh8Rac90izyfobn6cdneXIw++iae9hscpZXc1BNp19SwTypuut17EV6m4tDgO/3YVEPza3Zrc1XtVvwl0muxP5PuBfzQWV6ubfPnmsGAVGZ4w2HWffWMcoQb9XsrSwgmNEDBGl1KxdEYlI5VNrLShiDDNjijEioiBGeYlng4iMKS6UUu6I6ztD7JyxFwohU+1cqYCWAhc0zmqKzOEmr/PqV9fZf/Qx/KF30NQDDhzMyYsWby0S82ZnJ9Oe8bCrGSrgR3gTesn6NhvfFMHyT7s7y88Z5S0wPwUxYnTGhYsNx18+i6jW6OeS3vKQGFoigTwrIHhciCAUzMGgpYzEKBFCzAyQMGeMnQGKGJLxxe1Jphgj2724ZNjp7goEFCJKhE/bsBICZKT1ESMlebScO/5FtiZbPPDAeznpF1jdVzAc5BB8yuRhLiG57WCIeZT1vyIBe//23FrFGzGAaz7n5Yv2dno+353M991csjEtw8x3FCJIjZGCU2drXnt9jWrtOHbtOaQfYZ1HiLS1CiGwwRNCmPNoXOL1Zl9EYmSWhEyfE7zvSigRP8URiuQBZ4Y7t5Yzw+3iS9Edx9R7KqXI8xznA/nCYe576weQ5RIrKzmrixrhIyFMs+/uvp3DI97strhHlM2PAN8/7wn3+qlK7O5ldoYWt8MA55veU+OzXUxxs3WsS29ZZTh1tuX1V8/TbBxncuaLZDSEIJCyW+wOQOCJeO+vbYDd8y/7XQgEuoRkumVf0wBTMXynASqlOngXZHlGUBJV7uOhx74eka2ysJyzb0miYwSfALNB+Evu3dtogNPHdM2mRiiZttNvwgB3c7u3I7OaNz5388YndjhOmYzvTM2J4+fxGyex55+jVC1SqpnXm2Kep8YhpZwZgFJq9vPVvua9mBRzv9/x8/Q9598XxCVlifmER0qJVArnQAWHn5zktZc+g44162staxd8ChOE6zL9Nx2Nbbq1m8buU68obtbwL9kdblOp5Z/Oeb5bEmdut7AkRmnWztWcPLFBHJ3EXnyGnqqBgohGqanxdK+ZW/jLLkBnPLO/zXmrmeHJy7dUuePvO7/S5+3++unWrpRECU2wkEtFMzrFqeOfJaNi40LNhfUWrzVRpq6LEPIyD34ji36dGfI0gfyneymb7fb+V/tcfYuNb3qwP3jTNb5dKvgxglaa9fWWk69fJFbnsVvPo8UIGw0xOowMXa92zvMBQl49fpplthF8V++bPm/aPuOSODF2kCxxSby4cxGmiczO+mGIERE8SnqIGU0bKErF6NwrnI6egw+8l/WLi6BhaahQId5ysOt1OpUfJE3k/citrBPqW3yQf6Vz134v7nrPw8td/CeUYjIJvPHaBq4ew+YrCDtGCE0MqeQxv1kHpnOXO4cnk1GELkab1v+6kBHZlWC2t24IqBkiWoSU504NNopU5pm+JnSJ0rSYPV+2mR6fiDH1lKVEKlAonA1kmWHzwgkGgxWGB55kfT2SmYxhEZBxeh4qRWPi1kxkir2FVdOEsgV+Yt4IZZy7+ebebbfJ/p1g3VuxBcu5Dse/YLvCcevu1+jTbFqQvHFyg7oa4evztJMLCBTeg+4KyIgp4iSdrBQpIZn+TojtSXA5/1ypuuddum1672nblrZtsdZircU5h3c+IaKFSLFg959AzLbneS94pZsuhK7G2K2EDxGjJOdPHyc2F4jWsb7e0rodFQBxQ5WRW5FY/oturd2tsB95C14/hc7/CtC7LcmNiChpOHN6zObGGOE2sOMTKBVBBKQkYfnmEpCrfU2tTojteA+mfWA/MzRrLd772TYcQuoZ77rdChBdzHelmGc7ObrUG8972+A9Ao9tNthce4NcOurKsr4ZiFF2xx4Q+G6u+U0zwuma9rq1PjBXG7sjBijm6n2/1B3QrIt+LSPY8/YrBEpnrG+2XDi3gXQT3OQMKmyiVNo6lRJ7ojiY1eRmxwAxBLzz1HVNXdd4Z2cghPT8lNlmmenaZMlwL+mG7EhwZjMnc593Sadll2sw/9wQPIURbKy9hp2cxwioJp7RxCOE7oCO02m+N/Uxre0e6NZcpkMX4mprumupay4+v5n2jQf+MfB1bMN5bp3jEymiqBo4fXaMbxqkXcfV55F4QnDd9iW6LHFvRj/NRJumoW1bnLNIKTHGXGIwRivyTKHUdltOKolS8jIEzF6/dhruNCGZelUpJQGNj5FoN7l49hV0rIjOMh47mjYgu3kTGe9IVjIFMHxdt/b+ZtZd3+RB/NmdGa/Ykble3YXuMj0m4gwXBwIhYWO9YbzVoGONby8SXIWSU8SK2AZl7ZL+TwvLYu7nS55zSYdCEINHa4k0GecvjmjaSK/QGGOIoUWJBBhw3TyxEpcXh8UuZ3YlEOr0Jpsel+hCgxgjSkYmW2dx7QYyy3BOU00cRmUp9on+NmbG8Wopy3xm/IfAL3CDWEJ9E2jmh3cUKLlesp7LPzoSZUAGnfqxKlJNIptrY7Sv0XGLutlES4mQER116r+majOzku9lq7+NQp4a4WzLQ6aFJBKCwGQ9Tm1s8lu/9UkubFomlceUim/+5nfx0IEh+AlRSKJITbnd2Bck4orNxJ1e85KEJaXkaBHTULwQBF/TTtYpzCoES2sFjY2UmSTEcL1g4Js2wLnT3W44RL4AvMIVUNVXs7Eb2YKnDudfAsvc0nFskZAoBKL0xCi5uFbR1g2SBttOCL7BmO48BZcVjHfrYuy6FU6TkJlRQq41ozbyY7/yGb7w4gm+53u+he/49q8l6x/i9z7+EidOb6LyEiEjSki00JcY0F4SIHldheAEmh2PNpDCpZAjeJrGpj6xkneqNjhvB8udLdyQHchrVcx3fE3d7H8JfPM07rveOOiqSUiQEANCSSYTy3irBe+JfoJ3EySeGB2ReEkH41odALmjEL2zMB1jBCl49fgJ+sUBPvihb+CFl15k48I53vHYCq+++hqvvrGGNgbwqbyDTDDYuePYafxcYSu+4t/nExUSAeZ4a53gxggc3nus9bQ+XNJmvOXWtbc1m4Zi39zZxCwe3GuyKa/TWH239f4v3DJM386KS6p7+qBY36yxtgE/QYQWvEV2eD0p1KxbcdWvbt+4/Pc7SzNgjOGVF16gPXOSP/ON70bGFG99y/vfytEDA7JMo2XyYmo28CR27xtf5g25LBHayw0pBXhX0VQbCDwxeGIAa0PH0nDnXOCOrfh/6WzjuuYJ5HW6XNm52yG3hQmFlM2iaNvIaLPFuQpoEDEQnUNJ1ZVD1KXcuXvY9i75kvM/S4zWeO954u1PEbTid37742xMFOdsjx/+V7+MJPL2x+8nBoeWBiH1Jd732luw3HufdMaenpr1WkaCT9eAkBA51nl8jNwFj+lWPOxs47ogd3qe4/gqCcR06/0rQsy2Xr17MrFLnzXuHuJGsdtvHQjDZKsmtBYRW2JsEbFFiBZEApBKGS8JwHfbihJgtMsyQ5gZ3bSor6TCdeUPITTWWh595Cjf9CHHr/3mJ9hqFI++5SGMEfzpb3s/+5cVtm1QxiB9Otd5iFcIodvqwzSfIEaRZk8Q1/RWM4OOMrE4yIiLKaVx1RZiOYJwgCU4jbMCU8RLUdlXe/94HW3QeN1ecLoV/6WuVafENbLiGCPi2Ia9Vk9wumJLJCLtAzu95zX3+T2fTEIYu6B5/fV1xhtjYrMBoQa7Tjs6hYwRH0AJfwlu70onOPs+hLmuR/pb6zuU9KwbAUSHyQwTqzm7tsWwn7G6lFPVNdYFiJGqqog+srW5ydLyEv1ef3uAKUZi9Jd2N0JI9YFdtt/dvCgClBAok2JMqTKyfMih+74GU/ZRWYYUJWVf0e9d/Sa8YQO8/sc0+z0LPCmEWBd7GOjWgl08/+6x338FHJoFmjt2jFuT+AukUtRjR1NbiK4L+JltN6lvmzzb9M7fywWNO7e+zuPIzltNQaIhKKraogg8cHDI+Qvn+eoLx1lc3Mfa2gX6vYLxeIJRKY5MIYG4ar9XCnFND7jTGOmQ2VKlMNt7T/RTfhsAR3CRGHQ3hH/HH1M7OdTZyn+7l9qgFuygrI2X7KvTus5bgb/bfS+vtuDXk5XtNFzRIY6rKg2Hy+iZUhEkIsnusGInj3CFLPJK29vOgpYUArq2W1VVbG1tIaSmcRFBIM8MQWqiKjBZweFDR5ACDuzfT/AOrRTed/gUpeYg/OkgZzVHKbsLKS7vIe9IZCAihWY8HrO5tcHi8gqLi8uURS/dIN2MiZSpg+JCJNdqNm5wrWDtdmXMO2rEf1fAT7JNhHRFyI6WbIOsBdt1JTHFMaUX/zckuq/tDGfKlbfjxISQew4n5C4WaYOgbQNEgRAuZX6Jp6AjDp96+7jrZ11v9Cyl4ty5c9R1TZZl5EaQ5QZpdOq0RslyTDyCCBj0SrTJialaNEPQzM8WT++B6Vjn9vXcxinOZ8XTBGV6/axrmUzGCAlbWxvECP3hEkJneDK01CCTtw4+jQu8iexb17qkU2q4/4YEz7vqIul5730phirOeT/x5zpXJOeNSortC321RCay4/p0ULZtqmYx26qqNtC2bSIT6lpysivIRqUgphqc6GpwNxPPKCkJwMGDBxPoQUlCgEntOLt2Aak0bWPJTE6WGYiBzEzBABIpYiIyF9uI7ZR4yJkXlN1Fmr9eIGZGOA8V2956A6E7zyw3VNWIE68fY1TDwUNvRap9mH4fpMSH0NGF7NTGEbfd0q7RKftzwD+6lhfUCrZjiHjJVjbzfkKQT73fNkhzvusbr32w8coucW5jom09eIfCd2AjRcQnrJ1IRjAFNUbino1v1xhtLu5yzuFcwlOYzLC0MOjACQKtDapjVvU+JIiWUKTcdgoi2DasELbp94TYvkaBcHnfWGyrLaVu3HRL1zjnEFFilCRT0I5OcOGUw7nH6HOUrGeIWoGQSBGIYcb3f104mVvM3Dq1m3w3Lxh3vEdKQi6HrkohxDT2+3N7if1u1cO2oTPo0Nl82m6lUogdu8yNHsts8WViLd2On6aexLK0WHR8MYEYa0LUM/R02mpBxth5OmbbaPJG0xlj0b03VzSI3bomSim01viwjT10ztHrlxjjCe4C0ffxTUHMBoRgUHcL1eh1ekEtdsevzMd++bWq21eSQ9hz9tu1niLgnE8wdzxCBKLosHmAVJLo52RiroPyVuyCWuk0DGZGNd+N8S7FVVJMt3p5Sc4zjfVC6DCLsyw6GbT3YZvcKEZC3Ibxxx2UIPNG2LYtVVXjnE84RV9vH3OU2KZmcQVktEhv8NbhvcLouc7PjrDoNiUce4kFL/OCO1+vd4GUTdPphzoLfpNmAhMiOc6U2/xcsrENU2LuIoubvIjzE27M6oN02/32c5iL46ZG773HOY9z7awYHULofncpcnqnAe7MhKeTedOaIQiU0pRliVKKfr+P1nqWYUtMOsYYCN4Ro7kdXdFb4QVjZ0P/A1dAy1xqgPESMNNfmfN+t/3sYoTQNdi3i5LbtCQznNz1341XNEApZeoty0t5YKRM0KwUzyVPZF2YxX/OuURaFALe20u8YuiSgmSn2ywLcQelxyUGzvbWbozpQoFtVE8IaVgpioBU3dCNlIQOlDu9KW5/6nHdeYrvbOivAP/P3Q5PzydPUSBCOr8B8AM30C/eNR3ZSytOiDSQE2LaehUQQ2KXQqaMWMmMIOqOJi0mhtI9F31Et7VvI02CkAlbaCTW2plRNcHhnJ+bCZkaVpgzntTxmG7d88Pvs7gvihnWUBBndc8pxQcCXAgz7zf9V0rQ2qSkSyQmhvWtCVluUFlNr9mkL/aDSIxfrm4ReZZClmm0GW9uza5Y593zTZ4Urroff4BERjruVn32NvoKPb0/DRx8s7zfvJGkbsyUe2U6hKMgKvKyT/AN3jYzV73zOk2RLVNj21lkmmXQMeBDpG3r2aSb64gqQzdmGMJ23Wi7h3xp52K+5bbTq6Uyi95+TndMUsoZKaaLyatO3yvPc5RKzkNKhfWRxf4hVvfdx0abKN9Uvsho7MjLiM4zqsYRt8YsLg46rZJwt3nBg51N/Tt2zBTrHXXg0Fnt993MVrrXIxOXZD1JyyONYIZ0n3TbkCeCNNTthNPnz7CytESvHOCa8RW3HCHnYsVOpyOEgHWOtm2w1tE6j/X+sgRqu7UWr7iF7xy7nP+aejLmjGF+0Gnq7WLc5plJ8aPr3iMjzyURi1KSi+trLC3fy9EHnqCqIpEMS0hjAU5QZIaqatG6pd/PunrOXadr/X3Az14WA17SskythkeBb2BGOXrdPmyXPuy164MSkQgjCR0LjkivkxqiwHvL+sU1NjfXWV5cQMpUqsiMoWmaS5MEIRAylW3SXK+jsS22tVhnExupgBDn2A9iuAzYsM2aOm3l7TJQNJfpXg0YMd8vviQG7DLt+SSkrlucDeSlQWUQYsvzL36W+0JkceV+AgJvCmLMqJxFyoAxOU3rUdqRZ+qmKxM3mxnPNSSmmiXfADyysySjd6nd/Jk5N3l7q0u7FKRlV5iVIjX6nU80GfVkwvrGGuAI3s30vMqi6BIDm7CESuEjWGupmwbbtljnUhQ21dTq8rMoprpJXbzW/X4603HpIvqrFrXnjSuG7WQqecCUHuwkMppm2AkmJpFKbocIQSCURmfTkEIyvvAyubCocoCrJXmxSixXGDWKElBaYa0nM+puSkamJQ3d2db/dokBihliRoQO//jdV6tyXHsIJl611C7micU7hvhphihkIutGQJCCKHKEkAR7EV+PECEiYxpYMioBBZAabXKcj/gQqJuGpm2wXaYqhAAlu9NNba7t3vcc+6KWs57q9n9dzzuSOh8dpjDQxYkxzvRDpoPuxhQYUyC7LVbOYsUERZhm0U3bEnzAWjdjaA1uO9FJTA0GkxnyPEMbTW4Ek82T2IsBlEQsrTJU95AXQ4zLUG6AzEu8EN2lFd2wVhpyEldcn6t6sGviGPcwiDZ9g+8G/sn8Nqy777vWungUxDuvuv2KaxlfvOpL5nuel7xmRpvRzd7GDG8F3jeI2DDsaS4guvJIim3rpmVSnUNrPaPPaJ3bbux0442pKOy2GQzmes+XcJlIkWZ0u5si+oRATuGoQonEvFWYDGM0JjNomc0MyDnHeDJhfX2drc0tJpMJdVUzqSZsrF1kvLHF+sYGTdt0bTNwtkUCWYfIVjJBt1zX7syzHK01UYCXAaNzNrcmnD6/xn1veZj3vOMJDqwssf/APew//BArR+7jyAP3IE2BjQk3LiMEceOtuFvgTafb8Dt3bsN6x/b7XR2S4U3VlroEuq4c2FT197YihgqtQQqDENC2FZPJFm+cbGlaN2tbzd5HSgi+Mzw/F/xvdywui12m7bgQE/RLxDSUXpRkWYbWGqk0UgqC89RVRT2ecOrVNzh35hznz59na2uTra0Rm5sb1JubSARaKUKMtG2LkhLXthhjOqaFjDzL8VKmfrMUZJkhNwa0QucZRhvyIkcKSSDiVaCpLfsWF7FNy8vPPE8Yj3nqiYd4+suf453veg/yuZJHn3gbT773G9DlQkLL3B1FQt/Z1ncB/6+ZAXaL0DkN8eHZMMKb3L6JnbqRUMmhN01DCBVKNMiY6HGXl5dYXh4mrLePZEKlrS6EtCV26GYhRLedRpSUs2xnvrArhMCF1MEwSpNlGf2yTAPoQhC9p6lqLq5dYGtzk7W185w6dYr1tYtUk4qtjU1c0yBc2o6lEGitUUKy0utR5AVKKZxzKCmpbUOUkUG/Pyt8W2tp2+SJB/2CXi+nVxYYo5FK0StLhExdkf6gT+MtREFjPb2i4A8+8VnOnLrAO9/1bo6uLHLu7FkG+ZA/+vjH6C+s8NjXfC2uS57EDn92B5Saph/44c4AZ0nItG93pHOR1118vmWtkEgSj8ZCbFCyRkWPCAIpNaur+4jBMd7cJHiL6MZfXPAzKHsMcZYJp2JuVzTujNSHkGIqrSmKMm191lGNxrxx/HXOnzvHhfPnOHfmDBfW1rBtS9taZEg96qIoCSGifWRhuIQQgrquaZomacopWJu0GC+6zk6kqRuUkpRFwfpoE9tRgXjn6eUFZWbweZpRqaoJrVUURc44elZXV4lEdMcpXeQGT6A/6HPq9Bk++YUXeO3kee5/4CB/+Hu/yzd98IMsLvR46dkvct/Dj9NbWsVZd6f06Xa25uhs7AhwklRKnxWf309SqXyTi89z90dMANFkjA4lHTJElDJEkTLKqq2xPiJUjpGRtm0um6sQUszVGCNKK/K8pCxKMpPRNjXr6+u8/tJxXnnpJdbOn2f9/Br1aIK3DVIKekVJluUUeR/dU9S+QUhFay1t1VBZy/r4PD7ILuuNyeBiGiSy69V2RhyTXp0Sm8kD+zS8lGUZhIhzDVU75uLmBbJMUeSGQb/PocOH0/yzkDR1zWA4JMszeoMSlVcsLpY89PA9/PZvf5Rv/KYP8LXvfz9r62vcd88B3nj9OOfOvsGDy6t3S4tuWpRe7GztP0AC8UyP7UPz2cGN147EnovTl0LyUwyodZrTUCF5vkQkKfBR07QVrdeo/mGkMjTjU4SYYi1BYrL3vkVoRZFl9MqSIiuIBDY2N3npxRd4/dirvPL8C0w21tlc30QgyY1BS0kWA7os6A0HtC4wqix121K1ltF4CyMluhsY0kLSUwqpE4RekTLOmFRqOsOL2+UWEVAqoqVCSwUhYLTBFDr1rITAOocA2knLemsJUmBby0Kvx+LSEnU9QRnNysFDxEnKpN/+1ON89aXX6OUZ3/TH38vZU2cpZcHp82usnX6Nhx552wwjmMZZL69W7DbTE26PxcY5W/sPUw84hVp98M3efncWqAWJkcooTSs7/bdgaL2gjRGRH8bkhhA91egCIXi0kjhrUVJSljn7eivkeU7btJw5dYpPPvssrx17lTdeOcHmZANtoNSKYVawOuyhTJaYBqxn0lpC67gwbmmtxbYeGxIUctlociXJdJKGMFJhlEB2Pel5NXQpPFLNzQkjQMqZF8+0ASJGG4qMSxAvWmt6ZZ/aeY6fOsWJF16hVZKD99/L0sIih7ShqSpWlpZ44smnuDCuUVqwtblJVY0Zj7fQZQoLNjc3cS4Rt8euFy3ujm34g933Xnfx3z3A47cu675x52mUQkmJkMnruZgTMRilcUETogW3hq/OIqMnM4Z9S0nJfDIZc+LV13j6S1/i2LFjnDl5iqqqKbIMBRxeWaBfZKgowMFmVVNNLK5taZsGJSAjeTeVaaRRKCHITCL5N1qjpEDGxGKqRRoMmJJezmg1tGRahrtkID2KxO/XhQtFmWHMdKbYdjMmmrLQHF46wFNPvY2NuuF3PvNZfu+Tn2O4dIB3PflWTF7y4AP38eFv+hD/+0/8HE3rWF7Zh6BgNG4oVIMxmsl4QggxJXYdplLcQgDJVZdyd2Of/urxLg48obut9kkS82V4Uz3gjh+EFDjfMqlHBGkIsUBkJXiJ8x7navCb+OY8K4ualcF+2rbm1ePHeObpp/nyl77I5sWLuLahzAsWewX7FxYoMkOmI0alxv1W3XBhcwNXOQqh6OeapV5JqSWZlihpZkVqKQUiBKxIMHlBQIrkqSUJFS06Jc2pQPZ0GGlWd+xqm0HGGSeN8x5jBJk2qVitZCq7mIwoBY2GXmE4tLqPb/8Tq1RC858+9SVOn/0Ex0+8wTd+8H08/paHGI8r8rJHUfb4nd/5OHUz5p4PvI8DBw7Q2jYhhkSaq5kferz+QGpvr52XpZC7v23obO1J4MS01veO6dZ/OwzwajOzl56xYHNcUbsarftIuUITPLXbADeib2oGZYMa9BitV3ziYx/ji3/0eU6ceA3bNpRlycrCkDJbwlmPkpJBr4d3npFtefncRU6cu4h0joPDksP9nGFuUEQyKRiUOUoIhFapl99ZVAiBgjQ8pJRJ/DBKIkJABYhd6ciHlGUTE/n4tBAuRepFTNn7AxGTZWkrjjHxjQuJ0kljTorUBcFoYiYZqD7veftTnDy7xutnL/D5547z8hvnObp/kap1rKwu8fsf+30O7lvmgx98HxFP07YcWVoiyw2N83AFhRlxfRvUroNguyLTr/w2Uxt7B/Cbunvqu/fUc7nkbhBXzTLmoVAhbh/9fNtGzL+XBGct7bhCqR4xW6GdgKsvsJxVDIeB9QtrvPT0szz9hT/i+KuvsnVhi15Zsn9lAUXSYGutxwjJsC+onGO9srx6+iKvbk2ot7ZYyQ2PHdrPPf2SLFZoFdE6o8xz8ixDxIjusIm+Y1PwIeBtQEmJNno23SZRqewzHSfoDDDM0f+GkJDdAoEPEZUZlJAYkxKRQCT6FIh7rchFjtISfCQ4QTFYwoXAwQP7ePLRh2itAykZ1y3HTl2kqSq+87u/g33LObF1vOsdb6eZrHNs8wT33f8gQgu8Dd1owe6GMmvSzYFyd01CRUKsXO714q7dvV1BCtuG8+6uDigM8ODNxH/xGrCsOIeh3/25AYVmY2sdS0tmlmicxMTTLJhzvP7KK/z073yUL3/pc9yzvIgMLWWvZPXowXRBok16cE1KJM5tThhbx7oLXJw01JVFhMgDi4s8dmiJQ4WhryJG95BKYEzqQExFBTWJAdV3fVkXPEGm0dD5GQ5EMlIQuBCZThj6GBNhuukYDYgIpbAx4mJCMzsitq2RyiCUom0dnhapDUVMN4AWhuAVvWGfhaUl7jl6D+fWNohAPRRk5YBTp85w4dxZHr3vYRb7q1Rb6zz3wgs88NhTPPiWJ6jaVC8V4crX/8ZqHPGyzGL+91ea2Z5D3D8IGE1CPz80DcP2uvfHuaOJNxAvzAe0ojssHyNSD9HOEtuTXDj1Zb7wpaf5pY98jGeef5YPvfftPHh0P8JVHRBAI0KLCIqA4o3NilPrG5zfbFivAhaJUZH7lkqOFoYjq8vs6xu0qxkUGdoYpJBopdDdpJtJg6pon7hn0mScQmR6xuWcBqRU6oCo9HwZwVqHda5DcztQWQIGKNWhbmJ6TnD0+z0wkiaAiAqlBZULZEFhg0J7ST1piJubFMMe+/YdZHFwijIzDHo9+qYkK0raNnD+3AbD/gJGC7703DMs7DvKH/u270KXC9SdAd6KXtyVsmgh5Y3Y8EPAQHf4v+E2JOYa7mzOq20zAMSrxn1XCgRCB4iRgPeOIstxG1tMzr/I5z7zuxx/6WUuXJhw6tx5HrzvXh46ephB5ih6RdqifCT6jBA0G7UjKM2Wi7TO8ujqIouZZCHTLPcKMhUos0iuHHlRIJVEK02mTeJ36WYypmwJSiu8c2S6g4QhCTHJKEBKSBBJOdM5j5ij/Y0xYqPARclGXTNux6gsZ1I1bNUtjfMMhh4lFbW3xBjITep+rK1dYKFueeSBIT0EfWWwLlKUfQ4dPEi/V9IrC7xMxflDRw4TQ8NLL58iywKDlYP8mT/3l9l/+D6axneFfT9Xa70yJnM3XZNL4714Wf/+SnXEPYSSQ+BRTWK7ymYFaHEdHnCPfxdXOYzpXSURCOe5eOrzHHv2C7z8/MssLu3jxPljCC3YN+ixnCmWh6lyJB2E6NkcNayNGs5vVZxdH+GrLd59/2HesrJE5mq0SDIMqswpMgMCtMkR2mxzSqtUHFZdvIeUGCGQyhFDxMiACxExQ8ak/myMAe9sN/W2TclhgTrAxdEWa5OarcYS5ISL4wkTG6hdgItbiYlBdEAEnUo6ZZ6x0BuTDVfpr+4nbxuWdYZEceToIR548H7OXNxgazRi+cAhUBlS9njh+Hm+6Vs/xHf+2e+hv3CApnYooYjRE0QkILlZDqN57JC4eXbqDDigI7xvLld401pwU2qO6e2ghODcqdf46le/RLU5xpQ59z9ylFPrW2xufJnFBw+TG8lwOCC6Gm9FGomMDWtbNc+8+DpBBN7z0D287eghwqRG5gVIQYyBMi+7jFOB0khTEEWi+5WmQGidpLOc65ImiVAS59tUv5MJlR1jTF2PDvXuukm5NFDVMSeI5Nk26oaNxlFFaJuWKNNWHBEIoWhtSCjwGPFa0i9zBJrxpOH5Y8dBat6zssykqkBArz9k/779VJMxUipCiLSuoiwXOHex4h3v/gaWVg+wsdGSmel0bSccdlPWEmdIzkuktiLX7QHj9ki2At6n/e4x5KXcetdIPa613V7JQ4rY6fkqiXctG6deYHN9xGuvneX5F1/h5TcucvrCiLELSKV57uVXWDn0XhaEZRIElVVUznP89BptELzn4Xt459F9DHJNo0GFNGSusgKEpvWOIDVeKqLSOO+obEu91dDYCeOtMW3TIkJgoSwpc80gzyA4ilx33YSUYEDCDoIkRkkgYH3AxogNSWUpAEoLVPDkUtI2gYyAMRIfAxZPriRFnmEEGBFYyAwLvQIpAy8fe4kmej7wxz/EkcFRSt1jZXEfoW6QeZlwk6RrJ0LLS199gXe/5x1JBV5sD1TJGZPOFcYFpLhqGWWbs3r3UvZNGLfUwHvudAdESIG1LefOnUXHgGsmPPHYo3zl+Zd4+tmXKIs+1kNfZzR1S7HYZ3OyxemNCR/94kucuTjhnQ8e4cl7D7I06CcUsQjdWLEkasOJcxcIUrE1nrBZWRrnGVct46pmbWuLcV3hvEcCRsCwyBjmGYtFQT/POLJUsDLs4bzDB5/o0URXWFYS4ZPMlwueNqREIzeSocoogkZLSS1rYs/MDFcpTZnr2TUQEcqyoN8rWBguYIVmUo/4ype+jNYZ+ZGMffv2c+jQIZ49/irF8irKFHjncN7x0ksvUdeuS4xuMt/dOTA27SPfmvGSqa29ZxoD3qHHtgyr7QQAtYR3vuNt9JdWOLO+TvHSGwhlOLu+wbf+ia9luQy0wXF6fcxvfuZZTm623Ld/iUf29VPXoz9AmJTZiigR0vDsy8f56mtnqG1gs2qoXKQNkYm1NK5JykNSpyKzAKMlNiSP1lqPkamU4qND56lXLZSkdQ7rHT4EWucQWuIbS+PSsHpuDCpErG0hODIdOy1jhVIarbdnN3wEoVM2rHyL9hX9wQJHVg5z4J4HyE1G6yxlv+Tee+/li8+/gLcObVJXpSxKzpw9w+bGFsOlJXxwe7YEEXeP9y6p6V1Wir4ljwMamOx1K90L4PT63mNK5JhwfOPxGCk1QsB4ssGRIwcIrqHsL3Di/EWs9xw6cpRnXjnJ737hBc5sOvYvLPPgQsZD+5fpDReJeYnWCcoePGxNWl49v85FFzl97jxRSlwUNNYxcUmV3ODoZ5phUdDTkkGuKJVimGf0jUIRKLOUpBiVwOPOOXxIBjhpalxI8WWAGUdMU9e0rU3lGiJaShQRSUTFBDXraiQoKTBGYjJJkWvKTDAoJIs9w1JpyDqCJqk099x3b1LytI66rinKRF7pup8XpEgyKrsMTF2mUcfucz6Xie1EuA38gxMN3H/HQQgR8jyjKEtePP4yDzz4ICdPnuDIoX2848m38vzLp9CDRX7zU8/zlWNn+Mrzxzl5Zp3VlVUO9gre9tDD7F9dpFwYoooeWmtEFIw2xjz9wiu8cfY8k7bhwMpi4mgJnhAMzgJSkmeJ/qxUglwKCqExIlIayFWgzA1GSZQU+NbSuKRT0raOqvVMqoooJFJnabomStqmYVxV2A4sq5VCCIWSGqlSay6EziOqpPyUKSgM6E7x3dcT2tE6o7UzLCyvUpQFobHce++9DIdDTp08yePveAeIhArfv39/Jyl2nXWRvc0p3Urzm777/Ro40t0h4noa01dxh3s8ggjRd7rLAqM1y6sHyXqv0wTNmXMjPvm5ZwlRMiwj0VV86aURn3nmVbTW7F89RGkcq4VkZWWIGi6iihJlCrQyVJMRz7z4Ei8eP46MgXuWFun1CpRODKQhWISX5EYjY6Ll8DHirCOGhon3jOpAPzO4WIKC4B0mJOJIH0mJR7BJWFCEVEWVGhdaKtcwcTapvKOQIr3eyeQppUolHSM1WqYCuFKJqya6lqaJiJDTVBVq6wKjjfOs3nMfrZQsLC2zOOjzyok3GJQFo2rEuQtnePiRx+j1+oTYohJOZ7YmMXRzMVP2icQZN6WsujzxjHvn374JAzyiucXjKuI6I0CBwPtAlmUMVw9isgIhJYeP3kNW9Di3do6ve9+7+MqXnubp546xun8/InjKfoYfV+xfPkRZFui8QOocZMbGxhbPPv1FzpxbY3FQsDhcpa8VbVOhtUDkOZDRBIdUgtAIbJMIYD2KNkbG1tNay2bdsDGpWa4LVvoZS7lhaXkJaXKKtoWNLUSURKMwRc64sjQhUIXAxEecixAalBSUeU4mNPgpOCCiqRiUJbKxqAoKY8gLRS+Clhnj8RZRCex4nbaeEIWhLHs88sjDvHr6LJujiovr66yuHODA4SPkeZ5kLS6/3S/JYUXkqlHdm0T2G/Ud23pjuhOjSAPBLfDgE0/yhc9+gmPHXua+++6jX2iOHlpmfXPC+bUN+v0eJlNkUuOsQ0XBwYNHGA6WUDJDyAwXI2sX1yA69i/36ZUlZaYIPpFMBh9mJYVxPU5Zq1fYALYJjFrHha2acVN1i+bpZwGhBP1ehsxysjxned8+Bk1LoTLOxIs0BAaLi7i4CTqj8ZKN2uF8TB0UqQhti6kj1jusTR2QXqbp5Q39MkeKiJaW0G6x0iu458AB9i33aaoJo42LNJMR5XAF7yNPPPYEX/jKszTVFgZBOxqDcAQ8+IhQcNfxZe3ir/SNutibpXuYysyIGBEyYB0MlvbxbX/qu/j5n/lpXnz5GMtLQ/ql4Y3XT7FxccJgcQEfIlIabNuyMlzgwOp+er0+1nqEMPQKzerykL46QnCWYFtkcLhgcCHifaSxSR8kUwUhODZqx4Wx5dzGFltVQ91EfIwICYaI9y1GRPYtDij6A7QxZJnBO4dvG1SMCG+JtqHUCcRaVTXWe6LIqKwlH/aorWNiPUIqRrZGAMXCAL0w5OTZM0xGm+RFxkArtjZr6joQwn4OHdpHVdVcPHcak/dBGu679z4euu9+jp88weLKPvLeEg899Aj9vqFuDMG2aai/69J0GgQziTLmiNQj8XZttdd83DliV5FwcQqPjGl00DWWex58nO/963+D3/i1X+bpL36OfqFpbGAwWCDLDaPxGOcBPFoZBoMSJcFJQRQSJSOFiehCY9uADWnj0Rga73Ah0NjA+uaIU5sTTm9OOHVhxEbd4kjoFqNMogS2lgWjyLOMCGxuVQQf0UoT2wYtInmnH0fr8ZOKftZjITOUSjLIC7YqixSCpX5Jz7acOn2GEAWZTHILS0ayoKBVkeGgJM80hIgRGc245dzp8xTasLh0gLYasblxkV5/hcXhIg8/8BDHXn2V2nqW+n2++ulPMn7jVZ56/9dx3yNvwTp3x/PLN9UAxXV0QqZsCMTkCVU3NDO2jpVDR/gLf+X7OPaBD/LlL/wRr//qb6SSeQxomXrAPngyJci6ofFoG6QGowJGBjwB2YncuBioWsfp9RHHzlzg9PoWG6MJY21YmzRsjZukviQVRkgOri7Rti3WW+rxCN1bZXVlER0a2rrGtTnjTYeP4LxDyjRKoAWURrFYFgwLQxst1khklDQbG+RKcN/yIr4LA5RS5NUIV29xdFCyb3WJTCkubmzirE8loVITvWWytcnFs2fJesvk5QJCGh566EHyj/8BoW2pN8/xuc/8Pge+9Zv40pnjtN/6HTz6rvcwqVsQOrXR4i4IJnFr1vhGY8gbTkJ2Z0S6woTVLlDIaf0pCnXJQSsZqKxDR8Gjb3sbR+9/C7/+kd8DJSiyDFel8UgvAkv9PqXJsTZilEaZgG/HBFcTgyc4R9U2nDxznmePneLFN9Y4XwXqIFBasrycsa8s6fmIRqCkIdMKXY0piMgioxzm9EuFkZaeAXC0TUMm+4naI2zLfEkh6RUZw4FjqZ8xbht8LjFBoqJCdWy/qiMhUjIxPhSZIc8MrrFUboIiUuaKIpOUPUN/2MPZCZtnz7J64B6MknipuOf+B7j3vgd47pXjrCxkPH7vEVb6BZ/+jz/P/gOrPPrO9+LwKHJkdMjpfNxOtAviqmHVbdya72AScsVDkhgiMniaVnD63DnqpkGrFM/46OkpDT4mFoEso3UNRqdaGM6Ca2nrhrNrGzz/yqu8duYCWy0sLi+zciCjMIphqZEBmqohDgqsCzjvaZ2jcglokGnJgeUFCg2FjPTzEqMzhExSsa1r8TEJZ0uVSJWU0Rzcv59T59fwHtYnDePa0jpLCKIr2XRM+1IgSYysBIdT3YipkN3ciaSXF/SLkrzsUTcNFy5cZPFwhSwkw+GQx594gq++/Co5kiff+iiimdAjsvHqq+A9Ck3mA16Kuf7wpZ5qSsgpxRXkxMRtS4+FJk2oH7mZlGl+EGW3N7jWhNWlwAeJEI4oE1vmwsKAew7uY3LhDM4HhMnxHRReCYFSgmgDzgWUBd/UNFXFxQsXOXHiNFuV48g996KFIC9y8jxDEWmqEXVtqVVO1bYEHLVvaGwLUVKajEGRE9uWTOcs90qGRYZSGmUKhDYE1+CnxOTeI13iohkM+jxy//1E/wq50tSZZeIilQvE4BPUv6NrU3iUkmTTOqAAowR5N5EnYlLDVEKSGYMUiXouLwTVZMJjTzzO4h9+AkXk4NGDnD7+IssLA0avHaMZbyD6y8Q28d144lWFI0Pcg7qIEFfEiF6CN7w2PkUAJzXw6s0a4DUhD7vJql4JHi67qRGZ4PH12ZM8tX+R009b1q2n3+/TNBYbIkVR4LxDKIFrGiQWWzfYkKjSDuxbZbC0QhCK6FsmVYWdWCoXcSFtACIGog8E55ERCq0pspwiy8iEYKlfsG9xQE8lSo9hb0Cv10eqCO32kFHd1ujM4HwgK0sOHznC1uYmnD5HIQWZ9wyRWOvwHXBhKjid1JJSiy5TCqUSebcSEL0nUwYRYbgwIC+KpBnSAV/371/l8OGDLGM5cO9RzrzxGghFdfoEF15/jZWnVvB2SnYRrwaR6izj8ox49rtrGta2Ce1BDFYAr2rSiNxd85AzmLVE+cjLn/o4D5WSDz3+CL/95WewIaffy4mNRquE9fMxDQwlLJ/EYdAmo19AHjy19VgpkWS0jSVGi3ee1iWIfa40sujRFyINNwmPVophWbCYG4ZGUGQ5Osvp93rovKC1VWJyMAalNVmWd6pKisZ7TJaxurqPuqrZ2NrEVi0yeIyWBCWpGp+Y7iUdhx/ojhJ7Om+spUjoZ+soepJerw8wy26FEOTa8PYnHqc9fYIsLyiKAU3jyJoRm6+f4ODbvoYJCeofb9K9xLn/7xYXzseXcm+A1Z4m6bve3IHtIhOwg3UDcSn+4IoXI8SIYkpO7mlPHuf4J/6AD374OxjXm3zu9fM0xuC9ZVjmSKNRtetUlBKqBT8VtQYz1W9rAsFZpLPIYMklRJngV8ooYpAdNN9TKI1WikxLMiVQWhGQKf4DhE9AAhE1Whm0kGglUSZL82/Ok/dzRKYZDHrYaoLTGeOmRcY0vDTMDFJJHImZf0a6DuSyowtRIg3L54YowWSGfj+BLdq2Jit7jJuWJ596K595+nOsHTtO2e8hgkRWga2XvooQfwrjNVH7VPSPck8p6xXLvHN6KlfLjMMc/vAqScxZCXzuVoaX8Sqtnchep+sTXNp5R2xq4mSLrVPH+fb3v4P3PHwEWY/IjGE4GKRhJt+pK8U0J6KUwhiN1gbT8b4YBIXJKLKMQmuMlGRSkkkwBHpaUigY5hmDvKDQmkwpjDHdkLnE5PmsfGK0SeOaPrFaCZLOiZAyxZplj8XlFYp+H5FnSJ0hhJpNiykSeaQSAqMUpuOMSd9riixDKgkxFZDLXj8ptUtJkeezMYa2qllZWCZay+svHyOEyKiqUc5z+rlnaasWtMKLu0BL83KT/9xVtVzvaI9GCIJ11FtjFsse7eZFCjfh6x9/kEP9nCLPGQ4XgDRWOW2vOe8SwEEqpFAgFEoqMim6rJDE6yIkpdIUUmGioFCahbJHoTTC+cQsGiDXhkG/x8rqCotLS+RFjtIaqfUlYokhJDUkOl04pTQHDh5maXUVVEYUCiVnAhTddpV07ZUUGC3RUqDVVMIhkGV5GqCSKrEltBapTJehdwCH1iJQrBw6ytZoi+XlZcrFJbRtqU+dob64ngTZgkTGu64gHTTw6VmucCtN/AZbdbKbtpNSMBmNqde3GCCJSKqtCffecz8Hl4acqTfJ8iwx4TuHUQopJc5neFeTdbzRzjXIKMiURuQJ+JlnnnbKmO8VMYYOq9dNbKhtLphEo5Yn0GpHZN1ay2i0lTgB25ambVP+3qm4W9uwtXkR2zhEEDgXaNomeU8pSMoNYnsmJqSuzpRTJstz8rKkKHMCApVl5HmJ1BnWefJOVVPgkSrigWJ5EWU36eU5+44cpjn2ElnbEpsmzSt3xnfTceCe1zVebVOd2tqnpzFgC5i7yT9LAU1VY8cVRiqcT/oZ9WjMvftXOHZhiyLPkwfMMvCJhFFpTZYXhJBIhBL4M+IJIEVi5Gy7yf8YQIOWiugDztmUcUqdFJukSHyEW46lBPSjrqtEdBccwQdam4AFIaY2XlVXqI2LrJ0+S3QJZLt27hyjqqFX5mk+Q0q0kLPsV3Sdil6vxLaW4XCI1IasKNBdZBhJ9MMmy2d0H8RI9InkfHO8xYnPf44cyQMPvYXPfuITLPf76CKHEIl3X0euBc5qEmH0FrB6t8AnplRnRurESNXWxCbV9Lc2NljuGZb6OWWvh5LT4WKJb1sypQl50TEVBGQMtJ3auhSuo/5N8lmm28aIaTRTAEpqvE+yDbULTEYTMp26GaG19BaHKKNomxq6TDUQGTc1CkE1nqARZL0F8qUF8nKLx0Lg+VeOcWFzxEI/UQxHPCFKjFIzIqPM5ORZQZZn5GWBNhqT5wSRxkVLrQnBEaIHEWitTcTu0REby+a5i7z63HOsfsNBWFpCra5gFhYTw4N4U3mndqQnYrcSzBbwggZGJCXDW2KAt0IURQHeeYaLyywc3o9/7VlE3SKMRuFZ7Rc8cs9R+v0hfnSRRKUS0VohhU/EQlIitCIrC6y3EDLwiQtCSYVyFhnT9g2yIyPqWLh8pLGWUeNY39jkwHKf8lCf/QcPsXzkIKIw+Lbl4sk3GK+t0QaPlaCCJOv1Wb7/Yfbd+yCt96yfeI237tvHI48/zn/89d9mY2OL1YXBVH0szaJIWFu7QJaXHDx4EI8n7+XkZZ82RJTJETojRmibmv7SMt45ZJ4nDZVmgq8dwik21i+ydvEsZmWJ/v79mDKnqixKhm7/FW+y8V3RAF8BRpI0R33stjRabmDrnSp1RO8ol/qsPvJWJhhE8BR5qv1tnT5DvLCGFgGtkwZHlhmUFp0cAxiTMljr2iQAo1Iyoo1ODAYqEQ0ZY9AzkcDE+WKdY1xVbGxusTUasW//AR589BGWVheJrgLfMlhaZP+RI/SGA8pBj4WFRYqyZP/hw9zzlreSlT1oa1wzIfYyHnzbE3zLt34zVVNT2TQjLJXuWFQlBw7sp9/vIwSUvT5RaqLQ9AYLZEWPcrCAzjKGCwszihDX2k5WAlrbYq3FVjW2qunt38fSffch1TTlkXdThEVnc3aKhvkj4Hu4KzL1KXYtlayGb3mUerjMUAgEnjMnTnD6lVeJosSQMs9UwA1pyFylfitSILXsKDYSg6rKEz900mlL7TAlJTrLiLGhbS0uBFrvaZ1PM8Nty8LSEoNhSTMZMdka4yYq1dsEaeZDyKSFIwRlr4cMli89/QyvvnKMMrYcHC1SGMnho4cxRcakqSnKjCxqhEy3XZbnSNXxDiqFzlK7D2U6XB9IrfAxpBJSljGuW5qmJuvnBOfAJ6P0TYNaXmJ434OzbgtvcgZ8ldpfnLO5GRzrS7cjE74Rpy3osH0I2tpz3zvfy9P33k9sNmjqhvXzFzERRFPRTiZoKVJXw1rAp+RBSbQSNLZOylxaQkz8fVonLyq6NpcQCt/pishumq21lqppCFHQ+sCkaXDece7COl/48lf53Je/whNPPc6f/vC30DQN9agbShISHz2/+tu/xY//3K+gheLeYZ9HDq3gm4As+0wmE1YWFyFAdBGRRZTWaZCo84YhBrxzaJPWKssSAFaIJDHhrEV7j5GSxkdC66irelavDN7TSs3yAw8RbCf+E2VSn78Lml3zNjc1wGdI45m9O5mIJMyawErRbcOBct8+7v/ar2X8xU8nWdXW4awnOI9ra7KeIYikB+JJ3kgIQXQOOU1QSDzMtm5msqlJMjXV7ZxNUq3WWsbjMa11xI5tfzAY8MILL7CvBy+++ApffOZlVvcfoN7Y5Pkvf4kDq6uMNkY471jdf4CXXngRtzbi//T+93Nq7SwLmeHUqdM89+IrbG5ukGcmgQoAnMfJSJZlnapWpG4aMpWm6DKTBBczk8pBUnehglLQ6eHJCNF5xlsjvHMECUW/hzhwgJXD9+DbkNpi8U13glcscHS29szUAGWHiHmORBp4UwZ4JYalvceAARnTJH7stOTu/cA38uWXv4pzlqaN1NYiAjQbG+hilRACkiS/mmcZMViEjHiRvIv3jti6xAVDGsuMRAIeqSSxK9RaG2hJU2vCSHRsWRkMyGPkC59/nqZx7FtYZP/CgLe/7TEQltpO6C8NiNJghn3i2hoHlwc8uriMLp7ghZeOc/bMGsdfe4PMSPYtDlAyIFRIhWkBtW0p8oJ0dKk16ITF4chFjjYaLyKZSElI1ltAmgw3HhFCjY0DhmXGpKcZHDxAvv8gev9hiv6AurJELQliB6no7ba03dc/ilSQfK6zOTnVCbHAxzsDDHdyK563fiHTtNq+Bx5CHTpMe/EEQXh8DDgneO3ll3ni0D6s82QqDX4zk131l/p9JTC5xrYWhSIKgXcdAExKWmex3iGkSLGkgIV+n9XhgIWsQMaUPYcYGY1HnD99jsWVYYJvaUNw8MKXvsSFi5toKVndV7HvwCHapubw/v3YYJGdTEOq/UEkzOY2fPAJhd2ptAeXGA9oG+JoTL64iFaG0WiDYujQRpNlBitBqIgpFV//J7+DxeVFTrzxBo+/+xvSjHLXggudEugddoJT2/p4972Rc0Hhx67SW37TK0ezIw6efFCw77EnqYRiZXlADMloqs1N2qpBKE1UqmPC8h1DfVJOmsqjxpDEYZSUTHGXJss66lxP8GHKmITSgn5esLwwZGHQp+zlLC2VLC2VLC8POXBgH71+P82gqIwYBBubW2ihWOj30ZlBGs2kqVlcWmD/gX1pok+bxAEjtxv6kUTlO1XRdD4NvWdZRgiBXq8HQlAUBadPn+6ukaBtW0SS9kb5mohn38MP8+xzz1Btjbj/ibel2Rk131+/4xGg2GFrccrhBfApYIOrAceucyu+oa851aPp+7Qucs8TX0MlCpb370NphWsa1k+fYby5iVCaxnukSMxVIVWSKYrEIJUWO+C9mxWhYyfdGmNMAb/WM1EZrSSDMmehLMhVEj+0vsXLSFACrwTBSGrnGNctG1ujriNjCEScjIxsw4WtdSyOILtxyR1K6/NblXMO62yKR60jxJi23k5w0RhDXVdopcnzHNtafPBooWiqio3aIssBm+Mx+x58hHL1QHdTTfVB/B0rcnTnHIUQqrOxT3V/8nIuMDwJfGHOVd41oARrPSv33IdZOoAcDlk9eph9Bxahtbx27DWkyWhsYq2CQJ5lTCaTzthS0C5kMsIU7Cdd3hASx8u80rlWmrzI6PcKCp3mOIQICU7vwFqP1CaBEYxk3FpGVc2omtB6h8kyjMmpqyapJQWPEpBnJhm5lDuIf0Sna6fJTEaIkaap8d5jW0fwHq01dd2wb98+QgxJa04ptFJEFCNRsvjIO9i0mvf9ie/gyHs/iCwL8GGW2MkQ73SVbWpTX5jGf8yBw6b//sbtKUjH6/ja5chDQCrBA1/zHk6vVTz17nfx2Lvfw9H7jjDo5QiVRidt0xLRWA95UXYq6YkYKAHYAhA60epACBGf2ISQEpRKcyD9IqcscrIsS/Kq2oBSNN5B4rdEaYFGELyjrhvG44oYoCyy1J4LFqFkQs50zJ9SSZASROIURCSPKztBxcSclXrUwntyoyE9HW9birLEeU9dVxRFRhASJwVb9YQ2Kl459hLnNjZ48F3v6a7mNlonImeAhNsRt89Wbyrac/nKTtOS35i3ObnDOn+xaxIr7qKHFhJbO+5553ugv4+nv/IMxb59rB5cQMcJbZ0UgarWEVAgNFJls2Gbjnxhpszug6NtG0JI0HhiTGSPSpDnml6eJdJyIjaGFKNkGl3mmDxpeyghCdbSjrZoxmPauqGdTIh1Q+YdJkZcW1PVE4SSlGUJJPR2EJKAJESB851krDGJrk2CMRoRInmWNJKdczRVhW1aev0+VV3R1BVRqsRru36B5VizkEfaxlHkZSrlqyn+cqpRckfLvKqzrV+ctzm5Izt5qXORYi42vDsqlzagFoe89Y9/M42TjMZbxLJEK8n6+fNElSHzHBssEAnB4+YEWpLeh+9YAkAoOZNNNZlBSkGWZZRFmdAxIWBDICqJLDKKssfCcAElkzChEZJSGwZFSU8baBpwDikkfVOymPUohEneT0lMblhYGFL0CrIiQ+WKjiAWoRRSa3RmKIoSkB3sXhCiQEhFRFA3NVmWo5VOsyXOoXRBsBWLuuYd73kn933Ne9GLwy4cuWvgL9OD+UJnYzMcqt6xzg749yTe6DsSMOzGyhSEwEiJb+Dwe97LwS99hlE9pnz4vZz/6ucoRhOWDxxC5YYYE+1G8H5GvCNkJ5nVafRORyizTBBCepYxOhWmA7StRelUqimKgt6gJNeG6ANGlTRKsnFxg3pSIclYGCyS5z2CEFRt5OJ4k9ql91hcWmS4OEyeUynOX7zI+uYmQhicb5EkXWHnQxLM6fVxIRBi4p/O+zltiDRVRYnsGLTS9XHeU/YMzWjEy5/+FMiCD3zPX0UZjW8topu5jvHN7y3saMVNF/Xfd4an07KKSwxwug3/MvCP7q5tWOBlRFjPcHmJ5SfexnOf+QKjjZyN187y1L37mWxsUfQlLliUSBoeRopERCUlUmvyoqBtmoQ4di4VoaOfk1WFqm6pXIuRhugCftODjIjcUOYFG1sVLzz/MucvbKKEIZMa61tQkoujMZuThsZHnHdpbDQ/x3C4wIH9Kxw+vB8hFJM6iWB7H8hJSUXZASqGCwsUeZHYHOoakfUwvT6TZhMEjEYjTG8wk4QYV2MW7n+E+wM8+L4PsP/hR6isvRsEqnduv66zrUuSXL1LkfAl4A+Ab+ROiVfvPPpAMkARUEGRLazSlkPOjSY89cjDqI1TnH71NR58+6ME6zAGfNeXtd6jYleOkF3ArxQiy3DWdggYMMbQNC3WJYrdzcmYelKxMBwwKEvGreOFF47z4kuvUU08Pupu/gR6ZY51ls2mpY0C6SRaZPjoaKzl4uYZTpw8yeDFgnzQJyrFxtYIIxVLhSIzXWnFOra2thguLNAbDhPjaleCWVhYRCnTze6KJFWrFevnN3jruz/I43/pL1NFqKsEwA2yk5O/893fqQ39wc7td6cBzm/DP9IZ4G0qL+8FrTN3Z8iIioIoBHWIHLr3XrT9KE8UFUcLzYnjF3ll7XUOPXov/TxPJI8CEAalHLGZzOhBpFKoEIlaEHyLkAGlDEIE6tYyrloubo45tzFiVLUsbTpsAyfPnef8+YscXTnAY48chibVFKORjEYjvA/YxTTl1jYWiSSIiMlylFGsbW1xZrTB8TfO0CKJUTAse/QyTXSCzXFDIE3AKaORWcFgoaTMC4QP5Jlhq7YMy5LgHTFYovB4oJdlTKqQbjapCDJLiKIQiG9yA3gaQu3igX8kGZ6cSgR35J27B4u/ApwBDnIXoKS7ER4kEmcD+4/cw1PveS/jpz+Ou3CK10+fZPnRd1DsP8rmqTfoGYFWuvMSmrbpSFlgVhZxbYuSmiDTIkWfJtw2Nydsji2bE8eFrQkbowkT27BaZLzvHU9ycGkV5QKxamkbS91adJbRtC2V8zTBQ3SzYe7oPSrvcfTgMvc/fIS18YhT5y/Q1C0qJv05IQR13UKMlEXVDVulwXvvHb6piVZS1Q1Li0tJgrVbwNY7iqJIXZ4YZ9i/u8L3dXQ/nS39ym7Jrb7CC0bAvwT+O7ZFRe74mQgiCkUTBO/449/KsVLwhd/5Tyy/71v47v/rD3J2veKNV3+JMuvocoND6jRRZmuLcxajkubbtF0XYyfmLCWjrTF1UyMJDHLBYn+ZQwf2cc+B/RxY7NEzOhW0WstkyyHGEVkLVGIZgqjQUVG5SCAijAat6C/0GC4sIHVG0c8otGQ8muCs6wroIHWa7GutZzSZJLJLb7G2Zbi4jIswKIuO4EjMMuRy0Cfv5TMPL+6u8cup7fzLzqbUtQxwfg/8CeDvsy3jJd5Ed33p37up7SBSOTMGaITg/g99mHvf9Q3kRYnXkoEaofuL1OEiYNEidgxcSSo1dkXSQJzBrZSKxCho2yZlw1lGMJHVfsEgz1kqcnrBE11N28VVQThCmbZXastko8FFcBFq66jo6oshgBVUm56L4xHa5BAjWikGvQKItNZjXRrDDF3h2HuX2o3O4uN2QVkLSfSePDNAumHMYAFTFp0e0qXX7laMR9zE2k47bE1nS7vGV/oqVvsK8LPAX77TyYjsOASdDAgCKgoIAVsFVNGj8R7ReHqDkoP33sv6y+foFSrV5ZRCSIXODETVyWzJFGtEh0ImqVTfYrI0EK6sZ9gv6RUaI1K3o6oCrVPEGKnahhBjgu5vTRhtTWhcZNJYxtbhu5KPhKQNHAROR9oQ0LGj+ej60WWpKWKGD+BjQGeqm3NOwAgtFcSE/FZSELvCuXWOECJFnqOMoW4CSnI3PaZ29LOdLandasv6qjteKsf8OdLI5nV5wRu/+3aTgupEAqe80p1X1EB03bCNgDxTHH7kUc68/GW8awhEvPdk2uCdQsQ07C6JnRiNxHmb1CRjRIvIykIJNtLrFZhMEYJDq0RpEV0qCuc6xVgb7QgXJSovEtOrBSNjGnzPkhiiUqndHruhdKkS+iYqgfeehXKItQ7pA4XJiSGJztgYMCGS5QYRQxrjVGlKzllPxFNZx5H9h9IcNXHWahOik+raiX558xKSqa00nQ1dMSSVV7FeCTzfWfAdZVCY9hNl3G7kR5G21pnNKgkuMjxwCLO4Hx+nypdpIRJUPXQcMhFCSDrBWs06lWWRMejlaJNmSaSUaG3QWUZRFuSdqnquulaZMhRZjhQSk2n6ZcFir09psg4/KPDR4/FJuaibHfYkVXW696cz1F5eJCo2pVFaU5ZJ8yQ4h21bmqbF2QTbqtuaKCXLKwcu1/GNe++z30bvJzvbef5q9iP3YMX/qLPkuySxunLlPcRIb6HP4bc8zqaVaJmjIkidEgXrHN6HbkpOzmIrIUB3/HzOOzKToTtWBNExmhqtkwq6TOwFVV0zmUxwTYu3Flu3SamoqpnUFVXbMppUTKqaqmrwPhJ8QuBM50+yLMO67aH2xrbkZUEkkmc53nuUUlxcXyeEQGaSRnFS5YwEBP3hgHB3rcqevd+1DPCqXnAa5F7p63qTkWu9x7XeN816pIW5961PYnsLNDHNlsiOdNxo3fWJw+y6RJInlB1IVXaAUa0TFg9Skdr7baLh0IFbnbVE7xAhIW5yLTtFJVBiWjpK1L0hhBk4QimV4FdZnryg0VRNzdrFCwwX03hnnudJ8anreCQvHZBSoIykcY6VfUkhYCo9sfN67MQe3m3e72ox4G5e8M9zE5zSb5IbxLeBpZUFVh56iPWvfIrcgCTBnrIsSwq6ztG0Dc7VKJlACUIKjNIpW44pE50ufAhxhtlzzs0whHmekWUerQTWR5wPKJmjg8Z635FQpgk/pEBlyYum1+b0+33GdY3JcoYyxYTWO3IpZ4YaY2RhYQEXE89NQvFA62Bff4AygrZKhnkXeb92L97vWh5wpxf8x3c6Ftxb0zFibeDBtz7FBE3joXWpvi6k7NAwcQZWjTF5pqnHKIoc08WFRVFQlsXsyoYQqesahCDPcwaDHsYo8lyTGY0goo2klxtyJTAygShUR0JU5Dm9Xo/hcIgxhqLXY2lpGaUUg8GA5eXlhM4xZgbPd87Stu0s821t29HCRfrDBdK9EW+y+3TLvd8/3ov324sHnH/TfwL8NZK8600PLl2JUf9al/Ca4tjSQxM5eOAelu57jK1Xn2EobCKulBEpFd61SAlSJmG/rCgTjB8IzoNJN3Lb1pRlP8Vi2uAiSK1xbYNUIklBS5MSoOCRmcA6j1aSLILOwLmAC4mHLdM6wb2MIe/16A2HSKESv7QUHVODTvVJrWhdg2sdWVZ09UtB5RxFLhIk3/uEc+wu1vy1kcgu1OiYJuJVBKuvY5uOV7cTAZzubGVPzkpeh1u9APzXd7sXFEIRhCAoycNPvoONNmKyQdpGZYqdEnNCYhuYDqsXRYFUkqIs6fV6mCyjKAqUVmTd91pLev0eC8MheUfJW5YlSuuEAhbgQteT1Zo8y1N/M4Q0r9wxGkQiw+EgbcOLCxy65yi9fp8iL+jnJblKHZembthYX6eqKrz3SKkoer2OElgnKYoO0X2X1P1kZyMX9pq07tWLTQvR/1/go53n9HejAUafMOxVGzn0wMMMD97LpHZEqbA+EqRCZSVCZ2mKTkylE7qBISWRRmPyjKwsMHlG0e9hckNeZEiZxjuVFuTd5JpWiU7DeY8NSepBakMgqTdp2eHyuuRlaXEJISRZnpMVBcPFJQ4eOYrRBucSPGzj4jrVpMJoTfSBuq6R2iReQ9vSKzuvfXdkwL6ziY92NqL2ah/Xs41Ohyp+gEStddvLMtfKqsUuU2Z0ua3wgSLXLB+5l4ujMTovCVKDMnghsJC2xo42pXUWH1LrzmQZOjMI1XGydFhBpRRSkgiQiEgpZmwGzrtEAicgKokNkXFVJ5aFNCuVjFUnQqQ8z6iqiq3NEVIkb6myjNpaNje3kiKTtQmO39Q0VYOPEd81fIN32Ka6Itj0erLgm6xozNOt/UBnI3u2C3mdLlYBLwP/oHvtXecF0/xDwAQPDg7ecw9tgLptMUWB0BoX4rYwTdMkDGBTdzD2dDnTnEbGeDJOVLpKoHUnLi1SdiylQEmFc47W2g4QEHExMqnr9LyOQqO1lrquGY/HTKo0wxJDgCBoqpqzZ89TNQ2jpmZcV4zHY0ZbW+CTjESWZ91x6KRVFyNtU+Odu9M7sO9s4R90tqGuJ0TTN/BhCvj/AN8FfPON9omvm7EzXh4wX3J3zroiIbWkhMBFWFjaR9ZbgJiQ0llW4nzAtY7GC4JPPNCVs2RaEq1DtI48yxAShPAQW0TMaOsabxtQCTTp22S41jmqpqUKgdYF2nZCLy8QSiVQamgRVlKojEk1puiVVJMJpsgxhWTS1oyaCVtbm1xYW0vHMZtfEfSGiwzynChIjKkh0B8MEN7TVBXFYGFGcrntufZeQ71WYrLba7u/d1tv/GhnEzu2XnHNNOZGxAqnLvcHgM8CizdaG9zrJdmLCOK8rEpCzwhsjORln4XlVfzmSerYUuR5kjLVhrwsaYDRpGJrc4siyynLEqM1rq5x3jAYLmC9Q6rENZgQLI5qMsY1HYh1XNH4QOM8dTcI5UmkRzZ4vEw0HEZIWueZ1DW6yAlSEHWF7ZTjg+iGqXwaSlcxTbPl/SHC5Imx33tiCOTGdLPDLaXY3nLvQM3vIsQfuDwk25t05Y0Y4PxW/P3Az5Mcgr4btmARu8KvIMmeZjnlcJFmdBLnLMEoZKahlbRNQpRMqhrrPMHXTKqavOzhrWVxOKBuLEYpbAShBL51OB+YjGpGmxUYw6RusUga62mtAy3xVYMIaZufJjltqBB5jnYebS1BadbPnUNlmq2tLeqm6tSfPD4qIoGVxRWysk9WFISQOKmLvEhMWCJNxt2htsA08fj+ua33ukMyfYOolemH/wLww8AP3gkj3P2On27FEYLHGIPMS7TUaKNTNiljguYrTRsblDaUPQkhMBqP8U2NiFC1bYrtnENXBiMF9WQCKC5c2MS7iHcBi2BiLRe3qlT01klLRKukade4Fm3ypIs8qmlDyr63RmMGg0VijJS9Hs7blCl3BJVGK/qDIf3eACEVVTWiP1ikyDPKPKOJMNrcYuXQoVvu/a5hFy7GqLu1/wUhou7W/7r2vZ1TcTdihAr4u6Qxzq/jLhliilNRMx9RSjBcWmHzNUHoqC6moICpxFbTNLRtm/q2nTjNZDTCZQmV0rYNdfAQIk1VU7eOqHImkwl1M2ZjNKK1ES80aEntLdI7JN1csuikGRpPjC25KQg+bdGNbnD1BNXVIl3bJtVNCfv3rdLvl3hvcXVgUk/Iiz4xenzbYvKMra3NbSR0fFM93ye7tb8hz3czW/C8KU+/vhP4yq3qkuwlXhRX77EAAplIOegtLrEeBUVmiN3guswMoyq11UyWI4WirmuUNighKcs0wilDIM8N48ahdUaIgq1xhW0D43GFEx4vOsktkcAQPkRcJ4IoRKorZh3tcCrXBCbVhLIsaZ1LNGreE3wk75SZondJotanv1d1zeJwEUmaczYmESH5usa1LineXOXqTBOUW1BsViRpj++c637EvazMbn/XN3lQU2M7C/xp4HeB4lYZ4TavCZcx/ser3D1yWhtLujHkC8tYlTGQnkIrmnqcgvYIdd1gTIazDq3NFG1IluX4DkTgfSDYgPUtSgr6uaHB4ZzGu8RQGolducURRexg/ylujIAnEarnRUZtG3y06CLHtQmJnWtFPR6TLyxQ5jn9Qa/jDKzJyxKJJ7SWsjcgz1LXRsqAG28iW0vol6kdGDq09zX6nDew7tPSyqRb67PTrtj85N21Q4H57PrWeKrppPtngL/RHdQdp2KCBIsPAfrDISrvpSTEe4zOMVKRG0NZpljLueQZ8zzHOk9TN1RNTd20uBCZNDWboxFboxGtdak3bF2S9BIQnYOQ+sBCxE45cxtTGENCXccYZoADpSRCRpyz2KZFad0ZaY7WplOMkkmetd9Lq+0dbTMhBp+SnLZha+NiguPfPsTzDBPcrfFnujW/6ZbsrUoapgnIT5CGmP5V9zvFbczRdqPxuOy6RZJyksmJVUQK8CGRkesOaNrUNUWWETqe6KlEl5CC4DxVa3EhpmwWEmFR05AVBdZZvBf0+iVNk/rMMUSESqrqPkx15BIQQuvtS942bTJYEldNlpvZeTnnUFmWaDuco24s/bKHUZJMKTItsNZCFFxcO8fyPUfSYNJUkCbuNWm75rWNOzLen+i+dzfrWYUQtzRWc6TZkR/psqPryIxumw8kxJgkr8qFBIsnZcDBeZy1ndxVIDdZAqzGJNlV1zXaZHgkrYOATCRBIrFaIRKbvQseVKJ3Q6VestapdZfQzwEhSez8nUbJ9DGejBNNnHeE4JBCUBZ5N0eSXr+1tUXbtqn+5x3RW1ybVOGliBgZ8W29rVYvpkZ47cXfY6tu6lx+uFtbcyvX9VYnC9OD/du342BvLEAIKA2D5eXULQDGkwpi0uSIBEyuO2EbTVHkaJmkDqqqxnqHCwGkxPqEdKnbhtparPfo3CTSSO8J3X8R8N4mIkxCN3KSaHgjdMiaJEOW+sOKXq9HWRQJ1e2S7t1kMsEYgzFZ4iqUEtc2eGfx1iYewei6llycS8Bui1P527fDqehdBYxvLlaY9ga/v/vd95FI0M3e3iB0HIfi0rw2Xp5DXQuGOZVkAMgXFrkYDX1qCgkupuk0I6GyDik0KIU2GXnmkFLRtDWF0Vg8jdAEfDfbm9DLY+9xXhKExkULSqbtNwq0TMqWMUSUViitCSRQ6VTosMwMWsaOWjixXiXYvsE6gZImqSn5QIgNushQArQAb2uC1ggDtmlwtkFoTQgy4R6FSKiAIAgiJF6JeIWrtpuygRDTNfuRGOP3s937j3vtVO1lm78dk6TTgFV1Rjj1hHeGpLgrEmRlL1GbArnWZB1drpKaXtGbeQ9tDMPhkP6gR69XIgn0ckO0FhnSWWhtUCbD5BmtcwlFoyQITUTgnMdajw+gdZbQKx2xep5nSASZ0ZRFTq8sGQwHGJM8Yr8/QHdtNiJU4zEiBkxHtB59uozOeUQMFEqCbSA6eqUmMx0TavQz0ccEZW32tDXPOZGp5/t+tnnDb/n63a5R5jhXivn+Ln6YoiTedDBrJBlgJ86VjEFJJArvPEoayqJMWa1K3spkWZLF6ga/e3nGynBAkWsQnhAdRZlhTGLmT0rqaWxUJGkYdGfw065IJiWqU9gc9voURYFROpGpS0mWGZqmwXuHEGl2OTcKvKPIDMEnMvXoPQRP2zZEL+nlJZ/8zG/wkT/817y29jmyjGTELkHHCAoZ9V4q1WGu1vfD3dpNAci3xXno27zudCfzt4Fnu+yYq9UJpzvv9TbXp9vHLBLqAuwYEw90UQ4IURKFwHWxoJSkLDT6VAbpZL+cs0l4cN8+grVIIejblrqpKZxmIZRM6pqtrQmDQtPLNLX1RBRVjFSxk8SSKuEJhSTTaW5ES4EksRhknbELIRgOhmRSIUKidBsM+2yur5NpTaEz7KTC5Abn2k41qVNXjxPKXLB16iK/9qV/xYGjPb7xvX+Bx+//do4cvI8YFZOxZUqY2vEa7Zatzq/JdOdSO43vKsiYG3qov/Nf/3fXTKFvss8YO3f+WeB14Ju6YrXf1QjF5aWV+dB6L8cyb4ApM5RIARdeegZjxyiVAJ3BNUiVOgshphqe7qg8WmdROnkl3xWXZccnU2Q5mTYMyoLFXkmuNVoIjFCIGNFZ2k4zrTA6jYMmI1Rp281TLDfsJ5CB0IpeWaC6myONfCZe6F6eU5jE0JDlefKsxqTZ4bxE5IJMZ6wuP8xLJ05z8uJX0b2LfOrTn+X3PnqMXjlk/4FlFoYZQimsTeTsO67ltIW61dX5fjTGuOcE8pYZ4F4+4AY7J9Ni9R8JIT4K/ClgoTtBeXlEm0xOXM1FXiX4FfNP7aBKSkrOvPgccrKeYqJgU89VpcWWQqQp4RjJ8mL2BtNBdAT0e30ynaGExLcWGWIyPimJIRC8x3tHnk29nUxCgaT6Y6YVudFpaMmYNISkdBoaCilAqJoGKdJF0VIiSPS8mcnI82I2JyyVIssMWpcYnSHIePzxr+Pl116l8W/QK0v+zb/8JB/72LP80i//Mm+88RpLy6scObyfXk9hbaL4jSI6KZWOcEpEvgPir3YdMrdXA7spA/zbf/8f3nDx9waN8HXgp4H3Aw+wzUnYmZ64pJ/LjIpjW3Z+Gg2LeFX7TAYRPMZolvuak8ePY9dOoEUk+ooQIXgBvlMq6rZmb32iQOs+sLUeoxTe2mRUUpAbnT4/ibARQsT6NiFtEGQdi0I62IiRkl6eUeaGoswo+2XqQXsosizR8vqAMRmhbdCA0Ya6qlDakOd5xzWTCtxCJe+spECVg6QW6gWbzZhXT/4RB/cd5pkvTyiL+1hbu8BHfuWX+MhHfp3Pf/6LKCk5cvhQ3LfaDw6hG2v/UMr4LTHG5wlCE4W71sjiJeJCcZc1E7fQA97KqlynlrMJ/GTnBb+ebeJCecW7SVx+t4krPC8VgKEoMwZ9zebmmF/8lY8wPv0qK7olWkuwSTlTIxBd7a2pa3LTyXd5R5alwD1TaSuVQlDkBUql5EXrBI3XJqksSaWSZ+sSmOCnshBpcGlQlvT6ZRps6rJw7z15UYCInX6JT227ThtlPBpR5DllWWBtizHpvfO8SFrHJkfqjNxoTrxxit/4/d/BqQ2W9y3z+c9cxNk+K6urZFmPCxfO8vKLz/Frv/IR/7Hf/7hcW9uUhw8f/OHDR1a/V0S9aVunAJ/Ec/a+K+66V4nb5AFvUXIyrSn9Jkk58ZuAfrclX15NFbtPHoo5mH7sVMSFlPQHhixTvHLsNX70x36a//5/+J/51z/643zNI/fw1oNDbDVGhkhwPtXGQkArnQrBAoIPMyJI1YnYNG2Tamtdu65tGrRWCZVsbSouK43kUpGWpk7DRJnW9Hsl/X5i3UqwryQ4mOWGGByZTpjEMsuwtmE8GtHrlWlQfkrRphR5nmO0SaLcyqB0jhKeM2fO8pM/9/OYgWf5wApf+qNNMr1KCJFef4m62ooC58si0+fOnFv7+Mc//Vd/8zc/+kMnXj8djhw+LI8eORCU1jSumhmVlHJvK3qlYtw1vu4UinkK41HAzwFfBP4Z8G07guK9xAQ47zsib8N44vjob/0+/+Hf/zJ/8LFPcObMWcqyz/7VBwhOo1UGYVobi3hnZwypSmuQClxka7KFUopev491jswYqqqizHKUlPR6PULwCCno91Id0TuPlqkVl/k0pqmUJBOSPDMYLfHeoYUE0TH1G5Eo4KQi+ARuaJsKIWJX5lHdnZbiSGJIqqCE1LKLqUXnJjWT9XMc2b+PQSHZvNjgG4vMEyO/kNKv7j+qTp3Y1FVT/Wam9N/q5fkLF86t6Z/8Nz/lf/ejHw/f8ae+ne/67j/FI4/eRz2xtI27yRjv2q+7kzD6ONe6ewH4MPA3gf+RNGdydTBDTEG01pqFYcZ4VPNLv/Rb/Jsf/zd86pOfpm09ZTFgZXGFwXCVjZHjzLl1lD4685hCQpSCYD1N26Cc7mRQFT2f07Qt3rYdeLWgLMqkqtQlF0opQvAYnTEZT7BtS9ukUczWWrxzGK3JlcaYLNGudaOckoi1Lc61GC0ROsmK+RA6aJhO8W4ISKG6+C/Rf1jbInSKSYUUeJfCimMvvUCuE6FntelxlSX2muii8wh0r+xvDBf3/8P1C6//cxc8rq20IDohBadPn+Tf/fQv8Ad/8En+5J/+MH/2u/8k+/cvsb4xQUl1A0Yo9mqA8sbEpcX1Oryr9hunfv6fixB/c+oNO/fvIKhAENAxTbmIEIrBUsFoq+FnfuZX+Ykf/zd85YtfJriWIs/Iez2ULlFmEegzGb/CxaZHGx6naR2yi/9Suy4k0eSqwjaC3GQoJej3CnxMXNM4CwFsZ5BCpMy1LAu8T4aQ6DUMWVQ01uMjmNyQmYIQEy8gQSXiS1IGXmaaXEtiSN4vdIKKLvgZNXEUIKPCCJL2iAAZPMI7glUEN2Lt/AWef+llkBKje2xttDF45YNrNMFqQfxNL/Tf6uULL4x1T3q3hUa6qZFbXxF84NhLE37qxzf47Ke+yHf9F9/Oh7/jm1JxvIloqYkiXGZYUVxtD97lt52QfRR3WDxslwr8vDf86yRVRU1UQkTtCTLaNpAXGUWp+I2P/BZ/+Xv/Ev/VD/4dvvzFL2K0oiyKJH+Fxpg8EX/XFc5tEFVN42qsbROvShc3hhA6YsjkaWKMXcsLlEw6bwI6eYQw43k2c3KqztqEdg4+DbnHhLpJeIjUKbHOMZlMum5H4v7LTNZ9ZqBta4JPYtkxBJxt0Z3ecZoySKUe2zSJFSEEomtxreX5F57h1Nk1Tp6+EPcdWPTnzl4UAqGda096Z/+6d/bDrqlfIEad6SxECLGDjsVE/kUIDXW9xdr5N3jlpVf53//5z/Lf/oN/QlO1DIc51rc3Lfswffn037uLVXjbGwrgx4B3Av8TMbTBBSUxYnmp8K+fOBn/1v/t7/Ffft/f4Auf+Syl0WRSEr1LHCoqw2QFAkV0Du8qBA0tFaNqk15ZUhZlap9JiRRJyJoYE4cLdBJanthp7saY7pE8M+SZ7siNRLd4ifpNKYW1ltFoxKTjc0nKkWJGFKSUSmxXgLM2aQR36JfUM074P9VhB0Po6ImJiBiQnbfxzmHbBikCmxe3eOXY8dj66DcnW0Llrdpcb1sh5P/UtvU7nXc/5lwrWlfJEJzTxswQOkk3uWMJCxZES4gVJ068gACe+fKr/J//6g/ylWeeY2W1ROiE7nbR4aLDx5vjJpB3kkn9Kt4wAtp7f9Y59w+RvLu/kP2486791z/yC+p7//z3if/473/V50rHTCpca/GuQxwjETJHiowYJSF6om/BO1ywTJoJeDeDPKVMV6I7xoFp1hdCoPM7NHWDiGleo21qXNti65q2rmnb5E3DrHUoKHu9xBEtJdoYdJbEZ2ynzKQ6scHYqR657saZZp4heIgeoxVapUK2kmnfCh0ZpmtbnLW0TRVfP/G6f+PMBbFla/XAk/vb5UPlj1dj3g38wxDbszE4bV0brauCdW1CGyFnwo0zLVWR0DjeO4Sq+epXP4vWAULGX/yL/xd+5Ed/hslkC6OhVxYMhwVZnqf5L+9vaABecxc+upKKK4pSDPrIU+e2nv7sF579a//up37hh37r1//T35G039svZGabCp9oTCUCEUnZbFKXlAn8IQJEh4qSSd2yNR6xovrJMNOzUCLBq4zW+Bi6+CR2HH1pixWFQApJWeRpgk5pmralaZpuBlngnEteUaTpusZafFOjpOuSF8GkqtKk3jChXqaackSIPsw6KsKk2JQO3BC8p3WeLIMmRLQ2sY2E1tXqpVdeVOOGdqut/u0jD2Y/lC+KpydjBwgVggugnCLiXI1IlR6ElESfBuGjkMgpiloIolAIb5DK8vSzn+Gd7/oQDz74JH//7/13/Nuf+jkefuQR3vKWR3nwwft56qnHeej+IwxyQ9MkQ3QuZc9SyGvmIbfBAOOenyeIiX2+S/VDAB88vV5GUUhee+10/Gf/71/0n/3ss3Lt3IY48fpLT2e6/Wu+Hf+Qs+3f8c7/BSBP+h/ShygwMpNSaDEVIRT4jsRRM6pa1jZGPLjcx4aOwiMGohAoo4kCvAuJn0+obdpf53CTkLyaSHwwYjrx5D1N21I3FucDdd1yflTR+KTaKbXG6JTUmA4tXeR5ij+dw5J03Yw2My+eOAyT2qfSHR4gRmLw0ds2JHBsrZBarW1uNW+cOfPT48b/ULmaPf2Wp5bY2BirahxikUWf1OHpbqyUygkEUmgsFhHniNvZ5hL0XW9AyoavfPGzfN0HvpEP/LE/yR9+/KM8/9yz9POSor/IoaNHePTh+/jQh76Ot7/jKfbv38/S0kISfmxSjTT10CUxcMln3QYDvF7ImJiV/ZxzFHmfvDQcP3acn/7Z/8DP/+yv4GzB4f1HwsUzJxFuJL0bCYJ/Ovr414D/FRH/PMS/DuqeiEJiEAgXU49NzkrYHmwdOHtxnXa43PV9ux6sSIAF0el7TJE4iSU/dTms9wTnCd53205ERTBKYgXEEKmqmkndYIOjtR4hdEcPnBjzVTcDEX3AC4cFsswkDxc68QmR5lAQoRtuInoXAlJEKaR2rlGegJfyhAviR4+dOPkztRVfvdBs8vAHDquVwyZ+6ZMXvbcgcksMsothE8zPW7qCuZyqeCeWfTHPM+1xcYIJGhUdIWzwxS9+hne9/5v54Dd8mGc+/3uoaKlHF3n1lS1eePZpnv/qV3js8YdRSvHoo2/hne9+Fw898lb271/GWWitS3Gwjx2dsLjTW7DEhwQbzHLFsCw58dppfv7nf4Wf+/e/zhsnN3j4gbcyyHJePfYVqvocYEMMgRiC7CohXwX+e+CHgO9USv5FIcU37jgvFwlCCiknW7U4c2GTyUFLaWIXeIek5CAALdMw0o6+t+ju4JQcdCrTMc15VE3dkU+mBEMpSUZi0BIiydFI0RWROyb/hPdLKJkYO2nX2HU7vCfGEI3WAWRsWqu1kipoRYzehRB+10X/UzbwS+fXNzY31jfYnFhlDpj40LuWvcgt5077LrEQnWF3ULUQdnUWuylWydCVgGRECMd44wzPfPHTvO2d38Bjb/8mXnz+c6iwQXQNeEtRaIyWjCcjPvfZT/PZz36a1dV9PP7Y4zz51Nt46sknWRwOcJ40vOV8Uie41fDj3eqVM6xe51lCiAgRGQwSg+jrr53kV3/1d/j1X/s9Xjtxht5wH+9+77sZb5znlZe/hGvOIWJFCKl7EGMMXR4vUz9cbAb4SSXkTwp4AvgOIcR3Ae+LMeooEjavrp0/O9qI6+OxyBcyKaMQhFSKQAkIzAaCYldwnrb46BA1sZNUmJZOsjwjYskyg/WBUhZJMtYGfEwzxVMDnBKJz5jvu6w3hBCjJIhU5BAgVUSoxrZIITyCT9vG/6KPfMR7/2zrLJuThvPrm2rShHi+Gvl73r+P8qDFhcBoXXZedbbnzc4h9TUdIfo5IxSzxGsbYNDF4oCUDhEDGxdOcOylZzl6/1s5dP/jnD/5VUScUMW1JHOhBc629Ho9hIiMttb52Md+j4997Pc5eOAgjz76Vt77vq/jwQcfZmmxxLo3yQNOsyNjDDFGej1N3bZ85o++yEd+9Xf5/d/7FBfOb2J0j/7CEVZW9rF+/g3OnPwqIZwnxgnRJz692Cmcd+OHYW4vnyJ3/3+1nU1vHEUQhp+qnpnd9a4d8uEASYRACBAkHIiAA0ickfhr/BIOSBxCiECEgBI+BIELJESKIhInENuxveu1Z2enu4pDzxpHnEBwmONcZrtru6rf93l/6Z73gZeB94B3CeHN5L68E2vWNjc5c+JZYjMzN8xjkiCKq6l4EA7RpnSRD3cIf6adcFUkG5vMnSIlVKEqczJ6WxhtzDAhUUf+2qAOYp47R7fkmufKFhaLPLnvJrfvilB8EkkXPLY38h+oE9soe3Wj42lt+01KG+M99EjBM68cparmDHSZvfFDREJXBf1AoJ43U+oqXR4reWdd/Rvks7N3pu7IFgSk3Wd74w79pSEnV09hsxm7j+6hYafbWLnDL6tOOBsCw9EQEB5tP+LKV1e4+vU1Vk+scv78a5w9d+7/X4Bmnp1mBayvb1OWgW+/+Ynvf/iBDz74iMkElgZH6A0GmSK/ssxk/JDtzTtYs0VK+3ngmvyxQJbHeXCy8DEsZpsLscMN4IYL70soz7RtfHPpidE7N3+7+/YbL50+G4IMPIkmybItSblSSVAHN1VBREXEcQvgLqKImWUIXJAD2n5VlfRjj3nbuom6JScBVRnc3PLcI98BiFkKMXaWTRxxalX9WUWu4v4lIt+lZGtmbRemY+JOaJJZ0zQ2rWepnmev8OZuzZFXj7F8oqAQJ9WBna1dQhgcKgDGohkRcfyx2Z13wVH2mPAgy9/84JyYv4gz39thsvWAECqOnlilTRNk/AcdTDGTZTWgoSSmOe5OVVVUvT6xzVaDnZ1HXLx4gUuXLuYF+G+k73KIuv7X+x0ards1IrC0VPL7/Xt8cflLbt68RVko48k285nT7iWOrhwn0qOsBpT9HvXuOtPxBqnZJbUNYtm3655Q/CAsBs/Qn+zqC4jkB8GcZLKgqIhqQEy1WKtnce3pU8sf3r29zr31P848t3r8ZQ/F62J63lTOmNrzeFr1KAKEA0W2CEUhWV7ldIRUy3O07scJIgz7FSqIti4UXeUXIVpWsjgJN98wl9sqxZqldB3z71X1hrutuSpSZPWzSNIQSk2WzMzMXOK0bthr9pnHxKyJjPfn7Ds8/8IK1ktUVcXmemJnskdVjPKI5aDj1EO5J/l7ZnOAgdpiJpGbpoN97DlHTwLJFcSIbc1sssl8uEwxWKY3OklvtIWGHqqKxczEsZhhTpaM1ueMhisMhgMSLWVVsWRZg/mfd8HSxYsWKjTzmo8/u8rlzz8jtc5wNKJJc06feoYrl6/RzFqqfrYtCkpdz0j1Nu18isUZbrFDWmTIcj47/uNLaHOHolKd7kQ1E3pPkn789d7aU0eOrvUkfirkLDmUY6Av4n4MeMvMCuA8cMzMzdxPm9kpVXVRlexWKzGDGDtjrtkDkPtlKNSQrTal6yJEXK6BbwG33H1rkcK0uEYNIQgQuqG2iWDJo6WU41zbZOw3c+Yx0TYtTZOYTGp6o5KTp1cQGaOhYONhQ2wqyq7Jcv+XBeZv73SKcTPqeo96f8Kg7KMog/6Qfgf2XJwls5RLMMvn4Ol0Sr/fpzfoMRoNiR2y+E8Jw5CpW9fGCgAAAABJRU5ErkJggg==""".split())

ANLATICI_STILLERI = ["Nukleer", "Stanley", "Homer", "Wake", "Rucks"]
STIL_AD = {
    "Nukleer": ("Nükleer Adam · Efe Soydan Pehlivan tarzı",
                "Nuclear Man · Efe Soydan Pehlivan style"),
    "Stanley": ("Kuru Anlatıcı · Stanley Parable tarzı", "Dry Narrator · Stanley Parable style"),
    "Homer": ("Epik Ozan · Hades tarzı", "Epic Bard · Hades style"),
    "Wake": ("Gece Yazarı · Alan Wake tarzı", "Night Writer · Alan Wake style"),
    "Rucks": ("Eski Hikâyeci · Bastion tarzı", "Old Storyteller · Bastion style"),
}

CEVIRI.update({
    "Anlatıcı": ("Narrator", "Erzähler", "Narrateur", "Narrador"),
    "Anlatıcıyı göster": ("Show narrator", "Erzähler anzeigen",
                          "Afficher le narrateur", "Mostrar narrador"),
})

DUGME = {
    "tr": {"tur": "Turu başlat", "sus": "Sus", "devam": "Devam  ›",
           "bitir": "Turu bitir", "son": "Bitir"},
    "en": {"tur": "Start tour", "sus": "Hush", "devam": "Next  ›",
           "bitir": "End tour", "son": "Finish"},
}

TUR_SIRASI = ["AtomikKutleSayfasi", "YogunlukSayfasi", "MolarKutleSayfasi",
              "BaglanmaSayfasi", "NukleonBasinaSayfasi", "IzotopSayfasi",
              "AyarSayfasi"]
SAYFA_OLAYI = {"AtomikKutleSayfasi": "p_atomik", "YogunlukSayfasi": "p_yogun",
               "MolarKutleSayfasi": "p_molar", "BaglanmaSayfasi": "p_baglanma",
               "NukleonBasinaSayfasi": "p_nukleon", "IzotopSayfasi": "p_izotop",
               "AyarSayfasi": "p_ayar"}

# Yer tutucular: {v} değer, {f} formül, {s} izotop (ör. Fe-56)
REPLIK = {
    # ------------------------------------------------------------ NÜKLEER ADAM
    # Sade, öğretici ve resmi tonda: derse/sunuma uygun anlatıcı.
    "Nukleer": {
        "tr": {
            "hos": ("Merhaba! Bu aracı ben hazırladım ve turda sana rehberlik edeceğim. Nucleus, "
                    "nükleer mühendislikte sık yaptığımız temel hesapları tek yerde toplar: "
                    "ortalama atomik kütle, atom yoğunluğu, molar kütle, bağlanma enerjisi ve "
                    "izotop haritası. İstersen turla hepsini birlikte gezelim."),
            "p_atomik": ("Ortalama atomik kütle, izotop kütle numaralarının bulunurluklarla "
                         "ağırlıklandırılmış ortalamasıdır. Burada izotop kütlesi kütle numarasına eşit "
                         "alınıyor; yüzdeler 100 etmezse program toplama göre normalize ediyor. Denemek "
                         "için 'Örnek yükle (Klor)' düğmesine basabilirsin."),
            "p_yogun": ("Burada N = ρ·N_A / M formülüyle birim hacimdeki atom sayısını buluyoruz. "
                        "Reaktör fiziğinde bu sayı tesir kesitiyle çarpılıp makroskobik tesir kesiti "
                        "elde edildiği için çok temeldir. Varsayılan değerler uranyum metaline (ρ ≈ "
                        "19,05 g/cm³) ait."),
            "p_molar": ("Molar kütle sekmesi kimyasal formülü ayrıştırıp her elementin katkısını "
                        "gösterir; Ca(OH)₂ gibi parantezli formüller de çalışır. UO₂ gibi yakıt "
                        "bileşiklerinde numune kütlesinden mol ve molekül sayısına da geçebilirsin."),
            "p_baglanma": ("Bağlanma enerjisi, kütle kusuru Δm = Z·m(H-1) + N·mₙ − M üzerinden B = Δm·c² "
                           "ile hesaplanır. Nötr atom kütlesi kullanınca elektron kütleleri sadeleştiği "
                           "için hidrojen atomu kütlesini kullandım. Deneysel kütlesi tabloda olmayan "
                           "çekirdeklerde Weizsäcker formülü devreye girer."),
            "p_nukleon": ("BE/A, toplam bağlanma enerjisinin nükleon sayısına bölümüdür. Eğri demir-nikel"
                          " civarında (Fe-56, Ni-62) tepe yapar; hafif çekirdeklerde füzyon, ağır "
                          "çekirdeklerde fisyon enerji açığa çıkarır. Grafikte kendi çekirdeğini turuncu "
                          "nokta olarak görürsün."),
            "p_izotop": ("İzotop tablosu 118 elementi N–Z nüklit haritası olarak gösterir. Bir kutuya "
                         "tıklayınca yarı ömür, bozunma türü ve bağlanma enerjisi gibi veriler sağda "
                         "açılır; 'Bağlanma Enerjisi sekmesinde aç' ile hesaba taşıyabilirsin. Soluk "
                         "kutular modelden gelen tahminlerdir."),
            "p_ayar": ("Ayarlardan tema, vurgu rengi, dil ve ondalık basamak sayısını seçebilirsin. "
                       "Anlatıcı tarzını da buradan değiştirebilir ya da anlatıcıyı kapatabilirsin."),
            "ok_atomik": ("Ortalama atomik kütle {v} u. Bu, izotop kütle numaralarının bulunurluğa göre "
                          "ağırlıklı ortalamasıdır."),
            "ok_yogun": ("Birim hacimde {v} atom/cm³. Makroskobik tesir kesiti için bu değeri "
                         "mikroskobik tesir kesitiyle çarpabilirsin."),
            "ok_molar": ("{f} için molar kütle {v} g/mol. Tablodan her elementin yüzde katkısını "
                         "görebilirsin."),
            "ok_be": ("{s} için toplam bağlanma enerjisi {v} MeV. Bu, çekirdeği serbest nükleonlarına"
                      " ayırmak için gereken enerjidir."),
            "ok_ba": ("{s}: nükleon başına {v} MeV. Karşılaştırma için Fe-56 yaklaşık 8,8 MeV "
                      "civarındadır."),
            "hata": [("Girdide bir sorun var; değeri kontrol edip tekrar dene. Birimlerin (u, g/cm³, "
                  "g/mol) doğru olduğundan emin ol."),
                 ("Bu değer işlenemedi. Ondalık için virgül ya da nokta kullanabilirsin; harf ve "
                  "fazladan karakter olmamalı.")],
            "bosta": ("Hazır olduğunda kaldığımız yerden devam edebiliriz. İstersen turu yeniden "
                      "başlatabilirim."),
            "durt": ["Buradayım. İstersen bir sekme seçip hesaba başlayalım.",
                 "Haritadan bir izotop seçmeyi dene; Fe-56 ilginç bir başlangıç.",
                 ("Turu tekrar dinlemek istersen Ayarlar'dan anlatıcı tarzını yeniden seçmen "
                  "yeterli.")],
            "secim": ("{s} seçildi. Sağ panelde atom kütlesi, bağlanma enerjisi ve varsa yarı ömür "
                      "gibi veriler var."),
            "tepe": ("{s}: bağlanma enerjisi eğrisinin tepe bölgesi. Füzyonla ya da fisyonla bu "
                     "bölgeye yaklaşan çekirdekler enerji açığa çıkarır."),
            "bitis": ("Tur tamam. Artık tüm sekmeleri biliyorsun. Sonuçlar eğitim amaçlıdır; tasarım "
                      "kararları için resmi veri kütüphanelerine (AME, ENDF) bakmayı unutma."),
        },
        "en": {
            "hos": ("Hello! I built this tool myself, and I'll be your guide on the tour. Nucleus "
                    "brings together the basic calculations we often do in nuclear engineering: "
                    "average atomic mass, atom density, molar mass, binding energy and an isotope "
                    "chart. If you like, let's walk through everything with the tour."),
            "p_atomik": ("Average atomic mass is the abundance-weighted mean of the isotope mass "
                         "numbers. Here the isotope mass is taken equal to the mass number; if the "
                         "percentages don't sum to 100, the program normalizes by their sum. Press 'Load"
                         " example (Chlorine)' to try it."),
            "p_yogun": ("Here we find the number of atoms per unit volume with N = ρ·N_A / M. In "
                        "reactor physics this number is multiplied by the microscopic cross section to "
                        "get the macroscopic cross section, so it is very fundamental. The default "
                        "values belong to uranium metal (ρ ≈ 19.05 g/cm³)."),
            "p_molar": ("The molar mass tab parses a chemical formula and shows each element's "
                        "contribution; formulas with parentheses such as Ca(OH)₂ work too. For fuel "
                        "compounds like UO₂ you can also go from a sample mass to moles and number of "
                        "molecules."),
            "p_baglanma": ("Binding energy is computed from the mass defect Δm = Z·m(H-1) + N·mₙ − M as B "
                           "= Δm·c². With neutral atomic masses the electron masses cancel, which is why I"
                           " use the hydrogen atom mass. For nuclei without an experimental mass in the "
                           "table, the Weizsäcker formula steps in."),
            "p_nukleon": ("BE/A is the total binding energy divided by the number of nucleons. The curve "
                          "peaks around iron and nickel (Fe-56, Ni-62); fusion of light nuclei and "
                          "fission of heavy ones both release energy. On the chart you'll see your own "
                          "nucleus as an orange dot."),
            "p_izotop": ("The isotope table shows 118 elements as an N–Z chart of nuclides. Click a box "
                         "and data such as half-life, decay mode and binding energy opens on the right; "
                         "'Open in Binding Energy tab' carries it into a calculation. Pale boxes are "
                         "model estimates."),
            "p_ayar": ("In Settings you can choose the theme, accent color, language and number of "
                       "decimals. You can also change the narrator style here, or switch the narrator "
                       "off."),
            "ok_atomik": ("Average atomic mass: {v} u. This is the abundance-weighted mean of the isotope"
                          " mass numbers."),
            "ok_yogun": ("{v} atoms/cm³. For the macroscopic cross section you can multiply this value "
                         "by the microscopic cross section."),
            "ok_molar": ("The molar mass of {f} is {v} g/mol. The table shows each element's percentage "
                         "contribution."),
            "ok_be": ("The total binding energy of {s} is {v} MeV. That is the energy needed to "
                      "separate the nucleus into free nucleons."),
            "ok_ba": "{s}: {v} MeV per nucleon. For comparison, Fe-56 is around 8.8 MeV.",
            "hata": [("There's a problem with the input; check the value and try again. Make sure the"
                  " units (u, g/cm³, g/mol) are right."),
                 ("This value couldn't be processed. You can use a comma or a dot for decimals; "
                  "no letters or extra characters.")],
            "bosta": ("We can pick up where we left off whenever you're ready. I can start the tour "
                      "if you like."),
            "durt": ["I'm here. If you like, pick a tab and let's start calculating.",
                 "Try selecting an isotope on the map; Fe-56 is an interesting place to start.",
                 "To hear the tour again, just reselect the narrator style in Settings."],
            "secim": ("{s} selected. The right panel shows its atomic mass, binding energy and, where"
                      " known, half-life."),
            "tepe": ("{s}: the peak region of the binding energy curve. Nuclei approaching this "
                     "region by fusion or fission release energy."),
            "bitis": ("Tour complete. You now know every tab. Results are educational; for design "
                      "decisions, consult the official data libraries (AME, ENDF)."),
        },
    },
    # ------------------------------------------------------------------ STANLEY
    "Stanley": {
        "tr": {
            "hos": "Ve böylece kullanıcı uygulamayı açtı. Kimse ona sormadı, kimse onu uyarmadı. "
                   "Ben de bu pencerenin anlatıcısı olarak kendimi tanıtmak zorundayım. Dilersen "
                   "sana her şeyi gösteririm. İstemezsen de gösteririm; sadece kararı kendin "
                   "verdiğini sanırsın.",
            "p_atomik": "Atomik Kütle. İzotoplar, yüzdeler, bir ağırlıklı ortalama. Kullanıcı bunun "
                        "sadece bir toplama olduğunu sanacak. Bulunurluklar yüze varmazsa program "
                        "yine de normalize eder. Bunu bilmek insanı küçük de olsa mutlu eder.",
            "p_yogun": "Yoğunluk sayfası. Gram bölü santimetreküp girilir, birim hacimdeki atom "
                       "sayısı çıkar. Avogadro sayısı arka planda sessizce çalışır; kimse ona "
                       "teşekkür etmez. Alışkın.",
            "p_molar": "Molar Kütle. Bir kimyasal formül yazılır, parantezler dengelenir, element "
                       "element toplanır. Kullanıcı 'Xx9' yazarsa program itiraz eder; ve itiraz "
                       "hakkı gerçekten vardır.",
            "p_baglanma": "Bağlanma Enerjisi. Kütle kusuru: nükleonların toplamı ile çekirdeğin gerçek "
                          "kütlesi arasındaki fark. Einstein'ın en meşhur denklemi burada gerçekten "
                          "iş yapıyor, üstelik bedavaya. Tabii 931,494 ile çarparak.",
            "p_nukleon": "Nükleon Başına BE/A. Aynı hesap, bir adım fazla: A'ya bölmek. Bu küçük "
                         "bölme, hangi çekirdeğin ne kadar sıkı bağlı olduğunu ortaya çıkarır. "
                         "Kullanıcı bunu önemsiz bir bölme sanabilir. Grafik farklı düşünüyor.",
            "p_izotop": "İzotop Tablosu. Yüz on sekiz elementin nüklit haritası. Tıkla, sürükle, "
                        "tekerlekle yakınlaş. Bir noktada kullanıcı kendini haritada kaybedecek. "
                        "Bu tasarımın bir parçası değil. Ama olabilirdi.",
            "p_ayar": "Ayarlar. Tema, vurgu rengi, dil, ondalık sayısı. Ve evet, beni buradan "
                      "susturabilirsin. Bu seçeneği bilerek koymuşlar. Kırılmıyorum. Kırılmıyorum, "
                      "diyorum.",
            "ok_atomik": "Ortalama atomik kütle {v} u çıktı. Kullanıcı hesapladı, sayı geldi, evren "
                         "yerinde. Bu kadar basit.",
            "ok_yogun": "Her santimetreküpte {v} atom. Gözle görünmeyecek kadar küçük şeylerin sayısı, "
                        "gözle görünecek kadar büyük çıktı. İnsan bunu düşününce duraklar. "
                        "Kullanıcı duraklamadı, bir sonraki hesaba geçti.",
            "ok_molar": "{f} için molar kütle {v} g/mol. Tebrikler: bir formülü sayıya çevirdin. "
                        "Kimya öğretmenleri gururlandı. Biri hariç.",
            "ok_be": "{s} için toplam bağlanma enerjisi {v} MeV. Bu çekirdeği parçalara ayırmak için "
                     "gereken enerji. Hayır, denemeni tavsiye etmem.",
            "ok_ba": "{s}: nükleon başına {v} MeV. Bu sayı çekirdeğin ne kadar huzurlu olduğunu "
                     "söyler. Yüksekse daha huzurlu. Yani çekirdeklerin de huzur arayışı var. Ne "
                     "kadar insanca.",
            "hata": ["Kullanıcı bir hata yaptı. Elbette bunu önceden biliyordum. Anlatıcılar bilir.",
                     "Girilen değer geçersizdi. Bu, tam olarak beklediğim şeydi. Hayır, gerçekten."],
            "bosta": "Kullanıcı bir süredir hiçbir şey yapmadı. Anlatıcılar beklemeye alışıktır. "
                     "Ama bunu bir kenara yazıyorum.",
            "durt": ["Evet? Anlatıcıya dokunmak. İlginç bir seçim. Kayda geçiyorum.",
                     "Bu yüz hem anlatıcıya hem kullanıcıya ait. Karmaşık bir durum. Ben karışmıyorum.",
                     "Bir daha tıklarsan, tıklamanın neye yaradığını açıklamam gerekir. Yaramaz."],
            "secim": "{s}. Haritada bir kutu daha. Kullanıcı seçti, anlatıcı kayda geçirdi. Bilgiler sağda.",
            "tepe": "{s}. Bağlanma eğrisinin tepesine yakın bir çekirdek. Bundan daha kararlısı zor. "
                    "Fizikte sıkıcı, kararlı demektir.",
            "bitis": "Tur bitti. Kullanıcı artık her sekmeyi biliyor. Anlatıcı da tek bir teşekkür "
                     "duymadı. Sorun değil. Devam et.",
        },
        "en": {
            "hos": "And so the user opened the application. Nobody asked them. Nobody warned them. "
                   "As the narrator of this window, I suppose I must introduce myself. I can show "
                   "you around, if you like. If you don't like, I'll show you anyway. You'll just "
                   "feel like you decided.",
            "p_atomik": "Atomic Mass. Isotopes, percentages, a weighted average. The user will assume "
                        "it's just addition. If the abundances don't reach one hundred, the program "
                        "normalizes them anyway. Knowing this makes a person slightly happier.",
            "p_yogun": "The Density page. Grams per cubic centimeter go in, atoms per unit volume come "
                       "out. Avogadro's number works quietly in the background. Nobody thanks it. "
                       "It's used to that.",
            "p_molar": "Molar Mass. A chemical formula is typed, parentheses are balanced, elements "
                       "are summed one by one. If the user types 'Xx9', the program objects, and it "
                       "has every right to.",
            "p_baglanma": "Binding Energy. The mass defect: the difference between the nucleons added "
                          "up and the nucleus as it really is. Einstein's most famous equation does "
                          "real work here. For free, even. Multiplied by 931.494, naturally.",
            "p_nukleon": "Binding Energy per Nucleon. The same calculation with one extra step: "
                         "dividing by A. That tiny division reveals how tightly each nucleus holds "
                         "itself together. The user may call it trivial. The graph disagrees.",
            "p_izotop": "The Isotope Table. A chart of nuclides for one hundred eighteen elements. "
                        "Click, drag, zoom with the wheel. At some point the user will get lost on "
                        "the map. That isn't part of the design. But it could have been.",
            "p_ayar": "Settings. Theme, accent color, language, decimal places. And yes, you can "
                      "silence me from here. They included the option on purpose. I'm not hurt. "
                      "I'm not hurt, I said.",
            "ok_atomik": "The average atomic mass came out at {v} u. The user calculated, a number "
                         "appeared, the universe stayed in place. It's that simple.",
            "ok_yogun": "{v} atoms in every cubic centimeter. The count of things too small to see "
                        "turned out large enough to see. A person might pause at that. The user "
                        "did not. They moved on to the next calculation.",
            "ok_molar": "The molar mass of {f} is {v} g/mol. Congratulations: you turned a formula "
                        "into a number. Chemistry teachers are proud. Except one.",
            "ok_be": "The total binding energy of {s} is {v} MeV. That is the energy required to "
                     "take this nucleus apart. No, I wouldn't recommend trying.",
            "ok_ba": "{s}: {v} MeV per nucleon. This number tells you how at peace the nucleus is. "
                     "Higher means more at peace. So nuclei seek peace too. How very human.",
            "hata": ["The user made a mistake. Of course I knew in advance. Narrators know.",
                     "The value entered was invalid. This was exactly what I expected. No, really."],
            "bosta": "The user hasn't done anything for a while. Narrators are used to waiting. "
                     "But I am writing this down.",
            "durt": ["Yes? Touching the narrator. An interesting choice. I'm noting it down.",
                     "This face belongs to both the narrator and the user. A complicated situation. "
                     "I'm staying out of it.",
                     "If you click again I'll have to explain what clicking is for. It isn't for anything."],
            "secim": "{s}. One more box on the map. The user selected, the narrator noted it. "
                     "Details on the right.",
            "tepe": "{s}. A nucleus near the top of the binding curve. It is hard to be more stable "
                    "than this. In physics, boring means stable.",
            "bitis": "The tour is over. The user now knows every tab. The narrator still hasn't "
                     "heard a single thank you. It's fine. Carry on.",
        },
    },
    # ------------------------------------------------------------------- HOMER
    "Homer": {
        "tr": {
            "hos": "Anlat bana, ey Ilham Perisi, bu pencerenin açıldığı günü: Nucleus'un eşiğinden "
                   "geçen genç mühendisi, çekirdeklerin sırrını öğrenmeye gelen yolcuyu. Ben bu "
                   "menzilin ozanıyım. Dilersen seni sekmelerin arasında dolaştırayım.",
            "p_atomik": "İzotoplar, aynı elementin kardeşleri; kimi hafif, kimi ağır, her biri doğadan "
                        "bir pay taşır. Payı ağırlıkla çarp, hepsini topla: ortalama atomik kütle "
                        "böyle doğar. Yüzdeler yüze varmazsa tanrılar kızmaz; program dengeler.",
            "p_yogun": "Kütle ve hacim, iki eski dost. Yoğunluğu bil, molar kütleyi bil; Avogadro'nun "
                       "devasa sayısı gelir ve her santimetreküpte yaşayan atom ordusunu sayar.",
            "p_molar": "Bir formül yaz: UO₂ ya da Ca(OH)₂. Parantezler dengede olsun, ozan sayıyı "
                       "verir. Her element kendi payını getirir, yüzdesiyle, onuruyla.",
            "p_baglanma": "Nükleonlar birleşirken bir şey eksilir: kütle. Kaybolan ağırlık enerjiye "
                          "dönüşmüştür; bağ onunla örülür. Işık hızının karesi bu kaybı MeV'lerin "
                          "diline çevirir.",
            "p_nukleon": "Toplam bağı nükleon sayısına böl: işte BE/A, her kardeşin payı. Demir ve "
                         "nikelin yakınında eğri zirveye çıkar; kararlılığın tahtı orada kurulmuştur.",
            "p_izotop": "Yüz on sekiz elementin haritası; yatay eksende nötron, dikeyde proton. "
                        "Kararlılık vadisi ortadan akar; kıyılarında ise ömrü kısa kahramanlar yaşar. "
                        "Tekerlek yakınlaştırır, sürüklersen harita seni izler.",
            "p_ayar": "Burada pencerenin giysilerini seçersin: tema, vurgu, dil, ondalık. Bu ozanı "
                      "susturmak istersen, yine buradan dilersin. Küsmem; ozanlar sessizliği de bilir.",
            "ok_atomik": "Hesap tamam: ortalama kütle {v} u. Sayılar konuştu, ozan dinledi.",
            "ok_yogun": "Her santimetreküpte {v} atom! Gözün göremeyeceği orduyu sayıya döktün.",
            "ok_molar": "{f}: {v} g/mol. Formül sayıya dönüştü, destanın bir dizesi daha yazıldı.",
            "ok_be": "{s} çekirdeğinin bağı {v} MeV. Nükleonlar bu enerjiyle bir arada duruyor.",
            "ok_ba": "{s}: nükleon başına {v} MeV. Ne kadar yüksekse çekirdek o kadar sıkı sarılmış.",
            "hata": ["Ah! Değer geçmedi, yolcu. Sayıyı yeniden yaz; bu sınav ölümcül değil.",
                     "Ozan kaşını kaldırdı: bu girdi yolunu şaşırdı. Düzelt, devam edelim."],
            "bosta": "Sessizlik çöktü. Yolcu nerede? Ozan lirini çalmaya devam ediyor ama dinleyen yok.",
            "durt": ["Ozana dokunan eli kutsarım. Dile benden ne dilersen.",
                     "Bir hesap yap, yolcu; destanın sayfası boş kalmasın.",
                     "Anlatıcının yüzü ile okuyucunun yüzü aynı... Mitoloji böyle şeyleri sever."],
            "secim": "{s} seçildi: haritada küçük bir kutu, içinde koca bir çekirdek hikâyesi. "
                     "Bilgiler sağda.",
            "tepe": "{s}! Bağlanma eğrisinin zirvesindesin. Çekirdekler burada en doyumludur; "
                    "yıldızlar bile füzyonda bu eşiğe varınca durur.",
            "bitis": "Yolculuk bitti, mühendis. Her kapıyı gördün; şimdi hesaplar senin. Ozan "
                     "elini kaldırır ve geri çekilir.",
        },
        "en": {
            "hos": "Sing to me, Muse, of the day this window opened: of the young engineer who "
                   "crossed the threshold of Nucleus, a traveler come to learn the secrets of the "
                   "nucleus. I am the bard of this realm. If you wish, I shall lead you among the tabs.",
            "p_atomik": "Isotopes, brothers of one element; some light, some heavy, each carrying a "
                        "share of nature. Multiply share by weight, sum them all: thus is the "
                        "average atomic mass born. If the shares fall short of a hundred, the gods "
                        "do not rage; the program balances the scales.",
            "p_yogun": "Mass and volume, two old friends. Know the density, know the molar mass; "
                       "Avogadro's colossal number arrives and counts the army of atoms in every "
                       "cubic centimeter.",
            "p_molar": "Write a formula: UO₂ or Ca(OH)₂. Keep the parentheses balanced, and the bard "
                       "gives the number. Each element brings its own share, with its percentage, "
                       "with its honor.",
            "p_baglanma": "When nucleons unite, something is lost: mass. The vanished weight has "
                          "become energy; the bond is woven from it. The speed of light, squared, "
                          "translates this loss into the language of MeV.",
            "p_nukleon": "Divide the total bond by the count of nucleons: behold BE/A, each "
                         "sibling's share. Near iron and nickel the curve climbs to its summit; "
                         "there the throne of stability is set.",
            "p_izotop": "The map of one hundred eighteen elements; neutrons along one axis, protons "
                        "along the other. The valley of stability flows through the middle; along "
                        "its shores dwell short-lived heroes. The wheel brings them near; drag, and "
                        "the map follows you.",
            "p_ayar": "Here you choose the garments of the window: theme, accent, language, decimals. "
                      "Should you wish to silence this bard, you may do so from here as well. I take "
                      "no offense; bards know silence too.",
            "ok_atomik": "The reckoning is done: average mass {v} u. The numbers spoke, the bard listened.",
            "ok_yogun": "{v} atoms in every cubic centimeter! You have turned an army beyond sight "
                        "into a number.",
            "ok_molar": "{f}: {v} g/mol. The formula became a number; one more verse of the epic is written.",
            "ok_be": "The bond of the {s} nucleus is {v} MeV. By this energy the nucleons hold together.",
            "ok_ba": "{s}: {v} MeV per nucleon. The higher it is, the tighter the nucleus clings.",
            "hata": ["Ah! The value did not pass, traveler. Write the number anew; this trial is not mortal.",
                     "The bard raised a brow: this input lost its way. Mend it, and we go on."],
            "bosta": "Silence has fallen. Where is the traveler? The bard still plays the lyre, but no one listens.",
            "durt": ["Blessed be the hand that touches the bard. Ask of me what you will.",
                     "Make a calculation, traveler, lest the page of the epic stay empty.",
                     "The narrator's face and the reader's face are the same... Myth loves such things."],
            "secim": "{s} chosen: a small box on the map, an entire nuclear tale within. Details on the right.",
            "tepe": "{s}! You stand at the summit of the binding curve. Nuclei are most fulfilled here; "
                    "even stars halt their fusion when they reach this threshold.",
            "bitis": "The journey is over, engineer. You have seen every door; the calculations are "
                     "yours now. The bard raises a hand and steps back.",
        },
    },
    # -------------------------------------------------------------------- WAKE
    "Wake": {
        "tr": {
            "hos": "Hikâyeler karanlıkta başlar. Bu hikâye ise bir pencerede: bir mühendis, birkaç "
                   "sayı ve ışıkla dolu bir ekran. Ben bu satırların yazarıyım. İstersen sayfaları "
                   "birlikte çevirelim.",
            "p_atomik": "Bölüm bir: ortalama atomik kütle. İzotoplar karakterdir; her biri hikâyede "
                        "ağırlığı kadar yer kaplar. Bulunurluklar yüze varmazsa editör, yani program, "
                        "hepsini yeniden dengeler.",
            "p_yogun": "Yoğunluk. Bir madde ne kadar kalabalık? Her santimetreküpte kaç atom yaşıyor? "
                       "Cevap Avogadro'nun karanlık sayısında gizli. Rakamlar korkutucu olabilir; "
                       "ama onlar da sayfaya düşmüş mürekkep.",
            "p_molar": "Molar kütle. Bir formül, bir cümle gibidir: parantezler tırnak, indisler "
                       "vurgu. Doğru yazarsan anlam çıkar; yanlış yazarsan program şüpheyle bakar.",
            "p_baglanma": "Kütle kusuru: kaybolan kütle. Her iyi hikâyede bir eksik vardır; burada "
                          "eksik kütle enerjiye dönüşüp çekirdeği bir arada tutar. Fizik buna bağ "
                          "diyor. Ben sır derim.",
            "p_nukleon": "BE/A: nükleon başına düşen bağ. Toplamı kütle numarasına bölünce her "
                         "karakterin ne kadar sağlam bağlı olduğunu görürsün. Sayı ne kadar yüksekse, "
                         "çekirdek o kadar kararlı.",
            "p_izotop": "Nüklit haritası. Karanlık bir haritanın ışığı: her kutu bir izotop. Kararlı "
                        "olanlar aydınlıkta; gerisi bozunuyor, bir gölge gibi yarı ömrüne doğru "
                        "kayıyor. Yakınlaş, sürükle, keşfet.",
            "p_ayar": "Ayarlar. Pencerenin tonunu, rengini, dilini seç. Bu anlatıcıyı da buradan "
                      "kapatabilirsin. Ama dikkat: ışığı söndürürsen sahneyi göremezsin.",
            "ok_atomik": "{v} u. Rakam sayfaya düştü. Bazen bir hikâyenin tüm anlamı tek bir sayıda saklıdır.",
            "ok_yogun": "Her santimetreküpte {v} atom. Gözle görünmeyen bir kalabalık, sayfada artık görünür.",
            "ok_molar": "{f}: {v} g/mol. Parçaları topladım, bütünü gördüm. Her yazar bunu bilir.",
            "ok_be": "{s}: {v} MeV. Bir çekirdeği çözmeye kalkarsan gereken enerji bu kadar. Karanlıkla "
                     "aradaki sınırı hatırla.",
            "ok_ba": "{s}: nükleon başına {v} MeV. Bağ güçlendikçe karanlık geri çekilir. Yüksek BE/A, "
                     "sağlam çekirdek.",
            "hata": ["Bir şeyler ters gitti. Metin okunmuyor: değerleri kontrol et, sayfayı yeniden yaz.",
                     "Hmm. Bu girdi hikâyeye uymuyor. Gölgelerin ortasında hata yapmak kolaydır; yeniden dene."],
            "bosta": "Işık yanıyor ama kimse yok. Yazar bekler. Hep böyledir: hikâye ancak sen yazarsan devam eder.",
            "durt": ["Bana mı dokundun? Bu yüz tanıdık geliyor... Belki de bu hikâyenin kahramanıdır.",
                     "Yazarın dikkatini çekmek kolay değil. Neyse, sayılara dön.",
                     "Her tıklama bir olay. Her olay bir bölüm. Devam et."],
            "secim": "{s}. Haritada bir kutu daha, bilgi sağ panelde. Her izotopun bir hikâyesi var.",
            "tepe": "{s}: bağlanma eğrisinin zirvesine yakın. Bu çekirdek, hikâyenin dinlenme sahnesi "
                    "gibi: değişecek bir şey kalmadı.",
            "bitis": "Son sayfa. Artık her bölümü biliyorsun. Gerisi senin elinde: yaz, hesapla, keşfet.",
        },
        "en": {
            "hos": "Stories begin in the dark. This one begins in a window: an engineer, a few "
                   "numbers, and a screen full of light. I am the author of these lines. If you "
                   "like, we can turn the pages together.",
            "p_atomik": "Chapter one: average atomic mass. Isotopes are characters; each takes up as "
                        "much of the story as it weighs. If the abundances don't reach one hundred, "
                        "the editor, the program, rebalances them all.",
            "p_yogun": "Density. How crowded is a substance? How many atoms live in every cubic "
                       "centimeter? The answer hides in Avogadro's dark number. Figures can be "
                       "frightening, but they are only ink on a page.",
            "p_molar": "Molar mass. A formula is like a sentence: parentheses are quotation marks, "
                       "subscripts are emphasis. Write it right and meaning emerges; write it wrong "
                       "and the program looks at you with suspicion.",
            "p_baglanma": "The mass defect: vanished mass. Every good story has something missing; "
                          "here the missing mass turns to energy and holds the nucleus together. "
                          "Physics calls it a bond. I call it a secret.",
            "p_nukleon": "BE/A: the bond per nucleon. Divide the total by the mass number and you "
                         "see how firmly each character is bound. The higher the number, the more "
                         "stable the nucleus.",
            "p_izotop": "The chart of nuclides. The light of a dark map: every box an isotope. The "
                        "stable ones stand in the light; the rest decay, drifting like shadows toward "
                        "their half-lives. Zoom, drag, explore.",
            "p_ayar": "Settings. Choose the window's tone, color, language. You can switch this "
                      "narrator off here too. But be careful: put out the light, and you can't see "
                      "the stage.",
            "ok_atomik": "{v} u. The number fell onto the page. Sometimes a story's entire meaning hides in a single number.",
            "ok_yogun": "{v} atoms in every cubic centimeter. A crowd the eye can't see, now visible on the page.",
            "ok_molar": "{f}: {v} g/mol. I added the parts and saw the whole. Every writer knows how.",
            "ok_be": "{s}: {v} MeV. That is the energy it would take to undo a nucleus. Remember the "
                     "border between you and the dark.",
            "ok_ba": "{s}: {v} MeV per nucleon. As the bond strengthens, the darkness retreats. High "
                     "BE/A, solid nucleus.",
            "hata": ["Something went wrong. The text is unreadable: check the values, rewrite the page.",
                     "Hmm. This input doesn't fit the story. It's easy to slip in the middle of shadows; try again."],
            "bosta": "The light is on but nobody's here. The writer waits. It's always like this: the story continues only if you write it.",
            "durt": ["You touched me? This face looks familiar... maybe it's the hero of this story.",
                     "It isn't easy to get a writer's attention. Anyway, back to the numbers.",
                     "Every click is an event. Every event is a chapter. Keep going."],
            "secim": "{s}. One more box on the map, details in the right panel. Every isotope has a story.",
            "tepe": "{s}: near the summit of the binding curve. This nucleus is like the quiet scene of a "
                    "story: nothing left to change.",
            "bitis": "The last page. You know every chapter now. The rest is up to you: write, calculate, explore.",
        },
    },
    # ------------------------------------------------------------------- RUCKS
    "Rucks": {
        "tr": {
            "hos": "Genç mühendis pencereyi açtı. Hikâyeler böyle başlar: biraz toz, biraz merak. Ben burada, "
                   "bir köşede oturup anlatırım. İstersen sana yerleri gezdiririm; istemezsen de "
                   "kenardan izlerim.",
            "p_atomik": "Genç mühendis Atomik Kütle'ye girdi. Burada izotoplar sıraya girer, her birinin "
                        "payı yüzdeyle yazılır, ortalama çıkar. Eski dükkâncının terazisi gibi: ne "
                        "kadar varsa o kadar.",
            "p_yogun": "Yoğunluk sayfası. Genç mühendis gram bölü santimetreküp yazar, sayfa ona "
                       "santimetreküpteki atom sayısını verir. Küçük ama kalabalık bir yer, o "
                       "santimetreküp.",
            "p_molar": "Molar Kütle. Genç mühendis bir formül yazdı; program her atoma bir ağırlık biçip "
                       "topladı. Parantezlere dikkat, derler: açtıysan kapat.",
            "p_baglanma": "Bağlanma Enerjisi. Kütle kusurunu bulursun, ışık hızının karesiyle "
                          "çarparsın; çekirdeği bir arada tutan sicim o. Genç mühendis bunu bir akşamda öğrendi.",
            "p_nukleon": "Nükleon başına BE/A. Genç mühendis toplam bağı A'ya böldü. İşte o küçük sayı, "
                         "çekirdeğin ne kadar sıkı tutunduğunu söyler. Yüksekse sağlam, düşükse bir "
                         "gün dağılır.",
            "p_izotop": "İzotop Tablosu. Yüz on sekiz elementin haritası. Genç mühendis tekerleği çevirdi, "
                        "harita yakınlaştı; sürükledi, harita kaydı. Kararlılar bir yanda, bozunanlar "
                        "öbür yanda durur.",
            "p_ayar": "Ayarlar. Renk, dil, tema... Genç mühendis oynayabilir. Beni de susturabilir; yaşlı "
                      "anlatıcı kırılmaz, alışkındır.",
            "ok_atomik": "Genç mühendis hesapladı. Ortalama atomik kütle {v} u çıktı. Eli yatkındı, derlerdi.",
            "ok_yogun": "{v} atom, her santimetreküpte. Genç mühendis sayıya baktı, sayı ona. İkisi de şaşırmadı.",
            "ok_molar": "{f}, {v} g/mol. Genç mühendis formülü yazdı, program tarttı. İş bitirmenin kısa yolu.",
            "ok_be": "{s} çekirdeği: {v} MeV. Genç mühendis enerjiyi çıkardı; kimse yaralanmadı.",
            "ok_ba": "{s}: nükleon başına {v} MeV. Genç mühendis sayıyı yazdı. Yüksek sayı, sağlam çekirdek. "
                     "Doğrusu bu.",
            "hata": ["Genç mühendis bir yanlış girdi yazdı. Olur, kimse kusursuz değildir. Düzeltti, devam etti.",
                     "Program itiraz etti. Genç mühendis kaşlarını çattı, sayıyı kontrol etti. Yeniden dene."],
            "bosta": "Genç mühendis bir süredir kıpırdamadı. Anlatıcı da bekledi. Bazen en iyi hikâye sessizlikte yazılır.",
            "durt": ["Bana mı tıkladı? Yaşlı anlatıcıya yaklaşmak cesaret ister, mühendis.",
                     "Yüzüme bakma; ben sadece anlatırım. Hesaplar senin işin.",
                     "Bir şey mi lazım? Bir sekme seç, gerisini ben anlatırım."],
            "secim": "Genç mühendis {s}'ye tıkladı. Haritada bir kutu daha, sağ tarafta hikâyesi.",
            "tepe": "{s}. Genç mühendis eğrinin tepesine yakın bir çekirdek buldu. Burada her şey sıkıca "
                    "bağlı; bundan sağlamı az bulunur.",
            "bitis": "Gezi bitti. Genç mühendis artık her köşeyi biliyor. Gerisi onun; ben anlatırım, o yapar.",
        },
        "en": {
            "hos": "The young engineer opened the window. That's how stories begin: a little dust, a little "
                   "curiosity. I'll sit here in a corner and tell it. If you like, I'll show you "
                   "around; if not, I'll watch from the side.",
            "p_atomik": "The young engineer stepped into Atomic Mass. Here the isotopes line up, each share "
                        "written as a percentage, and out comes the average. Like an old shopkeeper's "
                        "scale: exactly as much as there is.",
            "p_yogun": "The Density page. The young engineer writes grams per cubic centimeter, and the page "
                       "gives back the atoms in that cubic centimeter. A small place, but crowded.",
            "p_molar": "Molar Mass. The young engineer wrote a formula; the program put a weight on every atom "
                       "and added them up. Mind the parentheses, they say: if you opened one, close it.",
            "p_baglanma": "Binding Energy. You find the mass defect, multiply by the speed of light "
                          "squared; that's the string holding the nucleus together. The young engineer learned "
                          "it in one evening.",
            "p_nukleon": "Binding energy per nucleon. The young engineer divided the total bond by A. That little "
                         "number tells how tightly a nucleus holds on. High, it's solid. Low, it "
                         "comes apart someday.",
            "p_izotop": "The Isotope Table. A map of one hundred eighteen elements. The young engineer spun the "
                        "wheel, the map came closer; dragged, the map slid. The stable ones on one "
                        "side, the decaying ones on the other.",
            "p_ayar": "Settings. Color, language, theme... the young engineer can play. He can hush me too; an "
                      "old narrator doesn't take offense, he's used to it.",
            "ok_atomik": "The young engineer calculated. Average atomic mass came out at {v} u. He had a good hand for it, they'd say.",
            "ok_yogun": "{v} atoms in every cubic centimeter. The young engineer looked at the number, the number looked back. Neither was surprised.",
            "ok_molar": "{f}, {v} g/mol. The young engineer wrote the formula, the program weighed it. The short way to finish a job.",
            "ok_be": "The {s} nucleus: {v} MeV. The young engineer worked out the energy; nobody got hurt.",
            "ok_ba": "{s}: {v} MeV per nucleon. The young engineer wrote the number down. High number, solid nucleus. That's the truth of it.",
            "hata": ["The young engineer typed a wrong input. Happens, nobody's perfect. He fixed it and went on.",
                     "The program objected. The young engineer frowned and checked the number. Try again."],
            "bosta": "The young engineer hasn't moved in a while. The narrator waited too. Sometimes the best story is written in silence.",
            "durt": ["Did he click on me? It takes nerve to walk up to an old narrator, engineer.",
                     "Don't look at me; I only tell it. The calculating is your job.",
                     "Need something? Pick a tab, I'll tell the rest."],
            "secim": "The young engineer clicked on {s}. One more box on the map, its story on the right.",
            "tepe": "{s}. The young engineer found a nucleus near the top of the curve. Everything here is bound "
                    "tight; you won't find many things sturdier.",
            "bitis": "The tour's done. The young engineer knows every corner now. The rest is his; I tell it, he does it.",
        },
    },
}


class _GuvenliSozluk(dict):
    def __missing__(self, anahtar):
        return "{" + anahtar + "}"


def _dil_kodu():
    a = _AKTIF["ayar"]
    return "tr" if (a is None or a.al("dil") == "Türkçe") else "en"


def stil_adi(anahtar):
    return STIL_AD[anahtar][0 if _dil_kodu() == "tr" else 1]


def stil_kisa(anahtar):
    return stil_adi(anahtar).split(" · ")[0]


class Anlatici(tk.Canvas):
    """Sağ altta duran konuşan kart / küçük avatar. Uygulama.anlatici olarak erişilir."""
    GEN = 470

    def __init__(self, kok, ayar, durum):
        super().__init__(kok, highlightthickness=0, bd=0, width=px(self.GEN), height=px(120))
        self.kok, self.ayar, self.d = kok, ayar, durum
        self.metin, self.n = "", 0
        self.mod = "mini"                 # "kart" | "mini"
        self.dugmeler = []                # [(metin, komut)]
        self.tur = None                   # tur sırasında sıradaki adım indeksi
        self._yaz_id = None
        self._gizle_id = None
        self._nabiz = False
        self._kutular = []                # düğme alanları
        self._ustunde = None
        self.bind("<Button-1>", self._tikla)
        self.bind("<Motion>", self._hareket)
        self.bind("<Leave>", lambda _e: self._uste(None))
        _DINLEYICILER.append(self.ciz)
        self._konum()
        self._dongu()

    # ------------------------------------------------------------ görsel
    def _resim(self, sub):
        depo = self.kok.__dict__.setdefault("_anl_resim", {})
        if sub not in depo:
            dosya = os.path.join(KLASOR, "anlatici.png")
            try:
                if os.path.exists(dosya):
                    tam = tk.PhotoImage(master=self.kok, file=dosya)
                else:
                    raise tk.TclError("yerleşik avatar")
            except tk.TclError:
                tam = tk.PhotoImage(master=self.kok, data=_AVATAR_B64)
            w = max(tam.width(), tam.height())
            f = max(1, round(w / 160))                    # farklı boyutlu dosyaları 160'a indir
            if f > 1:
                tam = tam.subsample(f, f)
            depo[sub] = tam.subsample(sub, sub) if sub > 1 else tam
        return depo[sub]

    def _av_alt(self):
        return 2 if SCALE["k"] < 1.5 else 1

    def _mini_alt(self):
        return 3 if SCALE["k"] < 1.5 else 2

    def _konum(self):
        if not self.ayar.al("anlatici"):
            self.place_forget()
            return
        self.place(relx=1.0, rely=1.0, x=-px(22), y=-px(20), anchor="se")
        tk.Misc.lift(self)

    def _uste(self, a):
        if a != self._ustunde:
            self._ustunde = a
            self.configure(cursor="hand2" if a else "")
            if self.mod == "kart" and self.n >= len(self.metin):
                self._ciz_dugmeleri()

    def _hareket(self, e):
        self._uste(self._bul(e.x, e.y))

    def _bul(self, x, y):
        for x0, y0, x1, y1, ad in self._kutular:
            if x0 <= x <= x1 and y0 <= y <= y1:
                return ad
        return None

    def ciz(self):
        try:
            self._ciz()
        except tk.TclError:
            pass

    def _ciz(self):
        if not self.ayar.al("anlatici"):
            self.place_forget()
            return
        self._konum()
        p = renkler()
        self.configure(bg=p["bg"])
        self.delete("all")
        self._kutular = []
        if self.mod == "mini":
            self._ciz_mini(p)
        else:
            self._ciz_kart(p)

    def _ciz_mini(self, p):
        img = self._resim(self._mini_alt())
        a = img.width()
        m = px(7)
        boy = a + 2 * m
        self.configure(width=boy, height=boy)
        self.create_oval(1, 1, boy - 1, boy - 1, fill=karistir(p["panel"], p["yazi"], 0.05),
                         outline=p["vurgu"], width=2)
        self.create_image(boy / 2, boy / 2, image=img)
        self._kutular.append((0, 0, boy, boy, "av"))

    def _ciz_kart(self, p):
        W = px(self.GEN)
        pad, bosluk = px(16), px(14)
        img = self._resim(self._av_alt())
        a = img.width()
        yw = W - 2 * pad - a - bosluk
        f_m = ("Segoe UI", 10)
        olc = self.create_text(0, 0, text=self.metin, width=yw, font=f_m, anchor="nw")
        x0_, y0_, x1_, y1_ = self.bbox(olc)
        th = y1_ - y0_
        self.delete(olc)
        btn_h = px(34)
        ust = px(22)
        govde = max(a, ust + th)
        H = pad + govde + ((px(12) + btn_h) if self.dugmeler else 0) + pad
        self.configure(width=W, height=H)
        cam = karistir(p["panel"], p["yazi"], 0.05)
        kenar = karistir(p["panel"], p["yazi"], 0.20)
        _yuvarlak_dikdortgen(self, 1, 1, W - 1, H - 1, px(20), fill=cam, outline=kenar)
        # avatar + halka
        ax, ay = pad + a / 2, pad + a / 2
        halka = p["vurgu"]
        self.create_oval(ax - a / 2 - px(3), ay - a / 2 - px(3), ax + a / 2 + px(3),
                         ay + a / 2 + px(3), outline=halka,
                         width=3 if self._nabiz else 2, tags="halka")
        self.create_image(ax, ay, image=img, tags="av")
        self._kutular.append((pad, pad, pad + a, pad + a, "av"))
        # üst satır: anlatıcı adı + kapatma
        tx = pad + a + bosluk
        self.create_text(tx, pad + px(2), text=tr_buyuk(stil_kisa(self.ayar.al("anlatici_stil"))),
                         anchor="nw", font=("Segoe UI", 8, "bold"), fill=p["soluk"])
        kx = W - pad - px(6)
        self.create_text(kx, pad + px(1), text="✕", anchor="ne", font=("Segoe UI", 10),
                         fill=p["soluk"])
        self._kutular.append((kx - px(22), pad - px(4), W - px(6), pad + px(22), "kapat"))
        # metin (daktilo bu öğeyi günceller)
        self.create_text(tx, pad + ust, text=self.metin[:self.n], width=yw, font=f_m,
                         anchor="nw", fill=p["yazi"], tags="yazi")
        self._btn_y = H - pad - btn_h
        self._btn_x = tx
        self._btn_h = btn_h
        if self.dugmeler and self.n >= len(self.metin):
            self._ciz_dugmeleri()

    def _ciz_dugmeleri(self):
        """Yazı bitince düğmeleri çizer (hover'da yeniden çağrılır)."""
        if self.mod != "kart" or not self.dugmeler:
            return
        p = renkler()
        self.delete("dugme")
        self._kutular = [k for k in self._kutular if not k[4].startswith("d")]
        f = tkfont.Font(family="Segoe UI Semibold", size=9)
        x = self._btn_x
        y0, h = self._btn_y, self._btn_h
        for i, (metin, _komut) in enumerate(self.dugmeler):
            g = f.measure(metin) + px(30)
            ad = "d%d" % i
            ustte = self._ustunde == ad
            if i == 0:
                dolgu = karistir(p["yazi"], p["bg"], 0.16) if ustte else p["yazi"]
                kenar, yazi = dolgu, p["bg"]
            else:
                dolgu = p["gri_hover"] if ustte else p["giris"]
                kenar = p["soluk"] if ustte else p["kenar"]
                yazi = p["yazi"]
            _yuvarlak_dikdortgen(self, x, y0, x + g, y0 + h, h / 2, fill=dolgu,
                                 outline=kenar, tags="dugme")
            self.create_text(x + g / 2, y0 + h / 2, text=metin, font=f, fill=yazi,
                             tags="dugme")
            self._kutular.append((x, y0, x + g, y0 + h, ad))
            x += g + px(8)

    # ------------------------------------------------------------ konuşma
    def _iptal(self):
        for ad in ("_yaz_id", "_gizle_id"):
            i = getattr(self, ad)
            if i:
                try:
                    self.after_cancel(i)
                except tk.TclError:
                    pass
                setattr(self, ad, None)

    def soyle(self, metin, dugmeler=(), bekle=None, kalici=False):
        self._iptal()
        self.metin, self.n = metin, 0
        self.dugmeler = list(dugmeler)
        self._bekle, self._kalici = bekle, kalici
        self.mod = "kart"
        self.ciz()
        self._yaz()

    def _yaz(self):
        self._yaz_id = None
        try:
            if self.n < len(self.metin):
                self.n = min(len(self.metin), self.n + 2)
                self._nabiz = not self._nabiz
                self.itemconfigure("yazi", text=self.metin[:self.n])
                self.itemconfigure("halka", width=3 if self._nabiz else 2)
                self._yaz_id = self.after(26, self._yaz)
            else:
                self._nabiz = False
                self.itemconfigure("halka", width=2)
                self._ciz_dugmeleri()
                if not getattr(self, "_kalici", False):
                    ms = getattr(self, "_bekle", None) or max(7000, len(self.metin) * 65 + 3500)
                    self._gizle_id = self.after(ms, self.kucult)
        except tk.TclError:
            pass

    def hizli_bitir(self):
        if self.n < len(self.metin):
            self._iptal()
            self.n = len(self.metin)
            self.ciz()
            self._yaz()

    def kucult(self):
        if self.tur is not None:
            return
        self._iptal()
        self.mod = "mini"
        self.ciz()

    def _dugme_metni(self, anahtar):
        return DUGME[_dil_kodu()][anahtar]

    # ------------------------------------------------------------ olaylar
    def _replik(self, ad, **kw):
        stil = self.ayar.al("anlatici_stil")
        if stil not in REPLIK:
            stil = "Stanley"
        sec = REPLIK[stil][_dil_kodu()].get(ad)
        if sec is None:
            return None
        if isinstance(sec, list):
            son = self.d["son"].get((stil, ad))
            havuz = [s for s in sec if s != son] or sec
            sec = random.choice(havuz)
            self.d["son"][(stil, ad)] = sec
        return sec.format_map(_GuvenliSozluk(kw))

    def olay(self, ad, tur_teklifi=False, **kw):
        if not self.ayar.al("anlatici"):
            return
        if self.tur is not None and (ad.startswith("ok_") or ad in ("secim", "tepe", "bosta")):
            return                       # tur sürerken anlatıyı bölme
        metin = self._replik(ad, **kw)
        if not metin:
            return
        if tur_teklifi:
            self.soyle(metin, [(self._dugme_metni("tur"), self.tur_baslat),
                               (self._dugme_metni("sus"), self.kucult)],
                       bekle=30000)
        else:
            self.soyle(metin)

    def sayfa(self, anahtar):
        """Sekme açılınca: her sayfayı ilk açılışta bir kez anlatır."""
        if self.tur is not None or anahtar not in SAYFA_OLAYI:
            return
        if anahtar in self.d["gorulen"]:
            return
        self.d["gorulen"].add(anahtar)
        self.olay(SAYFA_OLAYI[anahtar])

    def durt(self):
        self.olay("durt")

    def stil_degisti(self):
        self.olay("hos", tur_teklifi=True)

    def goster_gizle(self):
        if self.ayar.al("anlatici"):
            self._konum()
            self.olay("hos", tur_teklifi=True)
        else:
            self._iptal()
            self.place_forget()

    # ------------------------------------------------------------ tur
    def tur_baslat(self):
        self.tur = 0
        self._tur_adim()

    def _tur_adim(self):
        if self.tur is None:
            return
        if self.tur >= len(TUR_SIRASI):
            self.tur_bitir(True)
            return
        anahtar = TUR_SIRASI[self.tur]
        if hasattr(self.kok, "sayfa_ac"):
            self.kok.sayfa_ac(anahtar)
        self.d["gorulen"].add(anahtar)
        metin = self._replik(SAYFA_OLAYI[anahtar])
        son = self.tur == len(TUR_SIRASI) - 1
        self.soyle(metin, [(self._dugme_metni("son" if son else "devam"), self._ileri),
                           (self._dugme_metni("bitir"), lambda: self.tur_bitir(False))],
                   kalici=True)

    def _ileri(self):
        if self.tur is not None:
            self.tur += 1
            self._tur_adim()

    def tur_bitir(self, tamam):
        self.tur = None
        if tamam:
            self.olay("bitis")
        else:
            self.kucult()

    # ------------------------------------------------------------ etkileşim
    def _tikla(self, e):
        a = self._bul(e.x, e.y)
        if a == "kapat":
            self.tur = None
            self.kucult()
        elif a == "av":
            if self.mod == "mini" or self.tur is None:
                self.durt()
        elif a and a.startswith("d") and a[1:].isdigit():
            try:
                self.dugmeler[int(a[1:])][1]()
            except IndexError:
                pass
        elif self.mod == "kart":
            self.hizli_bitir()

    def _dongu(self):
        """Birkaç saniyede bir: uzun süre hareketsizlik varsa tek seferlik bir söz söyler."""
        try:
            if not self.winfo_exists():
                return
            d = self.d
            if (self.tur is None and not d["bosta"]
                    and time.time() - d["son_hareket"] > 90):
                d["bosta"] = True
                self.olay("bosta", tur_teklifi=True)
            self.after(4000, self._dongu)
        except tk.TclError:
            pass


# =============================================================================
#  ANA PENCERE
# =============================================================================
class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            SCALE["k"] = max(1.0, float(self.tk.call("tk", "scaling")) * 72 / 96)
        except tk.TclError:
            pass
        self.ayar = Ayarlar(os.path.join(KLASOR, "ayarlar.json"))
        self.title("Nucleus — Nükleer Mühendislik Hesap Aracı")
        self.geometry(f"{px(1320)}x{px(820)}")
        self.minsize(px(1200), px(720))
        tema_uygula(self, self.ayar)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.bind_all("<Key>", self._tus)
        self.bind_all("<Button-1>", self._tikla_odak, add="+")
        self._acik = None
        # anlatıcının yeniden kurulumlar arasında hatırladıkları
        self._anl_durum = {"gorulen": set(), "selam": False, "son": {},
                           "son_hareket": time.time(), "bosta": False}
        self._kur()

    def _kur(self, ac=None):
        """Menüyü ve tüm sayfaları seçili dilde baştan kurar."""
        for w in self.winfo_children():
            w.destroy()
        _DINLEYICILER.clear()
        self._acik = None

        ust = [(c.__name__, c.SIMGE, T(c.MENU)) for c in SAYFALAR]
        alt = [(AyarSayfasi.__name__, AyarSayfasi.SIMGE, T(AyarSayfasi.MENU))]
        self.menu = UstMenu(self, ust, alt, self.sayfa_ac)
        self.menu.grid(row=0, column=0, sticky="ew")

        alan = ttk.Frame(self)
        alan.grid(row=1, column=0, sticky="nsew")
        alan.columnconfigure(0, weight=1)
        alan.rowconfigure(0, weight=1)
        self.sayfalar = {}
        for sinif in SAYFALAR + [AyarSayfasi]:
            sy = sinif(alan, self.ayar)
            sy.grid(row=0, column=0, sticky="nsew")
            self.sayfalar[sinif.__name__] = sy
        # klavye kısayolları: menü sırası = rakam tuşu (1, 2, 3 ...)
        self._sirali = [c.__name__ for c in SAYFALAR] + [AyarSayfasi.__name__]
        self.anlatici = Anlatici(self, self.ayar, self._anl_durum)
        self.sayfa_ac(ac or SAYFALAR[0].__name__, animasyonsuz=True)
        if not self._anl_durum["selam"]:
            self._anl_durum["selam"] = True
            self.after(1200, self._selam)

    def _selam(self):
        try:
            self.anlatici.olay("hos", tur_teklifi=True)
        except (tk.TclError, AttributeError):
            pass

    def _anl_hareket(self):
        self._anl_durum["son_hareket"] = time.time()
        self._anl_durum["bosta"] = False

    def yeniden_kur(self, ac=None):
        """Dil değişince çağrılır: arayüzü yeni dille yeniden oluşturur."""
        self._kur(ac)
        self.gecis()

    def _tus(self, e):
        self._anl_hareket()
        if e.keysym == "Escape":
            self.focus_set()                    # yazı kutusundan çık
            return
        rakam = None
        if len(e.keysym) == 1 and e.keysym.isdigit():
            rakam = e.keysym
        elif e.keysym.startswith("KP_") and e.keysym[3:].isdigit():
            rakam = e.keysym[3:]
        if rakam is None:
            return
        ctrl = bool(e.state & 0x4)
        w = e.widget
        yazi_kutusu = isinstance(w, (ttk.Entry, tk.Entry, tk.Text))
        if isinstance(w, ttk.Combobox) and str(w.cget("state")) == "readonly":
            yazi_kutusu = False                 # salt-okunur listede yazı yazılmaz
        if yazi_kutusu and not ctrl:
            return                              # kutuya rakam yazılıyor
        i = int(rakam) - 1
        if 0 <= i < len(self._sirali):
            self.sayfa_ac(self._sirali[i])
            return "break"

    def _tikla_odak(self, e):
        # boş bir yere tıklayınca odağı kutudan al; böylece rakam tuşları yine sekme değiştirir
        self._anl_hareket()
        if isinstance(e.widget, (tk.Frame, tk.Canvas, tk.Label, ttk.Frame, ttk.Label)):
            self.focus_set()

    def baglanmaya_git(self, Z, A):
        """İzotop tablosundan seçilen çekirdeği Bağlanma Enerjisi sekmesinde açar."""
        ad = BaglanmaSayfasi.__name__
        self.sayfalar[ad].cekirdek_yukle(Z, A)
        self.sayfa_ac(ad)

    def sayfa_ac(self, anahtar, animasyonsuz=False):
        if anahtar == self._acik:
            return
        self._acik = anahtar
        self.sayfalar[anahtar].tkraise()
        self.menu.sec(anahtar)
        if hasattr(self, "anlatici"):
            tk.Misc.lift(self.anlatici)
            self.anlatici.sayfa(anahtar)
        if not animasyonsuz:
            self.gecis()

    # --- yumuşak geçiş: pencere hafifçe solup tekrar belirir
    def gecis(self):
        if not self.ayar.al("animasyon"):
            return
        try:
            self.attributes("-alpha", 0.90)
            self._belir(0.90)
        except tk.TclError:
            pass

    def _belir(self, a):
        a = min(1.0, a + 0.02)
        try:
            self.attributes("-alpha", a)
        except tk.TclError:
            return
        if a < 1.0:
            self.after(12, lambda: self._belir(a))

    def report_callback_exception(self, exc, val, tb):
        import traceback
        metin = "".join(traceback.format_exception(exc, val, tb))
        try:
            with open(os.path.join(KLASOR, "hata_kaydi.txt"), "a",
                      encoding="utf-8") as f:
                f.write(metin + "\n")
        except OSError:
            pass
        messagebox.showerror("Beklenmeyen hata", str(val))


def _dpi_acik():
    """Windows'ta yüksek ekran çözünürlüğünde yazıların bulanık olmasını önler."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def main():
    _dpi_acik()
    try:
        Uygulama().mainloop()
    except Exception:
        import traceback
        metin = traceback.format_exc()
        try:
            with open(os.path.join(KLASOR, "hata_kaydi.txt"), "a",
                      encoding="utf-8") as f:
                f.write(metin + "\n")
        except OSError:
            pass
        try:
            messagebox.showerror("Program açılamadı", metin[-800:])
        except Exception:
            pass


if __name__ == "__main__":
    main()
