import re
from Levenshtein.StringMatcher import StringMatcher

# const

# similarity threshold
threshold = 0.3
# filter pattern
pattern1 = "[+&・_/0-9a-zA-Z!/|\"'#@*~$%^=,-.<>`，。?:; ]"
pattern2 = "[[{(].*[)}]"
# to replace irregular char
repl = ""


def compare(template: list, target: str, ac : bool = False) -> list:
    """
    for error correctness, return a list of strings whose similarity >= threshold to target in template list ,use a SequenceMatcher

    :param ac:  specify to use quick ratio
    :param template:  a list
    :param target:  a input string
    :return: return a list of strings whose similarity >= threshold to  input in descending order with similarity value
    """
    # use a SequenceMatcher to compare target
    seq = StringMatcher(None)
    seq.set_seq1(target)
    # a list of some result
    res = []

    is_1 = True if len(target) == 1 else False

    # if similarity >= threshold , add to res
    if ac:
        for item in template:
            # pre process ...
            temp = pre_filter(item)

            # compute similarity
            seq.set_seq2(temp)
            if (not is_1 or abs(len(target)-len(temp)) <= 2) and item.find(target) != -1:  # if exactly contain
                res.append((item, seq.quick_ratio()))
                pass
            elif seq.quick_ratio() >= 0.66:  # else if similar enough
                temps = seq.ratio()
                if temps >= threshold:
                    res.append((item, seq.ratio()))
                    pass
                pass
            pass
    else:
        for item in template:
            # pre process ...
            temp = pre_filter(item)

            # compute similarity
            seq.set_seq2(temp)
            if item.find(target) != -1:  # if exactly contain
                res.append((item, seq.ratio()))
                pass
            elif seq.ratio() >= threshold:  # else if similar enough
                res.append((item, seq.ratio()))
            pass

    # sort res by similarity in descending order
    res.sort(key=lambda e: e[1], reverse=True)
    return res
    pass


# print(SequenceMatcher(a="456", b="v45879").quick_ratio())
# print(StringMatcher("", "456", "4").quick_ratio())



def pre_filter(indata: str) -> str:
    """
    clean indata with pattern1 and 2 for pre-processing

    :param indata:  str - input data
    :return:  str- data be cleaned
    """
    return re.sub(pattern1, repl, re.sub(pattern2, repl, indata))
    pass

# print(re.sub("[+&・_/0-9a-zA-Z!/|\"'#@*~$%^=,-.<>`，。?:;]", "", re.sub("[{(].*[)}]", "", "壞蛋王・老五 (The Bad King Five)")))

