from bs4 import BeautifulSoup, SoupStrainer
import cchardet
import lxml
import requests
import re
from selenium import webdriver
from tqdm import tqdm
import time


'''
cchardet, lxml 都是可以加速 bs4 的套件
要先 pip3 install cchardet lxml

webdriver 需要下載 chromedriver
dowload link: https://chromedriver.chromium.org/downloads

refe:
https://iter01.com/568912.html
https://www.browserstack.com/guide/download-file-using-selenium-python
https://ithelp.ithome.com.tw/articles/10196817
https://stackoverflow.com/questions/38459972/rename-downloaded-files-selenium
https://www.learncodewithmike.com/2020/11/multithreading-with-python-web-scraping.html
https://thehftguy.com/2020/07/28/making-beautifulsoup-parsing-10-times-faster/
https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id65
'''



page_url_list = []
doc_list = []
webdriver_path = '/Users/nerohin/Downloads/chromedriver' # chromedriver 路徑
requests_session = requests.Session()

# 把所有公告頁面的連結都抓下來
def get_announce_page(start_page: int, end_page: int):

    base_url = 'https://www.csie.ncku.edu.tw/ncku_csie/announce/news/1000'
    urls = [f'{base_url}?Infolist_page={page}' for page in range(start_page, end_page)]  # 1~100頁的網址清單，100 頁是到 2020-08-17
    
    for url in tqdm(urls):

        web = requests_session.get(url)
        web.encoding = 'utf-8' # 設定編碼
        soup = BeautifulSoup(web.text, 'lxml')       
    
        # get /ncku_csie/announce/view/ page
        for link in soup.find_all('a'):
            if link.get('href') is not None: # 有連結
                if re.match(r'/ncku_csie/announce/view/\d+', link.get('href')): # 有 /ncku_csie/announce/view/ 的連結
                    page_url_list.append('https://www.csie.ncku.edu.tw' + link.get('href')) # 把連結加到 page_url_list

# 把公告裡有 Download 的連結都抓下來
def get_doc_url(list: list):
  
    for page in list:
        web = requests_session.get(page)
        web.encoding = 'utf-8' # 設定編碼
        page_soup = BeautifulSoup(web.text, 'lxml', parse_only=SoupStrainer(class_="odd")) # 目前檔案下載都會在 odd class 裡面
        title = page_soup.find('td').text
        print(f'文字標題: {title}')
        for link in page_soup.find_all('a'):
            if re.match(r'/ncku_csie/Attachment/Download/', link.get('href')): # 有 Download 的連結
                doc_list.append('https://www.csie.ncku.edu.tw' + link.get('href')) # 把連結加到 doc_list

# 下載檔案
## TODO 下載到特定資料夾和名字

def download_doc(list: list):        
    for doc in tqdm(doc_list):
        driverPath = webdriver_path
        driver = webdriver.Chrome(driverPath)
        driver.get(doc) # 進入網頁
        time.sleep(1) # 等待網頁載入
        driver.close() # 關閉瀏覽器
 

get_announce_page(start_page=1, end_page=2)
get_doc_url(list=page_url_list)
download_doc(list=doc_list)
