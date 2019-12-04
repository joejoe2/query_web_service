# query_web_service

welcome to query web service

mode 0 is taiwanese

mode 1 is chinese

mode 2 is chinese popular

-------------------------------------------
API
-
/search_singer?singer=...&mode=...

/search_song?song=...&mode=...

/search_singer_and_song?singer=...&song=...&mode=...

will return a json sting in {'status':'not supported'(or 'empty' or 'success'),'content':a json array}

the json array is in [[song name,singer name,url,null],[song name,singer name,url,null],...] and it can be []

notice that an url may be NULL or point to a suffix after https://www.youtube.com/watch?v=
