from urllib import request
from bs4 import BeautifulSoup
import webbrowser

page = 1
count = 0
while True:
    url_list = []
    target = request.urlopen('http://www.inu.ac.kr/user/boardList.do?boardId=48510&page=' + str(page) + '&id=mobile_060200000000')
    soup = BeautifulSoup(target, 'html.parser')
    listOfsoup = soup.find_all('ul')    
