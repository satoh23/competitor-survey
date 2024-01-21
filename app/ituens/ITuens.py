import requests
import json

from bs4 import BeautifulSoup
import html5lib

class ITuens:
    
    store_url_template = 'https://apps.apple.com/{}/app/id{}'
    ituens_api_url_template = 'https://itunes.apple.com/lookup?id={}&country={}'

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
    

    def getDescription(self, country: str, id: int) -> str:
        url = self.ituens_api_url_template.format(id, country)
        response = requests.get(url)
        result = json.loads(response.text)['results'][0]
        
        return result['description']
