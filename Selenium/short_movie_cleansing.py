from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.ART_Movie_Platform  # 'ART_Movie_Platform'라는 이름의 db를 만듭니다.

db.ART_movie_list.update_many({'genre_1': '<장르1>' + '\n' + '공포(호러)'}, {'$set': {'genre_1': '<장르1>' + '\n' + '공포'}})

db.ART_movie_list.update_many({'genre_2': '<장르2>' + '\n' + '공포(호러)'}, {'$set': {'genre_2': '<장르2>' + '\n' + '공포'}})

db.ART_movie_list.update_many({'genre_1': '<장르1>' + '\n' + '멜로/애정/로맨스'}, {'$set': {'genre_1': '<장르1>' + '\n' + '멜로/로맨스'}})

db.ART_movie_list.update_many({'genre_2': '<장르2>' + '\n' + '멜로/애정/로맨스'}, {'$set': {'genre_2': '<장르2>' + '\n' + '멜로/로맨스'}})
