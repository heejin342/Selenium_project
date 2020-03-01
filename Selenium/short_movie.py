from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.ART_Movie_Platform  # 'ART_Movie_Platform'라는 이름의 db를 만듭니다.

# 크롬을 연다. (★chromedriver.exe 의 경로를 제대로 설정해주는 것이 중요함)
driver = webdriver.Chrome('./chromedriver')
# 단편영화 추출할  사이트로 들어간다.
url = 'http://www.kobis.or.kr/kobis/business/mast/mvie/findDiverMovList.do'
driver.get(url)

ART_Movie_ex = {
    'title': '',
    'poster': '',
    'director': '',
    'summary': '',
    'genre_1': '',
    'genre_2': ''
}
# 1-10 = 1page / 11-20 = 2page / 21-30 = 3page / 31-40 = 4page -> 4바퀴 돌아서 range(4)
for k in range(4):
    # 1page에 있는 1-10번 버튼
    for i in range(10):
        # 1번 버튼 안에 있는 12개의 영화
        for j in range(12):
            # 첫번째 영화들어가
            driver.find_element_by_xpath("//*[@id='listArea']/div/ul/li[" + str(j + 1) + "]/div/strong/a").click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            Art_movie_infos = soup.select(
                'body > div.ui-dialog.ui-corner-all.ui-widget.ui-widget-content.ui-front.ui-draggable.ui-resizable')

            for Art_movie_info in Art_movie_infos:
                # 영화 제목 가져오기
                # 36번째 영화 '애천'에서 끝남
                title = '<영화제목>' + '\n' + str(
                    Art_movie_info.select_one(
                        'div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix.ui-draggable-handle > div.hd_layer > div > strong').text)
                print(title + '\n')
                # 영화 포스터 이미지 가져오기
                poster = '<영화포스터>' + '\n' + 'http://www.kobis.or.kr/' + str(
                    Art_movie_info.select_one('img').attrs['src']).replace(
                    '//', '')
                print(poster + '\n')
                # 영화 감독 가져오기
                director_xpath = str(driver.find_element_by_class_name('staffMore').text)
                # 감독 정보가 없을 경우를 위해서 if 구문 사용
                # if not a:  # true print('a is empty!') -> 빈 리스트 체크하기
                # staffMore 목록이 없는 경우 if 구문
                if len(director_xpath) == 0:
                    director = '<감독>' + '\n' + 'NONE'
                    print(director + '\n')
                # staffMore 목록은 있지만, '감독' 정보는 없는 경우
                elif ('독' in director_xpath) == False:
                    director = '<감독>' + '\n' + 'NONE'
                    print(director + '\n')
                # staffMore 목록 안에, '감독' 정보 있는 경우
                else:
                    director = '<감독>' + director_xpath.split('배우')[0].split('만든사람들')[1].split('감독')[
                        1].replace('|', ',')
                    print(director + '\n')

                # if not a:  # true print('a is empty!') -> 빈 리스트 체크하기
                # 줄거리 목록이 아예 없는 경우 if not 구문을 탐.
                if not soup.find('p', class_='desc_info'):
                    summary = '<줄거리>' + '\n' + 'NONE'
                    print(summary + '\n')
                # 줄거리 목록이 있다면, else 구문을 탐.
                else:
                    summary_xpath = str(soup.find('p', class_='desc_info').text).strip()
                    summary = '<줄거리>' + '\n' + summary_xpath
                    print(summary + '\n')

                # 장르 목록이 아예 없는 경우 if not 구문을 탐.
                if not soup.find('dl', class_='ovf cont'):
                    genre_1 = '<장르1>' + '\n' + 'NONE'
                    print(genre_1 + '\n')
                    genre_2 = '<장르2>' + '\n' + 'NONE'
                    print(genre_2 + '\n')
                # 장르 목록이 있으면 else 구문을 탐.
                else:
                    genre_seletor = str(soup.find('dl', class_='ovf cont').text).split('|')[2].replace('\n',
                                                                                                       '').replace(
                        '\t', '').replace(' ', '').split(',')
                    # print(genre_seletor)
                    # print(genre_seletor)
                    # print(len(genre_seletor))
                    genre_1 = '<장르1>' + '\n' + genre_seletor[0]
                    print(genre_1 + '\n')

                    # 장르셀렉터의 2번째 장르가 없다면 len()으로 분리
                    if len(genre_seletor) == 1:
                        genre_2 = '<장르2>' + '\n' + 'NONE'
                        print(genre_2 + '\n')
                    # 장르셀렉터의 Len() 값이 2이상인 경우 else구문을 탐
                    else:
                        genre_2 = '<장르2>' + '\n' + genre_seletor[1]
                        print(genre_2 + '\n')

                ART_Movie_ex = {
                    'title': title,
                    'poster': poster,
                    'director': director,
                    'summary': summary,
                    'genre_1': genre_1,
                    'genre_2': genre_2
                }
                # 첫번쨰 영화 디비에 넣어
                db.ART_movie_list.insert_one(ART_Movie_ex)
                # 뒤로가기
                driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/a[2]/span").click()

        if i == 9:
            if k == 0:
                driver.find_element_by_xpath("//*[@id='pagingForm']/div/a[3]").click()
                driver.find_element_by_xpath("//*[@id='pagingForm']/div/ul/li[" + str(1) + "]/a").click()

            else:
                driver.find_element_by_xpath("//*[@id='pagingForm']/div/a[3]").click()

        else:
            driver.find_element_by_xpath("//*[@id='pagingForm']/div/ul/li[" + str(i + 2) + "]/a").click()
driver.close()
# 마지막에 에러 나는 이유 : 제일 마지막 장에서 지금은, 38번째에서 끝나는데 break를 안 걸어줘서 마지막에 error가 나는 것
