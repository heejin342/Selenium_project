from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.Short_Movie_Platform  # 'Short_Movie_Platform'라는 이름의 db를 만듭니다.

# 크롬을 연다. (★chromedriver.exe 의 경로를 제대로 설정해주는 것이 중요함)
driver = webdriver.Chrome('./chromedriver')
# 단편영화 추출할  사이트로 들어간다.
url = 'https://www.koreafilm.or.kr/library/search/type?keyTypeCode=01'
driver.get(url)

# 독립영화 카테고리 누르기
driver.find_element_by_xpath("//*[@id='frmSearch']/ul/li[4]/a").click()
# DB에 저장할 데이터 형식
ART_Movie_list = {
    'title': '',
    'poster': '',
    'director': '',
    'actor': '',
    'summary': '',
    'main_genre': '',
    'second_genre': ''
}
# 첫번째 영화 누르기
driver.find_element_by_xpath("//*[@id='contents']/div[4]/div/table/tbody/tr[2]/td[1]/a/span[2]").click()

soup = BeautifulSoup(driver.page_source, 'html.parser')
# 영화 정보들이 있는 제일 큰 셀렉터
a = soup.select_one('#contents>div:nth-child(5) > p > span')
Art_movies = soup.select('#contents')
cnt = str(a.text).strip()
cnt = cnt.split(' ')[1].split('편')[0]

for Art_movie in Art_movies:

    # moive가 몇개있는지 항목인지 확인해야함
    cnt = int(cnt) + 1

    while cnt > 1:
        title = str(
            Art_movie.select_one(
                'div:nth-child(5) >div:nth-child(' + str(cnt) + ') > table > tbody > tr > td > div').text).strip()
        a = title.split('K')[0].strip()
        title = '<영화제목>\n' + a
        print(title + '\n')

        poster = str(
            Art_movie.select_one('div.box-libraryDetail-2 > div.inner-left > p.img-1 > span'))
        b = poster.split('(')[1].split(')')[0]
        poster = '<포스터>\n' + b
        print(poster + '\n')

        director = '<감독>' + '\n' + str(
            Art_movie.select_one(
                'div:nth-child(5) > div:nth-child( ' + str(
                    cnt) + ') > table > tbody > tr:nth-child(5) > td').text).strip()
        print(director + '\n')

        actor_selecter = "div:nth-child(5) > div:nth-child(" + str(cnt) + ") > table > tbody > tr:nth-child(2) > td"
        actor_list = (Art_movie.select_one(actor_selecter)).text.split()
        if ','.join(actor_list) is not None:
            actor = '<출연>' + '\n' + ','.join(actor_list)
        else:
            actor = 'NONE'
        print(actor + '\n')

        summary = '<줄거리>' + '\n' + str(
            Art_movie.select_one(
                'div:nth-child(5) > div:nth-child(' + str(
                    cnt) + ') > table > tbody > tr:nth-child(10) > td').text).strip()
        print(summary + '\n')

        main_genre = str(
            Art_movie.select_one(
                'div:nth-child(5) > div:nth-child(' + str(
                    cnt) + ') > table > tbody > tr:nth-child(9) > td').text).strip()
        tmp_main_genre = main_genre.split(',')[0]
        print('<1장르>\n' + tmp_main_genre + '\n')

        # 컴마가 없다면 == 장르가 한개라면
        if main_genre.find(',') == -1:
            second_genre = '<2장르>' + '\n' + 'NONE'
            print(second_genre + '\n')

        else:
            # print(main_genre.split(',')[1])
            second_genre = '<2장르>' + '\n' + main_genre.split(',')[1]
            print(second_genre)

        cnt = int(cnt) - 1
        print('//////////////////////')

        ART_Movie_list = {
            'title': title,
            'poster': poster,
            'director': director,
            'actor': actor,
            # 'summary': summary,
            'main_genre': main_genre,
            'second_genre': second_genre
        }
        # Art_Movie 라는 것으로 저장
        db.Art_Movie.insert_one(ART_Movie_list)

    driver.back()

driver.close()
