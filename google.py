# 구글 이미지 크롤링 코드
from urllib.request import Request, urlopen
import ssl

# 새로운 링크와 변수에 대한 요청 및 응답 처리
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

req = Request('https://www.google.co.kr/imghp?hl=ko&ogbl', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req, context=context).read()

# 웹 드라이버 자동 조작
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
elem = driver.find_element(By.NAME , 'q')
elem.send_keys("")
elem.send_keys(Keys.RETURN)

time.sleep(3)

images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
count = 1
for image in images:
    image.click()
    time.sleep(5)
    imgUrl = driver.find_element(By.CSS_SELECTOR, ".sFlh5c.pT0Scc").get_attribute("src")
    
    req_img = Request(imgUrl, headers={'User-Agent': 'Mozilla/5.0'})
    img_data = urlopen(req_img, context=context).read()  # 새로운 링크로 이미지 다운로드
    
    with open(str(count) + ".jpg", "wb") as f:
        f.write(img_data)
    count += 1
