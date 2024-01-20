import os.path
import os.path
import gspread

from conf import settings

class SpreadSheetOperation:

    def __init__(self, sheet_id: str,) -> None:
        credentials_filename = 'credentials.json'
        token_filename = 'gspread_token.json'

        gc = gspread.oauth(
                   credentials_filename=os.path.join(settings.DIR_PATH_GOOGLE_DRIVE_CREDENTIALS_JSON, credentials_filename), # 認証用のJSONファイル
                   authorized_user_filename=os.path.join(settings.DIR_PATH_GOOGLE_DRIVE_CREDENTIALS_JSON, token_filename), # 証明書の出力ファイル
                   )   
        self.workbook = gc.open_by_key(sheet_id)

    '''
    ワークシートを複製するメソッド
    '''
    def copy_sheet(self, new_sheet_name: str):
        try:
            template = self.workbook.get_worksheet(0)
            self.workbook.duplicate_sheet(source_sheet_id=template.id,
                          new_sheet_name = new_sheet_name)
        except Exception as error:
            print(f"ワークシートの複製に失敗しました: {error}")

    '''
    セルの値を更新するメソッド
    '''
    def write_all(self, worksheet_name: str, value_dic: dict):
        try:
            worksheet = self.workbook.worksheet(worksheet_name)

            # アプリ名
            self.__write_with_user_entered(worksheet, 'A1', value_dic['app_name'])
            # google driveに格納されたアプリアイコンのid
            self.__write_with_user_entered(worksheet, 'J1', self.__create_image_url(value_dic['icon_id']))
            # アプリがリリースされた日時
            self.__write_with_user_entered(worksheet, 'B3', value_dic['release_datetime'])
            # ダウンロード時の価格
            self.__write_with_user_entered(worksheet, 'F3', value_dic['download_price'])
            # アプリ容量
            self.__write_with_user_entered(worksheet, 'H3', value_dic['file_size'])
            # 推定年間売上
            self.__write_with_user_entered(worksheet, 'B5', value_dic['annual_sales'])
            # ダウンロード数
            self.__write_with_user_entered(worksheet, 'F5', value_dic['download_count'])
            # WAU数
            self.__write_with_user_entered(worksheet, 'H5', value_dic['wau_count'])
            # アプリ紹介文
            self.__write_with_user_entered(worksheet, 'A9', value_dic['description'])
            # 課金プラン一覧
            self.__write_with_user_entered(worksheet, 'J9', value_dic['billings'])
            # アプリ検索に使われるキーワードランキング
            self.__write_with_user_entered(worksheet, 'F25', value_dic['keyword_ranking'])
            # WAUの国籍ランキング
            self.__write_with_user_entered(worksheet, 'J25', value_dic['wau_nationality_ranking'])
            
            # 1カ国目のレビューのnlpの結果
            self.__write_with_user_entered(worksheet, 'A46', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['1']['good']))
            self.__write_with_user_entered(worksheet, 'A69', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['1']['normal']))
            self.__write_with_user_entered(worksheet, 'A92', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['1']['bad']))
            self.__write_with_user_entered(worksheet, 'A115', self.__create_image_url(value_dic['bagOfWords_result']['1']['good']))
            self.__write_with_user_entered(worksheet, 'A138', self.__create_image_url(value_dic['bagOfWords_result']['1']['normal']))
            self.__write_with_user_entered(worksheet, 'A161', self.__create_image_url(value_dic['bagOfWords_result']['1']['bad']))
            self.__write_with_user_entered(worksheet, 'A184', self.__create_image_url(value_dic['sunburstChart_result']['1']['good']))
            self.__write_with_user_entered(worksheet, 'A207', self.__create_image_url(value_dic['sunburstChart_result']['1']['normal']))
            self.__write_with_user_entered(worksheet, 'A230', self.__create_image_url(value_dic['sunburstChart_result']['1']['bad']))
            
            # 2カ国目のレビューのnlpの結果
            self.__write_with_user_entered(worksheet, 'A253', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['2']['good']))
            self.__write_with_user_entered(worksheet, 'A276', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['2']['normal']))
            self.__write_with_user_entered(worksheet, 'A299', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['2']['bad']))
            self.__write_with_user_entered(worksheet, 'A322', self.__create_image_url(value_dic['bagOfWords_result']['2']['good']))
            self.__write_with_user_entered(worksheet, 'A345', self.__create_image_url(value_dic['bagOfWords_result']['2']['normal']))
            self.__write_with_user_entered(worksheet, 'A368', self.__create_image_url(value_dic['bagOfWords_result']['2']['bad']))
            self.__write_with_user_entered(worksheet, 'A391', self.__create_image_url(value_dic['sunburstChart_result']['2']['good']))
            self.__write_with_user_entered(worksheet, 'A414', self.__create_image_url(value_dic['sunburstChart_result']['2']['normal']))
            self.__write_with_user_entered(worksheet, 'A437', self.__create_image_url(value_dic['sunburstChart_result']['2']['bad']))

            # 3カ国目のレビューのnlpの結果
            self.__write_with_user_entered(worksheet, 'A460', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['3']['good']))
            self.__write_with_user_entered(worksheet, 'A483', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['3']['normal']))
            self.__write_with_user_entered(worksheet, 'A506', self.__create_image_url(value_dic['coOccurrenceNetwork_result']['3']['bad']))
            self.__write_with_user_entered(worksheet, 'A529', self.__create_image_url(value_dic['bagOfWords_result']['3']['good']))
            self.__write_with_user_entered(worksheet, 'A552', self.__create_image_url(value_dic['bagOfWords_result']['3']['normal']))
            self.__write_with_user_entered(worksheet, 'A575', self.__create_image_url(value_dic['bagOfWords_result']['3']['bad']))
            self.__write_with_user_entered(worksheet, 'A598', self.__create_image_url(value_dic['sunburstChart_result']['3']['good']))
            self.__write_with_user_entered(worksheet, 'A621', self.__create_image_url(value_dic['sunburstChart_result']['3']['normal']))
            self.__write_with_user_entered(worksheet, 'A644', self.__create_image_url(value_dic['sunburstChart_result']['3']['bad']))

        except Exception as error:
            print(f"スプレッドシートへの書き込みに失敗しました: {error}")
    
    def __create_image_url(self, parameter: str) -> str:
        return '=image("https://lh3.googleusercontent.com/d/{}")'.format(parameter)
    
    def __write_with_user_entered(self, worksheet, range_name: str, values: str):
        try:
            worksheet.update(range_name=range_name, values=values, value_input_option='USER_ENTERED')
        except Exception:
            raise

