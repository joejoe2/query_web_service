from flask import Flask, request
import os
import search
import packer

# setup flask
app = Flask(__name__)
port = int(os.environ.get("PORT", 8080))



def support(mode):
    """
    check is the mode is supported

    :param mode:  int
    :return:  support or not
    """
    if mode not in search.support_list:
        return False
        pass
    return True
    pass


@app.route("/")
def index():
    """
    main page, showing api explanations

    :return:  index html
    """
    return "welcome to query web service<br>" \
           "mode 0 is taiwanese<br>" \
           "mode 1 is chinese<br>" \
           "mode 2 is chinese popular<br>" \
           "-----------------------------------------<br>" \
           "/search_singer?singer=...&mode=...<br>" \
           "/search_song?song=...&mode=...<br>" \
           "/search_singer_and_song?singer=...&song=...&mode=...<br>" \
           "will return a json sting in {'status':'not supported'(or 'empty' or 'success'),'content':a json array}<br>" \
           "the json array is in [[song name,singer name,url,null],[song name,singer name,url,null],...] and it can be []<br>" \
           "notice that an url may be NULL or point to a suffix after https://www.youtube.com/watch?v="


@app.route("/search_singer", methods=['GET'])
def search_singer():
    """
    search with singer name

    :return:  json string
    """

    # get param
    singer = request.args.get("singer").strip()
    mode = int(request.args.get("mode").strip())
    if not support(mode) or singer == "":
        # return not supported
        return packer.pack(packer.NOT_SUPPORTED, None)
        pass
    else:
        # return query result
        return search.search_singer(singer, mode)
    pass


@app.route("/search_song", methods=['GET'])
def search_song():
    """
    search with song name

    :return:  json string
    """
    # get param
    song = request.args.get("song").strip()
    mode = int(request.args.get("mode").strip())
    if not support(mode) or song == "":
        # return not supported
        return packer.pack(packer.NOT_SUPPORTED, None)
        pass
    else:
        # return query result
        return search.search_song(song, mode)
    pass


@app.route("/search_singer_and_song", methods=['GET'])
def search_singer_and_song():
    """
    search with singer and song name

    :return:  json string
    """
    singer = request.args.get("singer").strip()
    song = request.args.get("song").strip()
    mode = int(request.args.get("mode").strip())
    if not support(mode) or singer == "" or song == "":
        # return not supported
        return packer.pack(packer.NOT_SUPPORTED, None)
        pass
    else:
        # return query result
        return search.search_singer_song(singer, song, mode)
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)
