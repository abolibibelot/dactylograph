DATA_PATH = "/Users/y.schwartz/poiesy/corpus/Syllaber/"

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



def filter_likely(info):
    length = info[2]
    if length == '12':
        return True
    if length in ['11', '12', '13'] and has_twelve(info):
        return True
    interv = length.strip().split(' à ')
    if len(interv) == 2 and (int(interv[0]) <= 12 <= int(interv[1])):
        return has_twelve(info)
    return False


full_info = []
likely = []
unlikely = []

for l in open(DATA_PATH + ALL, 'r', encoding='utf8'):
    verse_info = extract_info(l)

    full_info.append(verse_info)
    if filter_likely(verse_info):
        likely.append(verse_info)
    else:
        unlikely.append(verse_info)
