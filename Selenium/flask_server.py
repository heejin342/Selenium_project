from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from selenium import webdriver
from bs4 import BeautifulSoup

import random

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.ART_Movie_Platform  # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


# 영화 추천 함수
def recommend_movie_db():
    db.genre1_art_movie.drop()
    db.genre2_art_movie.drop()

    all_short_movie = list(db.ART_movie_list.find({}))

    customer_genre1 = '스릴러'
    customer_genre2 = '코미디'

    temp_main_genre_movie = []
    temp_second_genre_movie = []

    for k in range(len(all_short_movie)):
        # 단편영화 장르 값 입시로 저장해두기
        temp_genre1 = all_short_movie[k].get('genre_1').split('\n')[1]
        temp_genre2 = all_short_movie[k].get('genre_2').split('\n')[1]
        # print(all_short_movie[k].get('genre_1').split('\n')[1])
        # print(all_short_movie[k].get('genre_2').split('\n')[1])
        # 만약에 고객 메인 장르와 단편영화의 임시장르가 같으면,
        if customer_genre1 == temp_genre1 or customer_genre1 == temp_genre2:
            # 그 영화들을 하나의 리스트로 모아둔다.
            temp_main_genre_movie.append(all_short_movie[k])
        # 만약에 고객 서브 장르와 단편영화의 임시장르가 같으면,
        if customer_genre2 == temp_genre1 or customer_genre2 == temp_genre2:
            temp_second_genre_movie.append(all_short_movie[k])
        else:
            continue

    print(temp_main_genre_movie)
    print(temp_second_genre_movie)

    customer_genre1_movie = random.sample(temp_main_genre_movie, 3)
    customer_genre2_movie = random.sample(temp_second_genre_movie, 3)

    print("첫번째 선호하는 장르영화는", customer_genre1)
    for i in range(len(customer_genre1_movie)):
        movie_title = customer_genre1_movie[i].get('title').split('\n')[1]
        movie_poster = customer_genre1_movie[i].get('poster').split('\n')[1]
        movie_director = customer_genre1_movie[i].get('director').split('\n')[1]
        movie_summary = customer_genre1_movie[i].get('summary').split('\n')[1]
        print(movie_title, movie_poster, movie_director, movie_summary)

        # 영화 데이터
        genre1_movie = {
            'title': movie_title,
            'poster': movie_poster,
            'director': movie_director,
            'summary': movie_summary,
        }
        # 영화정보저장
        db.genre1_art_movie.insert_one(genre1_movie)

    print("두번째 선호하는 장르영화는", customer_genre2)
    for i in range(len(customer_genre2_movie)):
        movie_title = customer_genre2_movie[i].get('title').split('\n')[1]
        movie_poster = customer_genre2_movie[i].get('poster').split('\n')[1]
        movie_director = customer_genre2_movie[i].get('director').split('\n')[1]
        movie_summary = customer_genre2_movie[i].get('summary').split('\n')[1]
        print(movie_title, movie_poster, movie_director, movie_summary)

        # 영화 데이터
        genre2_movie = {
            'title': movie_title,
            'poster': movie_poster,
            'director': movie_director,
            'summary': movie_summary,
        }
        # 영화정보저장
        db.genre2_art_movie.insert_one(genre2_movie)


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/page3')
def page3():
    recommend_movie_db()
    return render_template('page3.html')


@app.route('/page4')
def page4():
    return render_template('page4.html')


@app.route('/user', methods=['GET'])
def listing():
    result = list(db.Long_movie_list.find({}, {'_id': 0}))
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result': 'success', 'Long_movie_list': result})


@app.route('/main', methods=['GET'])
def listing2():
    result = list(db.ART_movie_list.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'ART_movie_list': result})


@app.route('/customer', methods=['GET'])
def user_listing():
    result = list(db.userdb.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'userdb': result})


@app.route('/customer', methods=['POST'])
def saving():
    email = request.form['email']
    pwd = request.form['pwd']
    genre_1 = request.form['genre_1']
    genre_2 = request.form['genre_2']

    data = {
        'email': email,
        'pwd': pwd,
        'genre_1': genre_1,
        'genre_2': genre_2
    }

    db.userdb.insert_one(data)
    return jsonify({'result': 'success'})


@app.route('/userupdate', methods=['POST'])
def update():
    genre_1 = request.form['genre_1']
    genre_2 = request.form['genre_2']

    db.userdb.update_one({'genre_1': ''}, {'$set': {'genre_1': genre_1}})
    db.userdb.update_one({'genre_2': ''}, {'$set': {'genre_2': genre_2}})

    return jsonify({'result': 'success'})


@app.route('/genre1_movie', methods=['GET'])
def recommend():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.genre1_art_movie.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'movies': result})


@app.route('/genre2_movie', methods=['GET'])
def recommend2():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.genre2_art_movie.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'movies': result})


@app.route('/userbring', methods=['GET'])
def bring():
    user_info = list(db.userdb.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'userdb': user_info})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
