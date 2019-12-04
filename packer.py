import json

# const def for query status
NOT_SUPPORTED = "not supported"
EMPTY = "empty"
SUCCESS = "success"


def pack(status: str, content: list) -> str:
    """
    use to pack the query result and query status into json string, the format plz refer to main page

    :param status:  string
    :param content: query result
    :return:  a json string with status and content
    """
    # init json obj
    obj = {"status": status, "content": []}
    if status == NOT_SUPPORTED:
        # for not supported json obj
        pass
    elif status == EMPTY:
        # for empty json obj
        pass
    elif status == SUCCESS:
        # for non empty query json obj
        obj["content"] = content
        pass
    # return json string
    return json.dumps(obj)
    pass


# print(pack(SUCCESS, [('翁清溪+台灣爵士大樂團', '思想起', 'NULL', None), ('鄭進一', '思想起', 'mJhesIPPUqE', None)]))
