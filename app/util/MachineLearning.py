from conf import settings

import ginza
import spacy
import pandas as pd
import nlplot
import plotly.io as pio

from wordcloud import WordCloud

class MachineLearning:
    
    path_of_images_dir = '../images/'

    def __init__(self):
        nlp_ja = spacy.load('ja_ginza_electra')
        ja_dict = self.__create_country_dict(nlp_ja, 'Japanese.txt')
        nlp_en = spacy.load('en_core_web_lg')
        en_dict = self.__create_country_dict(nlp_en, 'English.txt')
        nlp_zh = spacy.load('zh_core_web_lg')
        zh_dict = self.__create_country_dict(nlp_zh, 'Chinese.txt')
        
        self.country_dict = {'ja': ja_dict, 'en': en_dict, 'zh': zh_dict}

    '''
    前処理後のデータフレームを返却する関数
    '''
    def create_data_frame_after_nlp(self, cleaned_text_list: list, language: str):
        country_info = self.country_dict[language]
        nlp = country_info['nlp']
        
        after_nlp_text_list = []
        for cleaned_text in cleaned_text_list:
            doc = nlp(cleaned_text)
            ginza.set_split_mode(nlp, "C")
            after_nlp_text_list.append(doc)
        
        include_pos = ('NOUN', 'PROPN', 'VERB', 'ADJ')
        stop_words = self.__create_stopwords(country_info['stopwords_file'])
        word_list = []
        for after_nlp_text in after_nlp_text_list:
            for sent in after_nlp_text.sents:
                sep_word = [
                    token.lemma_ for token in sent if token.pos_ in include_pos and token.lemma_ not in stop_words]
                word_list.append(sep_word)
        
        data_frame = pd.DataFrame(columns=['SEP_WORD'])
        data_frame['SEP_WORD'] = [s for s in word_list]

        return data_frame

    '''
    BOWを作成し、pngで保存する関数
    '''
    def create_png_of_bagOfWords(self, data_frame, language: str, app_name: str) -> str:
        word_list = []
        for words_list in data_frame['SEP_WORD']:
            for word in words_list:
                word_list.append(word)
        
        stop_words = self.__create_stopwords(self.country_dict[language]['stopwords_file'])
        wordcloud = WordCloud(background_color='white',
                              width=1920,
                              height=1080,
                              font_path='/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc',
                              stopwords=set(stop_words)).generate(' '.join(word_list))        
        file_name = 'bagOfWords_' + language + '_' + app_name + '.png'
        wordcloud.to_file(self.path_of_images_dir + file_name)

        return file_name

    '''
    サンバーストチャートを作成し、pngで保存する関数
    '''
    def create_png_of_sunburstChart(self, data_frame, language: str, app_name: str) -> str:
        npt = nlplot.NLPlot(data_frame, target_col='SEP_WORD')
        npt_stopwords = npt.get_stopword(top_n=2, min_freq=0)
        npt.build_graph(stopwords=npt_stopwords, min_edge_frequency=5)

        title = 'Sunburst_chart_' + language + '_' + app_name
        fig_sunburst = npt.sunburst(
            title=title,
            colorscale=True,
            color_continuous_scale='Oryel',
            width=1000,
            height=800,
        )
        file_name = title + '.png'
        # 画像保存
        pio.write_image(fig_sunburst, self.path_of_images_dir + file_name, engine='kaleido')

        return file_name

    '''
    共起ネットワークを作成し、pngで保存する関数
    '''
    def create_png_of_coOccurrenceNetwork(self, data_frame, language: str, app_name: str) -> str:
        npt = nlplot.NLPlot(data_frame, target_col='SEP_WORD')
        npt.build_graph(min_edge_frequency=5)

        title = 'Co-occurrence_network_' + language + '_' + app_name
        fig_co_network = npt.co_network(
            title=title,
            sizing=100,
            node_size='adjacency_frequency',
            color_palette='hls',
            width=1920,
            height=1080,
        )
        file_name = title + '.png'
        # 画像保存
        pio.write_image(fig_co_network, self.path_of_images_dir + file_name, engine='kaleido')

        return file_name

    '''
    ストップワード一覧を作成する関数
    '''
    def __create_stopwords(self, country: str) -> list:
        stopwords = []
        with open(settings.DIR_PATH_STOPWORDS + country) as file:
            for stopword in file.read().splitlines():
                stopwords.append(stopword)
        return stopwords
    
    '''
    自然言語処理用のモデルとストップワード一覧のファイル名を格納した辞書を作成する関数
    '''
    def __create_country_dict(self, nlp, file_name) -> dict:
        return {'nlp': nlp, 'stopwords_file': file_name}