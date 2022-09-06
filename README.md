> 原由

- 實驗室剛好要換新的官網，所以我就想說要不要寫個爬蟲來幫忙下載官網的資料，然後就有了這個 repo。
    - 因為數量不少，所以也有參考一些加速的方法，讓爬蟲的速度更快。

- cchardet, lxml 都是可以加速 bs4 的套件
    - 使用前要先 pip3 install cchardet lxml


- webdriver 需要下載 chromedriver
    - dowload link: https://chromedriver.chromium.org/downloads

---

> usage

- 目前有兩個變數可以輸入
    - start_page: 起始頁數
    - end_page: 結束頁數
- 範例
    - python3 app.py --start_page=1 --end_page=20


---
> requirements

```
beautifulsoup4
cchardet
lxml
requests
selenium
tqdm
```

---

> reference:
1. [Python BeautifulSoup 中文亂碼問題](https://iter01.com/568912.html)
2. [How to download a file using Selenium and Python](https://www.browserstack.com/guide/download-file-using-selenium-python)
3. [[Day23] Beautiful Soup 網頁解析！](https://ithelp.ithome.com.tw/articles/10196817)
4. [Rename downloaded files selenium](https://stackoverflow.com/questions/38459972/rename-downloaded-files-selenium)
5. [https://thehftguy.com/2020/07/28/making-beautifulsoup-parsing-10-times-faster/](https://thehftguy.com/2020/07/28/making-beautifulsoup-parsing-10-times-faster/)
6. [Imporve bs4 performance](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id65)


