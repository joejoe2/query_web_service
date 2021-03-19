# query_web_service

welcome to query web service, this is service for serching chinese and taiwanese songs by name of singer or song using sqlite and support missing some part of query key word by comparing the word 's distance

mode 0 is taiwanese

mode 1 is chinese

mode 2 is chinese popular

-------------------------------------------
API
-

via http get

/search_singer?singer=...&mode=...

/search_song?song=...&mode=...

/search_singer_and_song?singer=...&song=...&mode=...

will return a json sting in {'status':'not supported'(or 'empty' or 'success'),'content':a json array}

the json array is in [[song name,singer name,url,null],[song name,singer name,url,null],...] and it can be []

notice that an url may be NULL or point to a suffix after https://www.youtube.com/watch?v=

ex1. api usage 

/search_singer?singer=五月天&mode=1

ex2. api output for normal query

{

"status": "success", "content": 

[["\u4e5d\u5929", "\u4e00\u8d77\u8e66\u8e82", "NULL", null], 

["\u4e5d\u5929", "\u5225\u8aaa\u8a71\u543b\u6211", "jG0NFoFqUOo", null]]

}

ex3. api output for not supported mode like /search_singer?singer=五月天&mode=4

{

"status": "not supported", "content": []

}

ex4. api output for not found any result 

{

"status": "empty", "content": []

}