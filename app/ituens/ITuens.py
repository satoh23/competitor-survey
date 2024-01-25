import requests
import json
from time import sleep

from bs4 import BeautifulSoup
import html5lib
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from conf import settings

class ITuens:
    
    store_url_template = 'https://apps.apple.com/{}/app/id{}'
    ituens_api_url_template = 'https://itunes.apple.com/lookup?id={}&country={}'

    '''
    課金プラン一覧を取得する
    取得できない場合はNoneを返す
    '''
    def getBillingsOrNone(self, country: str, id: int) -> str:
        url = self.store_url_template.format(country, id)  
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        elements = soup.find_all(attrs={"class": "list-with-numbers__item"})

        billing_list = []
        billings = None
        if (len(elements) >= 1):
            for element in elements:
                # 半角スペースがプラン名と価格の間にたくさんある為、一旦除去してから再度追加する。
                billing = element.get_text().replace('\n', '').replace(' ', '').replace('¥', '\n¥')
                billing_list.append(billing)
            billings = '\n\n'.join(billing_list)
    
        return billings
    
    '''
    紹介文を取得する
    '''
    def getDescription(self, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        result = json.loads(response.text)['results'][0]
        
        return result['description']

    '''
    該当アプリのiTuensストアでの推定ダウンロード数を取得する
    iTuensはダウンロード数を取得できないため、Google Playでの同アプリのダウンロード数から推定を行う
    '''
    def getEstimatedDownloadCount(self, download_count_google_play: str) -> int:
        return round(int(download_count_google_play) * 0.33)

    '''
    アプリ容量を取得する
    '''
    def getFileSize(self, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        json_obj = json.loads(response.text)
        file_size = int(json_obj['results'][0]['fileSizeBytes']) / 1024 / 1024
        return str(round(file_size)) + 'MB'

    '''
    アプリのアイコンを取得する
    取得できなければNoneを返す
    '''
    def getIconImageOrNone(self, app_name: str, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        result = json.loads(response.text)['results'][0]

        icon_url = None
        # 512,100,60はそれぞれ画像のサイズのことだと思う
        if (len(result['artworkUrl512']) > 0):
            icon_url = result['artworkUrl512']
        elif (len(result['artworkUrl100']) > 0):
            icon_url = result['artworkUrl100']
        elif (len(result['artworkUrl60']) > 0):
            icon_url = result['artworkUrl60']
        else:
            print('アイコンの画像が取得できませんでした')
            return None

        icon = requests.get(icon_url)
        image_file_name = app_name + '_ituens.png'
        with open('../images/{}'.format(image_file_name), 'wb') as file:
            file.write(icon.content)

        return image_file_name

    '''
    アプリのユーザーの国籍ランキングを返す
    '''
    def getNationalityRankingOrEmpty(self, url: str) -> str:
        chrome_service = fs.Service(executable_path=settings.CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        try:
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
    アプリダウンロード時の価格をStringで返す
    0円の場合は「無料」と返す
    '''
    def getPrice(self, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        
        return json.loads(response.text)['results'][0]['formattedPrice']
