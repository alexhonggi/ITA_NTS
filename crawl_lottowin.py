# 셀레니움 웹 드라이버 임포트 해 주기
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Chrome 브라우저 열기
browser = webdriver.Chrome()

# 구글 페이지 연결시키기
url = "https://dhlottery.co.kr/gameResult.do?method=byWin"

#go to board
try:
    browser.get(url)
  
except:
    print("ERROR while entering webpage")
    
#Lotto 당첨번호 가져오기
#1등 당첨번호
num_win = browser.find_element(By.CLASS_NAME, 'num.win')
first_nums = num_win.find_elements(By.CLASS_NAME, 'ball_645')

#보너스 번호
num_bonus = browser.find_element(By.CLASS_NAME, 'num.bonus')
bonus_num = num_bonus.find_element(By.CLASS_NAME, 'ball_645')

# 당첨번호 출력
print('1등 당첨번호:')
for num in first_nums:
    print(num.text)
    
print('보너스 번호')
print(bonus_num.text)

time.sleep(10)
browser.quit()