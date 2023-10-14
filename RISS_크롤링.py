from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.alert import Alert
import string
import re
import os

# 키워드 입력받기
date = input('시작날짜를 입력해주세요.')
keyword = '창의성'
code = quote(keyword)
url = 'http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery='+code+'%EC%B0%BD%EC%9D%98%EC%84%B1''&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=DATE&p_year1=&p_year2=&iStartCount=0&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&l_sub_code=&fsearchMethod=&sflag=1&isFDetailSearch=N&pageNumber=1&resultKeyword='+code+'%EC%B0%BD%EC%9D%98%EC%84%B1''&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale=100&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query='+code

# 수치 가져오기
browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(10)
elem = browser.find_element(By.TAG_NAME,'dd')
elem_num = elem.find_element(By.CLASS_NAME,'num')
num = elem_num.text.replace(',','') #총개수 100 미만 vs 초과
print(num,'개의 논문 크롤링을 시작합니다.')

반복횟수 = int(num)//100 +1

for i in range(반복횟수):
    startcount = str(i * 100)

    if i >= 1 :
        url = 'http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=&strQuery='+code+'%EC%B0%BD%EC%9D%98%EC%84%B1''&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=DATE&p_year1=&p_year2=&iStartCount='+startcount+'&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&l_sub_code=&fsearchMethod=search&sflag=1&isFDetailSearch=N&pageNumber=1&resultKeyword='+code+'%EC%B0%BD%EC%9D%98%EC%84%B1''&fsearchSort=&fsearchOrder=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&colName=re_a_kor&pageScale=100&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKeyword=&relationKeyword=&query='+code
    
    #sub_url 가져오기
    target = request.urlopen(url)
    soup = BeautifulSoup(target,'html.parser')
    listOfsoup = soup.find_all('ul')
    with open(keyword+'html.txt', 'w', encoding = 'UTF-8') as outfile: #페이지 정보
        outfile.write(str(listOfsoup[79]))
    with open(keyword+'html.txt', 'r', encoding = 'UTF-8') as infile: #페이지 정보
        line = infile.readline()
        while line != '':
            line = line.rstrip('\n')
            line = line.strip('\t')
            line = line.strip()
            if '<p class="title"><a href="' in line:
                line = line.replace('<p class="title"><a href="','') #이게 최선?은 아닌 것 같아 애초에 크롤링부터 생각을 해보면 이게 필요가 없다. 근데 그게 가능?
                line = line.replace(line[line.index('">'):],'')
                with open(keyword+date+'targeturl.txt','a', encoding='UTF-8') as urla:
                    urla.write('http://www.riss.kr'+line+code+'\n')
            line = infile.readline()
    print(startcount,'개 url저장 완료')

with open(keyword+date+'targeturl.txt','r', encoding='UTF-8') as urlr:
    print('targetrul.txt의 길이=',len(urlr.readlines()),'개 url 크롤링성공!!! 목표 수 =',num)


print('각 논문 크롤링을 시작합니다')
with open(keyword+date+'targeturl.txt','r', encoding='UTF-8') as urlr: #각 논문 크롤링
    line = urlr.readline()
    cnt = 0
    while line !='':
        line = line.rstrip('\n')
        result = []
        cnt = cnt +1
        에러 = True
        delay_time = 0
        browser.get(line)
        try:
            da = Alert(browser)
            da.accept()
        except:#정상작동
            while 에러:
                browser.implicitly_wait(5)
                page_test = browser.find_element(By.TAG_NAME,'div')
                with open(keyword+'test_page.txt','w', encoding='UTF-8') as wtp:
                    wtp.write(page_test.text)
                    wtp.write('delaytime :'+str(delay_time))
                with open(keyword+'test_page.txt','r', encoding='UTF-8') as rtp:
                    testline = rtp.readline()
                if '서비스 이용에 불편을 드려 죄송합니다.' in testline:
                    browser.refresh()
                    delay_time = delay_time + 0.5
                    time.sleep(delay_time)
                else: 
                    에러 = 0
                if delay_time > 2:
                    delay_time = 0
                    browser.close()
                    print('창을 닫았습니다.')
                    browser = webdriver.Chrome()
                    print('창을 다시 엽니다.')
                    browser.get(line)

            elem = WebDriverWait(browser,60).until(EC.presence_of_element_located((By.ID,'thesisInfoDiv')))
            with open(keyword+'elem.txt','w', encoding='UTF-8') as outfile:
                outfile.write(elem.text)
            with open(keyword+'elem.txt','r', encoding='UTF-8') as infile:
                dataList = list(infile.readlines())

            #Title
            title = dataList[0]
            영어제목 = ''
            한국어제목 = ''
            if '=' in title:

                title = title.split("=")
                new_title_0 = re.sub(r"[^\uAC00-\uD7A30]", "", title[0])
                new_title_1 = re.sub(r"[^\uAC00-\uD7A30]", "", title[1])

                if new_title_0 == '':
                    영어제목 = title[0]
                else:
                    한국어제목 = title[0]
                if new_title_1 == '':
                    영어제목 = 영어제목 + title[1]
                else:
                    한국어제목 = 한국어제목 + title[1]
            else:
                new_title = re.sub(r"[^\uAC00-\uD7A30]", "", title) 
                if new_title == '': #영어다
                    영어제목 = title
                else:
                    한국어제목 = title
            result.append(한국어제목.rstrip('\n').replace(',','/').strip())
            result.append(영어제목.rstrip('\n').replace(',','').strip())

            if result[0] == '': result[0] = '한국어제목이 없습니다.'
            if result[1] == '': result[1] = '영어제목이 없습니다.'

            for index in range(1,len(dataList)):
                if dataList[index] == '저자\n' :
                    result.append(dataList[index+1].replace(' ','').rstrip('\n').replace(',',''))
                elif dataList[index] == '발행기관\n':
                    result.append(dataList[index+1].rstrip('\n').replace(',',''))
                elif dataList[index] == '학술지명\n':
                    result.append(dataList[index+1].replace(' ','').rstrip('\n').replace(',',''))
                elif dataList[index] == '권호사항\n':
                    result.append(dataList[index+1].rstrip('\n').replace(',',''))
                elif dataList[index] == '발행연도\n':
                    result.append(dataList[index+1].rstrip('\n').replace(',',''))
                elif dataList[index] == '작성언어\n':
                    result.append(dataList[index+1].rstrip('\n').replace(',',''))
                elif dataList[index] == '주제어\n':
                    result.append(dataList[index+1].replace(' ','').rstrip('\n').replace(',',''))
                    
                    break

        else: #알림창발생으로인한 오작동 방지 알림창 발생시에도 한 줄을 채운다.
            result = '논문 알림창발생 크롤링 불가능!!'
            with open(keyword+date+'.txt','a',encoding='UTF-8') as final:
                final.write(result+'\n')
                break
        
        with open(keyword+date+'.txt','a',encoding='UTF-8') as final:
            final.write(','.join(result)+'\n')   
        line = urlr.readline()

print('프로그램 종료')