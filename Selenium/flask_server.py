from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.ART_Movie_Platform  # 'dbsparta'라는 이름의 db를 만듭니다.

app = Flask(__name__)


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/page2')
def page2():
    return render_template('page2.html')


@app.route('/page3')
def page3():
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


# API 역할을 하는 부분
@app.route('/user', methods=['POST'])
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


# 여기서부터 추가
@app.route('/art_user_genre_1', methods=['GET'])
def ART_Movie_listing_genre_1():

    user_info = list(db.userdb.find({}, {'_id': 0}))
    user_genre_1 = (user_info[0]['genre_1'])

    genre_1_moive_infos = list(db.ART_movie_list.find({'genre_1': '<장르1>' + '\n' + user_genre_1}, {'_id': 0}))
    # 포스터 url 키를 추가한후 출력
    for i in genre_1_moive_infos:
        i['poster_url'] = str(i['poster']).split('\n')[1]
    print(genre_1_moive_infos)
    return jsonify({'result': 'success', 'ART_movie_list': genre_1_moive_infos, 'user_genre_1': user_genre_1})


@app.route('/art_user_genre_2', methods=['GET'])
def ART_Movie_listing_genre_2():

    user_info = list(db.userdb.find({}, {'_id': 0}))
    user_genre_2 = (user_info[0]['genre_2'])

    genre_2_movie_infos = list(db.ART_movie_list.find({'genre_2': '<장르2>' + '\n' + user_genre_2}, {'_id': 0}))
    for j in genre_2_movie_infos:
        j['poster_url'] = str(j['poster']).split('\n')[1]
    print(genre_2_movie_infos)

    return jsonify({'result': 'success', 'ART_movie_list': genre_2_movie_infos, 'user_genre_2': user_genre_2})


@app.route('/userbring', methods=['GET'])
def bring():
    user_info = list(db.userdb.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'userdb': user_info})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
