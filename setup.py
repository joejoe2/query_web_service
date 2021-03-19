import sqlite3
import os
import json


def create_songs_db_from_json_file(json_file_name: str, db_name: str) -> None:
    """
build a db by reading all songs info in the json_file with given db_name
    :type json_file_name: str
    :type db_name: str
    :param db_name:
    :param json_file_name:
    """
    with open(json_file_name, encoding="utf8") as reader:
        data = json.load(reader)

    if os.path.exists(db_name):
        raise Exception("param db_name:"+db_name+" already exists in path !")
        pass
    else:
        default_table_name = "TEST"
        create_db(db_name)
        create_songs_table_in_db(db_name, default_table_name)
        insert_songs_data_into_db(db_name, default_table_name, data)
        pass
    pass


def create_db(db_name: str) -> None:
    db_connection = sqlite3.connect(db_name)
    db_connection.commit()
    db_connection.close()
    pass


def create_songs_table_in_db(db_name: str, table_name: str) -> None:
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    db_cursor.execute('CREATE TABLE '+table_name+'(SINGER TEXT NOT NULL,SONG TEXT,URL TEXT NOT NULL,EMOTION CHAR(16));')
    db_cursor.execute('CREATE INDEX index1 ON '+table_name+' (SINGER,SONG);')
    db_connection.commit()
    db_connection.close()
    pass


def insert_songs_data_into_db(db_name: str, table_name: str, songs_data: object) -> None:
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    for song_info in songs_data:
        song_info["name"] = song_info["name"].replace('"', "")
        song_info["singer"] = song_info["singer"].replace('"', "")
        db_cursor.execute('INSERT INTO '+table_name+' VALUES ("' + str(song_info["singer"]) + '","' + str(song_info["name"]) + '","' + str(
            song_info["songID"]) + '",NULL);')
        pass
    db_connection.commit()
    db_connection.close()
    pass


if __name__ == '__main__':
    json_files = ["songWithID_Taiwanese.json", "songWithID_Chinese.json", "songWithID_Chinese_popular.json"]
    db_names = ["taiwanese.db", "chinese.db", "chinesepop.db"]
    for file, db in list(zip(json_files, db_names)):
        try:
            create_songs_db_from_json_file(file, db)
            print("successfully created "+db+" !")
        except Exception as ex:
            print(ex)
            pass
        pass
    pass
