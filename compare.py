import re
from Levenshtein.StringMatcher import StringMatcher

# similarity threshold
default_threshold = 0.3
# filter pattern
pattern1 = "[+&・_/0-9a-zA-Z!/|\"'#@*~$%^=,-.<>`，。?:; ]"
pattern2 = "[[{(].*[)}]"
# to replace irregular char
repl = ""


def compare(template: list, target: str, threshold: float = default_threshold, ac: bool = False) -> list:
    """
    to find the strings similar  to target, return a list of strings whose similarity >= threshold in template list
    output example: [(0.9, ''apple"), (0.5, "hello")]

    :param threshold: similarity threshold
    :param ac:  specify whether to use quick ratio for similarity
    :param template:  a list for  finding the target
    :param target:  find this target int the template list
    :return: return a list of strings whose similarity >= threshold  in descending order with similarity value
    """
    # use a SequenceMatcher to compare target
    seq = StringMatcher(None)
    seq.set_seq1(target)
    # result list
    res = []

    only_one_letter = True if len(target) == 1 else False
    # if similarity >= threshold , add to res
    if ac:  # use quick ratio
        for test in template:
            # pre process ...
            item = pre_process_filter(test)

            # compute similarity
            seq.set_seq2(item)
            if (not only_one_letter or abs(len(target)-len(item)) <= 2) and item.find(target) != -1:
                # if exactly contain in substring or two string length is close, use quick compare
                res.append((seq.quick_ratio(), test))
            elif seq.quick_ratio() >= 0.66:  # else if similar enough, work for more precise compare
                ratio = seq.ratio()
                if ratio >= threshold:
                    res.append((ratio, test))
                    pass
                pass
            pass
    else:  # use real ratio
        for test in template:
            # pre process ...
            item = pre_process_filter(test)

            # compute similarity
            seq.set_seq2(item)
            if item.find(target) != -1:  # if exactly contain in substring
                res.append((seq.ratio(), test))
            elif seq.ratio() >= threshold:  # else if similar enough
                res.append((seq.ratio(), test))
            pass

    # sort res by similarity in descending order
    res.sort(key=lambda e: e[0], reverse=True)
    return res
    pass


def pre_process_filter(indata: str) -> str:
    """
    clean indata with pattern1 and 2 for pre-processing

    :param indata:  input data
    :return:  cleaned data
    """
    return re.sub(pattern1, repl, re.sub(pattern2, repl, indata))
    pass

# print(re.sub("[+&・_/0-9a-zA-Z!/|\"'#@*~$%^=,-.<>`，。?:;]", "", re.sub("[{(].*[)}]", "", "壞蛋王・老五 (The Bad King Five)")))

