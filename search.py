import sqlite3
import compare
import packer

# support mode const
TAIWANESE_MODE = 0
CHINESE_MODE = 1
CHINESEPOP_MODE = 2
support_list = [TAIWANESE_MODE, CHINESE_MODE, CHINESEPOP_MODE]

# setup matcher list
conn = sqlite3.connect('taiwanese.db')
c = conn.cursor()
c.execute("select distinct SINGER from TEST")
t_singer = [s[0] for s in c.fetchall()]
print(len(t_singer))
conn.close()
conn = sqlite3.connect('taiwanese.db')
c = conn.cursor()
c.execute("select distinct SONG from TEST")
t_song = [s[0] for s in c.fetchall()]
print(len(t_song))
conn.close()

conn = sqlite3.connect('chinese.db')
c = conn.cursor()
c.execute("select distinct SINGER from TEST")
c_singer = [s[0] for s in c.fetchall()]
print(len(c_singer))
conn.close()
conn = sqlite3.connect('chinese.db')
c = conn.cursor()
c.execute("select distinct SONG from TEST")
c_song = [s[0] for s in c.fetchall()]
print(len(c_song))
conn.close()

conn = sqlite3.connect('chinesepop.db')
c = conn.cursor()
c.execute("select distinct SINGER from TEST")
cp_singer = [s[0] for s in c.fetchall()]
print(len(cp_singer))
conn.close()
conn = sqlite3.connect('chinesepop.db')
c = conn.cursor()
c.execute("select distinct SONG from TEST")
cp_song = [s[0] for s in c.fetchall()]
print(len(cp_song))
conn.close()


def get_list(mode: int) -> tuple:
    """
    return a tuple with singer_list and song_list according to mode

    :param mode: int
    :return:  (list, list)
    """
    if mode == TAIWANESE_MODE:
        return t_singer, t_song
        pass
    elif mode == CHINESE_MODE:
        return c_singer, c_song
        pass
    elif mode == CHINESEPOP_MODE:
        return cp_singer, cp_song
        pass
    pass


def get_db(mode: int) -> str:
    """
    return a db name according to mode

    :param mode: int
    :return: string
    """
    if mode == TAIWANESE_MODE:
        return 'taiwanese.db'
        pass
    elif mode == CHINESE_MODE:
        return 'chinese.db'
        pass
    elif mode == CHINESEPOP_MODE:
        return 'chinesepop.db'
        pass
    pass


def search_singer(singer: str, mode: int) -> str:
    """
    return query result with singer name and mode in json string, the format plz refer to the main page

    :param singer:string
    :param mode:int
    :return:json string
    """
    db = get_db(mode)
    singer_list = get_list(mode)[0]
    cmp = compare.compare(singer_list, singer)
    res = []
    con = sqlite3.connect(db)
    for sin in cmp:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM TEST WHERE SINGER = "'+sin[0]+'"')
        res.extend(cursor.fetchall())
        pass
    con.close()

    if len(res) == 0:
        return packer.pack(packer.EMPTY, res)
    return packer.pack(packer.SUCCESS, res)
    pass
# print(search_singer("伍佰", 0))
# print(compare.compare(t_singer, "伍百"))


def search_song(song: str, mode: int) -> str:
    """
    return query result with song name and mode in json string, the format plz refer to the main page

    :param song:string
    :param mode:int
    :return:json string
    """
    db = get_db(mode)
    song_list = get_list(mode)[1]
    cmp = compare.compare(song_list, song)
    res = []
    con = sqlite3.connect(db)
    for sin in cmp:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM TEST WHERE SONG = "'+sin[0]+'"')
        res.extend(cursor.fetchall())
        pass
    con.close()

    if len(res) == 0:
        return packer.pack(packer.EMPTY, res)
    return packer.pack(packer.SUCCESS, res)
    pass


# print(search_song("思想起", 0)
# print(search_song("???54", TAIWANESE_MODE))