import requests
import json

import emoji
import re
import mojimoji

from conf import settings

class StringUtil:

    def cleaning_text(self, text: str) -> str:
        text = emoji.replace_emoji(text)
        text = text.replace('\n','').replace('\r','')
        text = text.replace('\u3000', '')
        
        # 全角文字を半角に変換(カナ以外)
        text = mojimoji.zen_to_han(text, kana=False)
        # 半角カナを全角に変換
        text = mojimoji.han_to_zen(text, ascii=False)

        # 不要な記号等を除去
        text = text.lower()
        code_regex = re.compile('[\t!"#$%&\'\\\\()*+,-./:;；：<=>?@[\\]^_`{|}~○｢｣「」〔〕“”〈〉'\
            '『』【】＆＊（）＄＃＠？！｀＋￥¥％♪…◇→←↓↑｡･ω･｡ﾟ´∀｀ΣДｘ⑥◎©︎♡★☆▽※ゞノ〆εσ＞＜┌┘・т▼ᐟ๑•̀ㅂ•́و✧ดี꒳≧∇≦ꉂˊᗜˋºロ]')
        text = code_regex.sub('', text)
        code_regex_full_width = re.compile("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F\u202a-\u202c\u2460-\u2468]")
        text = code_regex_full_width.sub('', text)
        text = re.sub("[草笑w]+$", '', text)
        
        # 顔文字にアルファベットが使われている場合があり、こうしないと除去できなかった
        text = text.replace('m m', '')
        
        # 数字は不要
        num_regex = re.compile('\d+,?\d*')
        cleaned_text = num_regex.sub('', text)
        
        return cleaned_text
    
    def translate_to_ja(self, word_list: list) -> list:
        if (len(word_list) >= 1):
            url = 'https://api-free.deepl.com/v2/translate'
            headers = {'Authorization': 'DeepL-Auth-Key {}'.format(settings.DEEPL_AUTH_KEY), 'Content-Type': 'application/json'}
            json_data = {'text': word_list, 'target_lang': 'JA'}
            response = requests.post(url=url, headers=headers, json=json_data)
            json_obj = json.loads(response.text)

            translated_word_list = []
            for translation in json_obj['translations']:
                translated_word_list.append(translation['text'])
            
            return translated_word_list

        return word_list