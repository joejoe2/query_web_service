import sqlite3
import os
import json

# setup db
jf = None
with open('songWithID_Taiwanese.json', encoding="utf8") as reader:
    jf = json.load(reader)
if not os.path.exists("taiwanese.db"):
    conn = sqlite3.connect('taiwanese.db')
    c = conn.cursor()
    c.execute('CREATE TABLE TEST(SINGER TEXT NOT NULL,SONG TEXT,URL TEXT NOT NULL,EMOTION CHAR(16));')
    c.execute('CREATE INDEX index1 ON TEST (SINGER,SONG);')
    conn.commit()
    for p in jf:
        p["name"] = p["name"].replace('"', "")
        p["singer"] = p["singer"].replace('"', "")
        print(p["singer"])
        c.execute('INSERT INTO TEST VALUES ("' + str(p["singer"]) + '","' + str(p["name"]) + '","' + str(p["songID"]) + '",NULL);')
        pass
    conn.commit()
    conn.close()
    pass

jf = None
with open('songWithID_Chinese.json', encoding="utf8") as reader:
    jf = json.load(reader)
if not os.path.exists("chinese.db"):
    conn = sqlite3.connect('chinese.db')
    c = conn.cursor()
    c.execute('CREATE TABLE TEST(SINGER TEXT NOT NULL,SONG TEXT,URL TEXT NOT NULL,EMOTION CHAR(16));')
    c.execute('CREATE INDEX index1 ON TEST (SINGER,SONG);')
    conn.commit()
    for p in jf:
        p["name"] = p["name"].replace('"', "")
        p["singer"] = p["singer"].replace('"', "")
        print(p["singer"])
        c.execute('INSERT INTO TEST VALUES ("' + str(p["singer"]) + '","' + str(p["name"]) + '","' + str(p["songID"]) + '",NULL);')
        pass
    conn.commit()
    conn.close()
    pass

jf = None
with open('songWithID_Chinese_popular.json', encoding="utf8") as reader:
    jf = json.load(reader)
if not os.path.exists("chinesepop.db"):
    conn = sqlite3.connect('chinesepop.db')
    c = conn.cursor()
    c.execute('CREATE TABLE TEST(SINGER TEXT NOT NULL,SONG TEXT,URL TEXT NOT NULL,EMOTION CHAR(16));')
    c.execute('CREATE INDEX index1 ON TEST (SINGER,SONG);')
    conn.commit()
    for p in jf:
        p["name"] = p["name"].replace('"', "")
        p["singer"] = p["singer"].replace('"', "")
        print(p["singer"])
        c.execute('INSERT INTO TEST VALUES ("' + str(p["singer"]) + '","' + str(p["name"]) + '","' + str(p["songID"]) + '",NULL);')
        pass
    conn.commit()
    conn.close()
    pass
