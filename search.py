import sqlite3
import compare
import response

# support mode const
TAIWANESE_MODE = 0
CHINESE_MODE = 1
CHINESE_POPULAR_MODE = 2
# support list
supported_modes = [TAIWANESE_MODE, CHINESE_MODE, CHINESE_POPULAR_MODE]
# matcher list
taiwanese_singers = []
taiwanese_songs = []
chinese_singers = []
chinese_songs = []
chinese_popular_singers = []
chinese_popular_songs = []


def is_support(mode: int) -> bool:
    """
    check is the mode is supported

    :param mode:  int
    :return: support or not
    """
    return mode in supported_modes
    pass


def do_on_first_import():
    # setup matcher list
    conn = sqlite3.connect('taiwanese.db')
    c = conn.cursor()
    c.execute("select distinct SINGER from TEST")
    taiwanese_singers.extend([s[0] for s in c.fetchall()])
    conn.close()
    conn = sqlite3.connect('taiwanese.db')
    c = conn.cursor()
    c.execute("select distinct SONG from TEST")
    taiwanese_songs.extend([s[0] for s in c.fetchall()])
    conn.close()

    conn = sqlite3.connect('chinese.db')
    c = conn.cursor()
    c.execute("select distinct SINGER from TEST")
    chinese_singers.extend([s[0] for s in c.fetchall()])
    conn.close()
    conn = sqlite3.connect('chinese.db')
    c = conn.cursor()
    c.execute("select distinct SONG from TEST")
    chinese_songs.extend([s[0] for s in c.fetchall()])
    conn.close()

    conn = sqlite3.connect('chinesepop.db')
    c = conn.cursor()
    c.execute("select distinct SINGER from TEST")
    chinese_popular_singers.extend([s[0] for s in c.fetchall()])
    conn.close()
    conn = sqlite3.connect('chinesepop.db')
    c = conn.cursor()
    c.execute("select distinct SONG from TEST")
    chinese_popular_songs.extend([s[0] for s in c.fetchall()])
    conn.close()
    pass


def get_singers_and_songs_by_mode(mode: int) -> tuple:
    """
    return a tuple with (singer_list , song_list) according to mode

    :param mode: int
    :return:  (list, list)
    """
    if mode == TAIWANESE_MODE:
        return taiwanese_singers, taiwanese_songs
        pass
    elif mode == CHINESE_MODE:
        return chinese_singers, chinese_songs
        pass
    elif mode == CHINESE_POPULAR_MODE:
        return chinese_popular_singers, chinese_popular_songs
        pass
    else:
        raise Exception("invalid mode")
    pass


def get_db_name_by_mode(mode: int) -> str:
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
    elif mode == CHINESE_POPULAR_MODE:
        return 'chinesepop.db'
        pass
    else:
        raise Exception("invalid mode")
    pass


def get_acceleration_flag(mode: int, is_song: bool) -> bool:
    if mode == CHINESE_MODE and is_song:
        return True
    return False
    pass


def search_with_singer(singer_name: str, mode: int) -> str:
    """
    return query result with singer name and mode in json string, the format plz refer to the main page

    :param singer_name:
    :param mode:
    :return:json string
    """
    SINGER_NAME = 1
    db = get_db_name_by_mode(mode)
    singer_list = get_singers_and_songs_by_mode(mode)[0]
    similar_singers = compare.compare(singer_list, singer_name)
    res = []
    db_connection = sqlite3.connect(db)
    for singer_with_similar_score in similar_singers:
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT * FROM TEST WHERE SINGER = "' + singer_with_similar_score[SINGER_NAME] + '"')
        res.extend(db_cursor.fetchall())
        pass
    db_connection.close()

    if len(res) == 0:
        return response.pack(response.EMPTY, res)
    else:
        return response.pack(response.SUCCESS, res)
    pass


def search_with_song(song_name: str, mode: int) -> str:
    """
    return query result with song name and mode in json string, the format plz refer to the main page

    :param song_name:
    :param mode:
    :return:json string
    """
    SONG_NAME = 1
    db = get_db_name_by_mode(mode)
    song_list = get_singers_and_songs_by_mode(mode)[1]
    res = []
    songs_data = []

    db_connection = sqlite3.connect(db)
    if get_acceleration_flag(mode, True):
        for letter in song_name:
            db_cursor = db_connection.cursor()
            db_cursor.execute('SELECT * FROM TEST WHERE SONG LIKE "%' + letter + '%"')
            songs_data.extend([song for song in db_cursor.fetchall()])
            pass
        songs_data = list(dict.fromkeys(songs_data))
        similar_songs = [song[SONG_NAME] for song in songs_data]
        similar_songs = compare.compare(similar_songs, song_name, ac=True)
        for song_with_similar_score in similar_songs:  # pick the song in similar_songs from in songs_data
            for song_info in songs_data:
                if song_with_similar_score[SONG_NAME] == song_info[SONG_NAME]:
                    res.append(song_info)
                    break
        pass
    else:
        similar_songs = compare.compare(song_list, song_name)
        for song_with_similar_score in similar_songs:
            db_cursor = db_connection.cursor()
            db_cursor.execute('SELECT * FROM TEST WHERE SONG = "' + song_with_similar_score[SONG_NAME] + '"')
            res.extend(db_cursor.fetchall())
            pass
        pass
    db_connection.close()

    if len(res) == 0:
        return response.pack(response.EMPTY, res)
    else:
        return response.pack(response.SUCCESS, res)
    pass


def search_with_singer_and_song(singer_name: str, song_name: str, mode: int) -> str:
    """
    return query result with singer and song name and mode in json string, the format plz refer to the main page

    :param singer_name: string
    :param song_name:  string
    :param mode:  int
    """
    SINGER_NAME = 1
    SONG_NAME = 1
    db = get_db_name_by_mode(mode)
    singer_list, song_list = get_singers_and_songs_by_mode(mode)
    similar_singers = compare.compare(singer_list, singer_name)
    similar_songs = compare.compare(song_list, song_name, get_acceleration_flag(mode, True))
    res1 = []
    res2 = []

    db_connection = sqlite3.connect(db)
    for singer_with_similar_score in similar_songs:
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT * FROM TEST WHERE SONG = "'+singer_with_similar_score[SONG_NAME]+'"')
        res1.extend(db_cursor.fetchall())
        pass
    for singer_with_similar_score in similar_singers:
        db_cursor = db_connection.cursor()
        db_cursor.execute('SELECT * FROM TEST WHERE SINGER = "' + singer_with_similar_score[SINGER_NAME] + '"')
        res2.extend(db_cursor.fetchall())
        pass
    db_connection.close()

    res = [x for x in res1 if x in res1 and x in res2]

    if len(res) == 0:
        return response.pack(response.EMPTY, res)
    return response.pack(response.SUCCESS, res)
    pass


if __name__ == '__main__':
    do_on_first_import()
    # print(search_with_singer("五月天", 1))
    pass
else:
    do_on_first_import()
    pass
