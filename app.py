from bs4 import BeautifulSoup, SoupStrainer
import cchardet
import lxml
import requests
import re
from selenium import webdriver
from tqdm import tqdm
import time
import parser
import argparse
import threading
from selenium.webdriver.chrome.service import Service
import pathlib


parser = argparse.ArgumentParser()
parser.add_argument('--start_page', type=int, default=1, help='start page, default: 1')
parser.add_argument('--end_page', type=int, default=2, help='end page, default: 2')
parser.add_argument('--download', type=str, default=False, help='download doc or not, default: False')

args = parser.parse_args()
start_page = args.start_page
end_page = args.end_page
download = args.download

page_url_list = []
doc_list = []
thread_list = []
webdriver_path = './chromedriver' # chromedriver path
download_path = "/download" # download path

# if download_path not exist, create it
pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)

# selenium webdriver config
chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0, # disable download window pop up
'download.default_directory':download_path, # setting download path
"profile.default_content_setting_values.automatic_downloads":1, # allow multiple download
"download.manager.showWhenStarting":False, # disable download manager
}
chrome_options.add_experimental_option('prefs', prefs)


# main
requests_session = requests.Session()
ncku_url = 'https://www.csie.ncku.edu.tw'



# 把所有公告頁面的連結都抓下來
def get_announce_page(start_page: int, end_page: int) -> list:

    base_url = 'https://www.csie.ncku.edu.tw/ncku_csie/announce/news/1000'
    urls = [f'{base_url}?Infolist_page={page}' for page in range(start_page, end_page+1,1)]  # 1~100頁的網址清單，100 頁是到 2020-08-17
    for url in tqdm(urls):

        web = requests_session.get(url)
        web.encoding = 'utf-8' # 設定編碼
        soup = BeautifulSoup(web.text, 'lxml')       
    
        # get /ncku_csie/announce/view/ page
        for link in soup.find_all('a'):
            if link.get('href') is not None: # 有連結
                if re.match(r'/ncku_csie/announce/view/\d+', link.get('href')): # 有 /ncku_csie/announce/view/ 的連結
                    page_url_list.append(link.get('href')) # 把連結加到 page_url_list

# 把公告裡有 Download 的連結都抓下來
def get_doc_url(page: str) -> list:

    page = ncku_url + page
    web = requests_session.get(page)
    web.encoding = 'utf-8' # 設定編碼
    page_soup = BeautifulSoup(web.text, 'lxml', parse_only=SoupStrainer(class_="odd")) # 目前檔案下載都會在 odd class 裡面
    title = page_soup.find('td').text
    print(f'文字標題: {title}')
    print(f'網址: {page}\n')
    for link in page_soup.find_all('a'):
        if re.match(r'/ncku_csie/Attachment/Download/', link.get('href')): # 有 Download 的連結
            doc_list.append(link.get('href')) # 把連結加到 doc_list

# 下載檔案
## TODO 下載到特定資料夾和名字

def download_doc(doc_list: list):     
    for doc in tqdm(doc_list):
        doc = ncku_url + doc
        driver = webdriver.Chrome(service=Service(webdriver_path), options=chrome_options)
        driver.get(doc) # 進入網頁
        time.sleep(1) # 等待網頁載入
        driver.close() # 關閉瀏覽器

if __name__ == '__main__':

    start_time = time.time()
    print(f'抓取 {start_page} ~ {end_page} 頁的公告\n')

    get_announce_page(start_page=start_page, end_page=end_page)
    print(f'共抓取 {len(page_url_list)} 篇公告\n')

    # get doc url with threading

    for index, page in enumerate(page_url_list):
        page_thread = threading.Thread(target=get_doc_url, args=(page,))
        thread_list.append(page_thread)

    # 開始
    for thread in thread_list:
        thread.start()

    # 等待所有子執行緒結束
    for thread in thread_list:
        thread.join()

    if download == True:
        download_doc(doc_list=doc_list)
        print(f'共抓取 {len(doc_list)} 個檔案\n')

    print(f'共抓取 {len(doc_list)} 個檔案\n')
    end_time = time.time()
    print(f'所用時間: {time.time() - start_time}')  

