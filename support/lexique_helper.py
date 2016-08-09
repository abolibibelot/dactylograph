
LEXIQUE_PATH = '../data/Lexique380.txt'

fields = """
1_ortho	2_phon	3_lemme	4_cgram	5_genre	6_nombre	7_freqlemfilms2	8_freqlemlivres	9_freqfilms2	10_freqlivres
11_infover	12_nbhomogr	13_nbhomoph	14_islem	15_nblettres	16_nbphons	17_cvcv	18_p_cvcv	19_voisorth
20_voisphon	21_puorth	22_puphon	23_syll	24_nbsyll	25_cv-cv	26_orthrenv	27_phonrenv	28_orthosyll
29_cgramortho	30_deflem	31_defobs	32_old20	33_pld20	34_morphoder	35_nbmorph
""".strip().split()

def load_lexique():
    lexique = {}

    for l in open(LEXIQUE_PATH, 'r', encoding='latin1'):
        ff = l.strip().split('\t')
        lexique[ff[0]] = ff
    return lexique
