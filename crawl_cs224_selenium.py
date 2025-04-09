# 셀레니움 웹 드라이버 임포트 해 주기
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Chrome 브라우저 열기
browser = webdriver.Chrome()

# 구글 페이지 연결시키기
web_url = "http://web.stanford.edu/class/cs224n/"

#go to board
try:
    browser.get(web_url)
  
except:
    print("ERROR while entering webpage")
    

element = browser.find_element(By.ID, 'schedule')
elements = element.find_elements(By.TAG_NAME, 'a')

# To get all pdf links
pdf_links = []
for elem in elements:
    if 'slides' in elem.text:
        if 'pdf' in elem.get_attribute('href') and 'pptx' not in elem.get_attribute('href'):
            pdf_links.append(elem.get_attribute('href'))
    
time.sleep(2)
browser.quit()

for pdf_link in pdf_links:
    print(pdf_link)


# To open pdf links and save the file (.pdf)
import wget

num_links = len(pdf_links)
idx = 1

print('DOWNLAOD THE PDF FILES IN {}'.format(web_url))

for file_link in pdf_links:
    #file_url = web_url + file_link
    file_url = file_link
    filepath = file_link.split('/')[1]
    
    print()
    print('[{}/{}] DOWNLOAD START: \'{}\''.format(idx, num_links, filepath))
    wget.download(file_url, filepath)
    
    idx += 1
    
print()
print()
print('DOWNLAOD completed !')