import requests
from bs4 import BeautifulSoup
import html5lib

class ITuens:
    
    store_url_template = 'https://apps.apple.com/{}/app/id{}'

    def getBillingsOrNone(self, country: str, app_id: int) -> str:
        url = self.store_url_template.format(country, app_id)  
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
    