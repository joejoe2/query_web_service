from difflib import SequenceMatcher
import re

# const

# similarity threshold
threshold = 0.3
# filter pattern
pattern1 = "[+&・_/0-9a-zA-Z!/|\"'#@*~$%^=,-.<>`，。?:; ]"
pattern2 = "[[{(].*[)}]"
# to replace irregular char
repl = ""


def compare(template: list, target: str) -> list:
    """
    for error correctness, return a list of strings whose similarity >= threshold to target in template list ,use a SequenceMatcher

    :param template:  a list
    :param target:  a input string
    :return: return a list of strings whose similarity >= threshold to  input in descending order with similarity value
    """
    # use a SequenceMatcher to compare target
    seq = SequenceMatcher(lambda x: x == " ", target)
    # a list of some result
    res = []
    # if similarity >= threshold , add to res
    for item in template:
        # pre process ...
        temp = pre_filter(item)

        # compute similarity
        seq.set_seq2(temp)
        if item.find(target) != -1:  # if exactly contain
            res.append((item, seq.ratio()))
            pass
        elif seq.quick_ratio() >= 0.5:  # else if similar enough
            temps = seq.ratio()
            if temps >= threshold:
                res.append((item, seq.ratio()))
                pass
            pass
        pass

    # sort res by similarity in descending order
    res.sort(key=lambda e: e[1], reverse=True)
    return res
    pass


def pre_filter(indata: str) -> str:
    """
    clean indata with pattern1 and 2 for pre-processing

    :param indata:  str - input data
    :return:  str- data be cleaned
    """
    return re.sub(pattern1, repl, re.sub(pattern2, repl, indata))
    pass

# print(re.sub("[+&・_/0-9a-zA-Z!/|\"'#@*~$%^=,-.<>`，。?:;]", "", re.sub("[{(].*[)}]", "", "壞蛋王・老五 (The Bad King Five)")))

