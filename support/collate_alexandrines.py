from os import path

DATA_PATH = "../tmp"

ALL = "all_verses.txt"


def extract_info(line):
    raw_split = line.strip().replace('\xa0', ' ').split('\t')
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
        return True #No dieresis
    if length == '11 à 12': #dieresis
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



full_info = []
likely = []
unlikely = []

for l in open(path.join(DATA_PATH, ALL), 'r', encoding='utf8'):
    verse_info = extract_info(l)
    #merge(verse_info)
    full_info.append(verse_info)
    if filter_likely(verse_info):
        likely.append(verse_info)
    else:
        unlikely.append(verse_info)

