import requests
import json

from bs4 import BeautifulSoup
import html5lib

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
                billing = element.get_text().replace('\n', '').replace(' ', '').replace('¥', ' ¥')
                billing_list.append(billing)
            billings = '\n'.join(billing_list)
    
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
    def getEstimatedDownloadCount(self, download_count: str) -> int:
        return round(int(download_count) * 0.33)

    '''
    アプリ容量を取得する
    '''
    def getFileSize(self, country: str, id: int):
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        json_obj = json.loads(response.text)
        file_size = int(json_obj['results'][0]['fileSizeBytes']) / 1024 / 1024
        return str(round(file_size)) + 'MB'

    '''
    アプリのアイコンを取得する
    取得できなければNoneを返す
    '''
    def getIconImageOrNone(self, app_name: str, country: str, id: int):
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
        with open('../images/{}'.format(app_name + '_ituens'), 'wb') as file:
            file.write(icon.content)