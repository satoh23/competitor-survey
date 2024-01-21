import requests
from bs4 import BeautifulSoup
import html5lib

class ITuens:
    
    store_url_template = 'https://apps.apple.com/{}/app/id{}'

    def getBillings(self, country: str, app_id: int) -> str:
        url = self.store_url_template.format(country, app_id)  
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        elements = soup.find_all(attrs={"class": "list-with-numbers__item"})

        billing_list = []
        for element in elements:
            billing = element.get_text().replace('\n', '').replace(' ', '').replace('¥', ' ¥')
            billing_list.append(billing)
        billings = '\n'.join(billing_list)
        
        return billings
    