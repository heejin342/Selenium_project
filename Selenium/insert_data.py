from selenium import webdriver
from bs4 import BeautifulSoup

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

driver = webdriver.Chrome('./chromedriver')
# 크롬을 연다. (★chromedriver.exe 의 경로를 제대로 설정해주는 것이 중요함)


driver.get('http://www.kobis.or.kr/kobis/business/stat/boxs/findFormerBoxOfficeList.do')
# 조건을 검색해야하는 사이트를 들어간다.
driver.find_element_by_id("sMultiMovieYn").send_keys("독립·예술영화")
# 조건을 입력해야하는 태그에 대한, ID 값을 찾아서 Send_keys 값으로 입력.
# <button type="button" class="btn_blue" onclick="chkform('search');">조회</button>
driver.find_element_by_class_name("btn_blue").click()
# "조회" 버튼을 클릭한다.

soup = BeautifulSoup(driver.page_source, 'html.parser')

art_movies = soup.select('#content > div.rst_sch > table > tbody> tr')

rank = 1
#  insert 할 데이터 셋트를 만듦
art_movie_data = {
    'rank': rank,
    'movie': '',
    'openday': '',
    'earn_money': '',
    'audience': '',
    'screen_num': '',
    'movie_show_num': ''
}

for art_movie in art_movies:
    print(rank, end=' ' + '위 : ')
    movie = art_movie.select_one('#td_movie').text.strip()
    print(movie)
    openday = '개봉날짜 : ' + str(art_movie.select_one('#td_openDt').text).strip()
    print(openday)
    earn_money = '매출액 : ' + str(art_movie.select_one('#td_salesAcc').text).strip()
    print(earn_money)
    audience = '관객수 : ' + str(art_movie.select_one('#td_audiAcc').text).strip()
    print(audience)
    screen_num = '스크린 수 : ' + str(art_movie.select_one('#td_scrnCnt').text).strip()
    print(screen_num)
    movie_show_num = '상영횟수 : ' + str(art_movie.select_one('#td_showCnt').text).strip()
    print(movie_show_num + '\n')

    art_movie_data = {
        'rank': rank,
        'movie': movie,
        'openday': openday,
        'earn_money': earn_money,
        'audience': audience,
        'screen_num': screen_num,
        'movie_show_num': movie_show_num
    }

    db.art_movie.insert_one(art_movie_data)
    rank += 1