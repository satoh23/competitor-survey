import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
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
from type.Reviews import Reviews

class ITuens:
    
    store_url_template = 'https://apps.apple.com/{}/app/id{}'
    ituens_api_url_template = 'https://itunes.apple.com/lookup?id={}&country={}'

    def __init__(self):
        self.chrome_service = fs.Service(executable_path=settings.CHROMEDRIVER)
        self.driver = webdriver.Chrome(service=self.chrome_service)

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
        try:
            self.driver.get(url)
            
            sleep(1)
            result_list = []
            for i in range(1,5):
                element = self.driver.find_element(By.CSS_SELECTOR, '#users-country > div > div.right > ul > li:nth-child({})'.format(i))
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
            self.driver.quit()
        
        return result

    '''
    アプリダウンロード時の価格をStringで返す
    0円の場合は「無料」と返す
    '''
    def getPrice(self, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        
        return json.loads(response.text)['results'][0]['formattedPrice']

    '''
    アプリがリリースされた日時を返す
    '''
    def getReleaseDay(self, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)

        return json.loads(response.text)['results'][0]['releaseDate']

    '''
    アプリのレビューを500件取得する
    外部apiの仕様上500件までしか取得できない
    '''
    def getReviews(self, country: str, id: int) -> Reviews:
        reviews = Reviews()

        page_num = 1
        while True:
            url = 'https://itunes.apple.com/{}/rss/customerreviews/page={}/id={}/json'.format(country, page_num, id)
            response = requests.get(url)
            if response:
                json_obj = json.loads(response.text)
                entry_list = json_obj['feed']['entry']

                for obj in entry_list:
                    rate = int(obj['im:rating']['label'])  # レビューの星の数
                    review = obj['content']['label']

                    if rate >= 4:
                        reviews.good_review_list.append(review)
                    elif rate == 3:
                        reviews.normal_review_list.append(review)
                    elif rate <= 2:
                        reviews.bad_review_list.append(review)
                page_num += 1
            else:
                print('レビューが取得できませんでした。page_num={}'.format(page_num))
                break

        return reviews
    
    '''
    アプリ検索時に使用されるキーワードランキングを取得する
    '''
    def getSearchKeywordRanking(self, url:str):
        country_codes = ['US', 'GB', 'JP', 'KR']
        keyword_ranking = {}
        try:
            for country_code in country_codes:
                country_dict = {}
                # ループごとにドライバーを作り直す必要がある
                driver = webdriver.Chrome(service=self.chrome_service)
                driver.get(url + '?keyword_country={}'.format(country_code))
                sleep(1)
                
                for i in range(1, 5):
                    keyword_info_dict = {}

                    element = driver.find_element(By.CSS_SELECTOR, '#app-ranked > div.inside.no-padding > div.ranked-graph > ul > li:nth-child({})'.format(i))
                    keyword_info_list = element.text.split('\n')
                    
                    index = keyword_info_list[0].find(' #')
                    keyword_info_dict['keyword'] = keyword_info_list[0][:index]
                    keyword_info_dict['ratio'] = keyword_info_list[2]
                    
                    country_dict[i] = keyword_info_dict
                
                driver.quit()
                keyword_ranking[country_code] = country_dict
        except NoSuchElementException:
            print('要素が取得できませんでした')

        # TODO 変更が必要になった時に大変なのでなんとかしたい
        return 'US\n'\
                '--------------\n'\
                '{} {}\n'.format(keyword_ranking['US'][1]['keyword'], keyword_ranking['US'][1]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['US'][2]['keyword'], keyword_ranking['US'][2]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['US'][3]['keyword'], keyword_ranking['US'][3]['ratio']) + \
                '{} {}\n\n'.format(keyword_ranking['US'][4]['keyword'], keyword_ranking['US'][4]['ratio']) + \
                'JP\n'\
                '--------------\n'\
                '{} {}\n'.format(keyword_ranking['JP'][1]['keyword'], keyword_ranking['JP'][1]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['JP'][2]['keyword'], keyword_ranking['JP'][2]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['JP'][3]['keyword'], keyword_ranking['JP'][3]['ratio']) + \
                '{} {}\n\n'.format(keyword_ranking['JP'][4]['keyword'], keyword_ranking['JP'][4]['ratio']) + \
                'GB\n'\
                '--------------\n'\
                '{} {}\n'.format(keyword_ranking['GB'][1]['keyword'], keyword_ranking['GB'][1]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['GB'][2]['keyword'], keyword_ranking['GB'][2]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['GB'][3]['keyword'], keyword_ranking['GB'][3]['ratio']) + \
                '{} {}\n\n'.format(keyword_ranking['GB'][4]['keyword'], keyword_ranking['GB'][4]['ratio']) + \
                'KR\n'\
                '--------------\n'\
                '{} {}\n'.format(keyword_ranking['KR'][1]['keyword'], keyword_ranking['KR'][1]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['KR'][2]['keyword'], keyword_ranking['KR'][2]['ratio']) + \
                '{} {}\n'.format(keyword_ranking['KR'][3]['keyword'], keyword_ranking['KR'][3]['ratio']) + \
                '{} {}\n\n'.format(keyword_ranking['KR'][4]['keyword'], keyword_ranking['KR'][4]['ratio'])
                