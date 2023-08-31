from plugins import query as q

data = '''1 : 530808431 : @iman_ghader : Iman ghader : True : 4 : 0
2 : 62835173 : @Mo0ortezaR : Morteza : True : 4 : 0
3 : 444556030 : @AlirezaNezami : Alireza : True : 5 : 0
4 : 108804923 : @Salar_hasemzadeh : Salar : True : 4 : 0
5 : 394214452 : @hami7v : 🇭 🇦 🇲 🇪 🇩 : True : 3 : 0
6 : 143475031 : @The_Luckiest_One : Sina : True : 4 : 0
7 : 116054120 : @aliseyyedlar : علی سیدلر | : True : 4 : 0
8 : 642796204 : @FaridAlaghmand : فرید : True : 4 : 0
9 : 406825504 : @Milad_ghader : Milad : True : 4 : 0
10 : 63123988 : @HamedZola : Hamed : True : 4 : 0
11 : 68034619 : @None : (Z.GH) : True : 0 : 0
12 : 1733716621 : @freethemandem : - M o b : True : 4 : 0
13 : 74091523 : @Vahedi_i : Vahedi : True : 4 : 0
14 : 102246942 : @mahta_mohegh : Mahta : True : 4 : 0
15 : 105530597 : @Mohsen2hb : Mohsen : True : 4 : 0
16 : 82044784 : @deuxmim : Mahssa : True : 0 : 0
17 : 98477724 : @Poonehsami : Pooneh : True : 0 : 0
18 : 5844211067 : @None : Meehdi : True : 0 : 0
19 : 76794242 : @MousaviNazanin : Nazanin Mousavi : True : 1 : 0
20 : 124922386 : @theshemoon : $|-|!\/o0oOl : True : 0 : 0
21 : 119034829 : @mahssa_mohegh : M. : True : 0 : 0
22 : 1082814346 : @aazrrzaa : A. R. : True : 4 : 0
23 : 763829797 : @None : H : True : 5 : 0
24 : 5302594013 : @H_UxD : Mohmmad Sadeq : True : 9 : 0
25 : 59023580 : @hamedeshaghii : Hamed : True : 9 : 0
26 : 127392860 : @Reihan_dnj : ☘️Reihane☘️ : True : 0 : 0
28 : 791927771 : @HabibiDev : Mahdi : True : 56 : 2
29 : 129672164 : @Hosein0351 : Hosein : True : 5 : 0
30 : 93414541 : @e_rfn : erfan : True : 0 : 0
31 : 205930201 : @Sajad_nyn : ♤sajad : True : 5 : 0
32 : 65711083 : @alifti : Ali Fattahi : True : 9 : 0
33 : 344005595 : @poshtibanitakhasosi : پشتيباني تخصصي مراکز درمانی : True : 9 : 0
34 : 35342742 : @sarsadr : Alireza : True : 9 : 0
35 : 5462865762 : @paziresh24_p24 : paziresh24 : True : 9 : 0
36 : 5484756114 : @Mersad_sl : Mersad : True : 9 : 0
37 : 449720290 : @abooheiran : Mr : True : 9 : 0
38 : 1015337707 : @M1e9h8d2i : M : True : 5 : 0
39 : 1414726588 : @M4tinBeigi : Rick ˢᵃⁿᶜʰᵉᶻ 🤍 ریک سانچز : True : 5 : 0
40 : 92354499 : @Mehdisnvd : Mehdi : True : 5 : 0
41 : 6064880102 : @const_dyna_fight : Amirsajad : True : 5 : 0
42 : 66443035 : @OneProgrammer : Mehrab : True : 9 : 0
43 : 5097544132 : @AmirH_Fayaz : Amir‌H : True : 5 : 0
44 : 1870928835 : @mahhdigh : Mahdi : True : 1 : 0
45 : 5673473829 : @Mandmd : M : True : 4 : 0
46 : 394427631 : @msdqqm : mohamad : True : 5 : 0
47 : 471204252 : @mhhm76 : محمد حسین : True : 3 : 0
48 : 158697670 : @MohammadGhader : Mohammad : True : 9 : 0
49 : 340466824 : @Maralzar : Maral : True : 5 : 0
50 : 1976114053 : @None : Hafiz Omid : True : 5 : 0
51 : 5708974459 : @ESaeedi_1380 : E. : True : 0 : 0
52 : 276203133 : @None : Aria : True : 5 : 0
53 : 101262363 : @Teluriian : marin : True : 6 : 0
54 : 5417465480 : @plokiqawse : ploki : True : 4 : 0
55 : 888853322 : @JS_Mechanic : Milad : True : 8 : 5
56 : 1998609692 : @P86KA : pkarj : True : 6 : 0
57 : 505769972 : @thelilduckling : Mahya : True : 5 : 0
58 : 84176095 : @None : Mahbubeh : True : 5 : 0
59 : 89832885 : @fajavadi : Fatemeh : True : 7 : 0
60 : 5494873511 : @ESaeedi_2001 : Kaladin : True : 4 : 0
61 : 201362835 : @Hedaiat_habibi : Hedaiat : True : 8 : 0
62 : 41026785 : @ebrahimghane : محمد ابراهیم : True : 23 : 0
63 : 579157771 : @Pooryakass : Poorya : True : 5 : 0
64 : 5326749653 : @None : Kamyar : True : 5 : 0
65 : 1308310642 : @David_D_1989 : Davoud : True : 2 : 0
66 : 114497458 : @Aleereza_zi : Alireza : True : 8 : 0
67 : 1937257850 : @navigtr : A : True : 7 : 0
68 : 5802834447 : @None : Shahryar : True : 5 : 0
69 : 166139394 : @DavoudDourvash1989 : Davoud : True : 2 : 2
70 : 331397967 : @AhmadEsmram : Ahmad : True : 8 : 0
71 : 111188232 : @me8dib : Mehdi : True : 10 : 0
72 : 72167946 : @ammiiirrrrsssss : Amir : True : 5 : 0
73 : 124020115 : @amirhosein_vedadi : امیرحسین : True : 5 : 0
74 : 910130524 : @Dani_Ze : ๔คหเ٤ł : True : 54 : 0
75 : 161623399 : @MDF5458 : Majid : True : 2 : 0
76 : 5572369913 : @Zti76 : TAHERI : True : 5 : 0
77 : 623078452 : @Svdjawd : Svdjawd : True : 2 : 0
78 : 1149089554 : @sadrashady : Sadra : True : 4 : 0
79 : 240796691 : @AliJavadi21 : Ali : True : 5 : 0
80 : 6265258501 : @MEgooneh : MEGAGON : True : 5 : 0
81 : 236823448 : @Baaabaei : Inv. Alireza : True : 9 : 0
82 : 489500554 : @Mohsenn_M : Mohsen : True : 9 : 0
83 : 771935856 : @HafezaHM : Hafez : True : 9 : 0
84 : 1034201463 : @ehsanKeyOriginal : Ehsan Key : True : 5 : 0
85 : 927575468 : @SB_Askari : صابره : True : 5 : 0
86 : 1078590891 : @Sam310q : Sama : True : 4 : 0
87 : 38108961 : @amaz13 : Ahmad : True : 32 : 0
88 : 103595826 : @go2infinity : Alireza : True : 6 : 0
89 : 762914793 : @mam0od : Mahmood : True : 2 : 0
90 : 255504158 : @Merkousha : مسعود : True : 9 : 0
91 : 278873327 : @Haiedeh_veisi : H : True : 7 : 0
92 : 2008770836 : @Amirhbbhbb : amirhb : True : 7 : 0
'''

data = data.splitlines()
for d in data:

    id = d.split(':')[1].replace(' ','')
    username = d.split(':')[2].replace(' ','')
    name = d.split(':')[3].replace(' ','')
    active = d.split(':')[4].replace(' ','')
    credit = d.split(':')[5].replace(' ','')
    invite = d.split(':')[6].replace(' ','')

    q.hset(id,'name', name)
    q.hset(id,'username',username)
    q.hset(id,'active', 'True')
    q.hset(id,'progress', 'False')
    q.hset(id,'invite', int(invite))
    q.hset(id,'credit', int(credit))
    q.lpush('studaio_users',id)
    print(f'user {id} added to studaio_users')
