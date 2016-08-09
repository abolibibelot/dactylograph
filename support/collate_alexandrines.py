from os import path
from lexique_helper import load_lexique
from collections import defaultdict

DATA_PATH = "../tmp"

ALL = "all_verses.txt"


def extract_info(line):
    raw_split = line.strip().split('\t')
    if len(raw_split) != 2:
        return None
    l = [raw_split[0]]
    l.extend(raw_split[1].split(','))
    return l


def has_twelve(info):
    return len(info[1].split('/')) == 12


def add_dieresis(info):
    splits = info[1]
    desc = info[4]
    candidate = desc[desc.find('sur : ') + 6:].lower()
    phonems = ['ie', 'ia', 'ui', 'ue', 'iu']
    orig = splits.find(candidate)
    idx = splits.find(candidate)
    if idx == -1:
        return None
    repl = None
    for phonem in phonems:
        if phonem in candidate:
            repl = candidate.replace(phonem, phonem[0] + '/' + phonem[1])
            break
    if repl is None:
        return None
    info[1] = splits.replace(candidate, repl)


def filter_likely(info):
    length = info[2]
    if 'à' not in length:
        return length == '12'
    if length == '12 à 13' or length == '12 à 14':
        return True  # No dieresis
    if length == '11 à 12':  # dieresis
        add_dieresis(info)
        return True

    return False


def merge(info):
    raw = info[0]
    split = info[1]
    idx = 0
    res = ''
    for c in split:
        while idx < len(raw):
            if c == '/':
                res += '//'
                break
            if c == raw[idx]:
                res += c
                idx += 1
                break
            res += raw[idx]
            idx += 1
    info.append(res)


def filter_alex():
    full_info = []
    likely = []
    unlikely = []

    for l in open(path.join(DATA_PATH, ALL), 'r', encoding='utf8'):
        l = l.replace('\xa0', ' ')
        verse_info = extract_info(l)
        # merge(verse_info)
        full_info.append(verse_info)
        if filter_likely(verse_info):
            likely.append(verse_info)
            print(l.replace('\n', ''))
    return likely


def load_alexandrins(filepath, lex):
    res = []
    for l in open(path.join(filepath), 'r', encoding='utf8'):
        info = extract_info(l)
        if info is None:
            continue
        normalize_final(info, lex)
        res.append(info)
    return res

matches = [
            [['s'], ''],
            [['out', 'ous', 'oux'], 'ou'],
            [['art', 'ard'], 'ar'],
            ]


DECOMP_FIELD = 22
miss = set()


def normalize_final(line_info, lex):
    line = line_info[1]
    default = line.split('/')[-1]
    tmp = line.replace('/', '').replace("'",' ').rstrip().lower()
    tmp = tmp.replace('…','').replace('œ','oe').replace(')', '')

    last= tmp.split()[-1]
    if last in lex:
        line_info.append(lex[last][DECOMP_FIELD].split('-')[-1])
    else:
        line_info.append(default)
    return line_info

IDX_FINAL = 5

lexique = load_lexique()
alx = load_alexandrins('../data/alexandrins.txt', lexique)
by_final = defaultdict(list)

for l in alx:
    by_final[l[IDX_FINAL]].append(l)




