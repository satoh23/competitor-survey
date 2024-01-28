import requests
from time import sleep

from google_play_scraper import app
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.common.exceptions import NoSuchElementException

from conf import settings

class GooglePlay:

    def __init__(self, id: str, lang: str, country: str) -> None:
        self.result = app(
            id,
            lang=lang,
            country=country
        )        
        self.chrome_service = fs.Service(executable_path=settings.CHROMEDRIVER)
    
    '''
    課金プランの最低額と最高額を取得する
    '''
    def getBillings(self) -> str:
        return self.result['inAppProductPrice'].replace('/アイテム', '')

    '''
    アプリの紹介文を取得する
    '''
    def getDescription(self) -> str:
        return self.result['description']

    '''
    ダウンロード数を取得する
    '''
    def getDownloadCount(self) -> str:
        return self.result['minInstalls']

    '''
    アプリのアイコンを取得する
    できなければNoneを返す
    '''
    def getIconImageOrNone(self, app_name) -> str:
        icon_url = None
        if (len(self.result['icon']) > 0):
            icon_url = self.result['icon']
            icon = requests.get(icon_url)

            file_name = app_name + '_google.png'
            with open('../images/{}'.format(file_name), 'wb') as f:
                f.write(icon.content)
            return file_name
        else:
            print('アイコンの画像が取得できませんでした')
            return None

    '''
    アプリのユーザーの国籍ランキングを取得
    '''
    def getNationalityRanking(self, url: str):
        try:
            driver = webdriver.Chrome(service=self.chrome_service)
            driver.get(url)
            
            sleep(1)
            result_list = []
            for i in range(1,5):
                element = driver.find_element(By.CSS_SELECTOR, '#users-country > div > div.right > ul > li:nth-child({})'.format(i))
                text = element.text.replace('\nアクティブユーザー\n', ':')
                colon_index = text.find(':')
                result_list.append(text[:colon_index])
                newline_index = text.find('\n')
                result_list.append(text[:newline_index][colon_index+1:] + '\n')
        except NoSuchElementException:
            print('要素が取得できませんでした')
            result = ''
        else:
            result = '\n'.join(result_list)
        finally:
            driver.quit()
        
        return result

    '''
    アプリリリース日を取得
    '''
    def getReleaseDay(self):
        return self.result['released']
