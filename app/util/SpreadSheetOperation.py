import os.path
import os.path
import gspread

from conf import settings
from type import AppInfo

class SpreadSheetOperation:

    def __init__(self, sheet_id: str) -> None:
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
    def write_all(self, worksheet_name: str, app: AppInfo):
        try:
            worksheet = self.workbook.worksheet(worksheet_name)
            image_url_template = '=image("https://lh3.googleusercontent.com/d/{}")'

            # アプリ名
            self.__write_with_user_entered(worksheet, 'A1', app.name)
            # google driveに格納されたアプリアイコンのid
            self.__write_with_user_entered(worksheet, 'J1', image_url_template.format(app.icon_id))
            # アプリがリリースされた日時
            self.__write_with_user_entered(worksheet, 'B3', app.release_datetime)
            # ダウンロード時の価格
            self.__write_with_user_entered(worksheet, 'F3', app.download_price)
            # アプリ容量
            self.__write_with_user_entered(worksheet, 'H3', app.file_size)
            # 推定年間売上
            self.__write_with_user_entered(worksheet, 'B5', app.annual_sales)
            # ダウンロード数
            self.__write_with_user_entered(worksheet, 'F5', app.download_count)
            # WAU数
            self.__write_with_user_entered(worksheet, 'H5', app.wau_count)
            # アプリ紹介文
            self.__write_with_user_entered(worksheet, 'A9', app.description)
            # 課金プラン一覧
            self.__write_with_user_entered(worksheet, 'J9', app.billings)
            # アプリ検索に使われるキーワードランキング
            self.__write_with_user_entered(worksheet, 'F25', app.keyword_ranking)
            # WAUの国籍ランキング
            self.__write_with_user_entered(worksheet, 'J25', app.wau_nationality_ranking)
            
            # 1カ国目のレビューのnlpの結果
            self.__write_with_user_entered(worksheet, 'A46', image_url_template.format(app.coOccurrenceNetwork_result['1']['good']))
            self.__write_with_user_entered(worksheet, 'A69', image_url_template.format(app.coOccurrenceNetwork_result['1']['normal']))
            self.__write_with_user_entered(worksheet, 'A92', image_url_template.format(app.coOccurrenceNetwork_result['1']['bad']))
            self.__write_with_user_entered(worksheet, 'A115', image_url_template.format(app.bagOfWords_result['1']['good']))
            self.__write_with_user_entered(worksheet, 'A138', image_url_template.format(app.bagOfWords_result['1']['normal']))
            self.__write_with_user_entered(worksheet, 'A161', image_url_template.format(app.bagOfWords_result['1']['bad']))
            self.__write_with_user_entered(worksheet, 'A184', image_url_template.format(app.sunburstChart_result['1']['good']))
            self.__write_with_user_entered(worksheet, 'A207', image_url_template.format(app.sunburstChart_result['1']['normal']))
            self.__write_with_user_entered(worksheet, 'A230', image_url_template.format(app.sunburstChart_result['1']['bad']))
            
            # 2カ国目のレビューのnlpの結果
            self.__write_with_user_entered(worksheet, 'A253', image_url_template.format(app.coOccurrenceNetwork_result['2']['good']))
            self.__write_with_user_entered(worksheet, 'A276', image_url_template.format(app.coOccurrenceNetwork_result['2']['normal']))
            self.__write_with_user_entered(worksheet, 'A299', image_url_template.format(app.coOccurrenceNetwork_result['2']['bad']))
            self.__write_with_user_entered(worksheet, 'A322', image_url_template.format(app.bagOfWords_result['2']['good']))
            self.__write_with_user_entered(worksheet, 'A345', image_url_template.format(app.bagOfWords_result['2']['normal']))
            self.__write_with_user_entered(worksheet, 'A368', image_url_template.format(app.bagOfWords_result['2']['bad']))
            self.__write_with_user_entered(worksheet, 'A391', image_url_template.format(app.sunburstChart_result['2']['good']))
            self.__write_with_user_entered(worksheet, 'A414', image_url_template.format(app.sunburstChart_result['2']['normal']))
            self.__write_with_user_entered(worksheet, 'A437', image_url_template.format(app.sunburstChart_result['2']['bad']))

            # 3カ国目のレビューのnlpの結果
            self.__write_with_user_entered(worksheet, 'A460', image_url_template.format(app.coOccurrenceNetwork_result['3']['good']))
            self.__write_with_user_entered(worksheet, 'A483', image_url_template.format(app.coOccurrenceNetwork_result['3']['normal']))
            self.__write_with_user_entered(worksheet, 'A506', image_url_template.format(app.coOccurrenceNetwork_result['3']['bad']))
            self.__write_with_user_entered(worksheet, 'A529', image_url_template.format(app.bagOfWords_result['3']['good']))
            self.__write_with_user_entered(worksheet, 'A552', image_url_template.format(app.bagOfWords_result['3']['normal']))
            self.__write_with_user_entered(worksheet, 'A575', image_url_template.format(app.bagOfWords_result['3']['bad']))
            self.__write_with_user_entered(worksheet, 'A598', image_url_template.format(app.sunburstChart_result['3']['good']))
            self.__write_with_user_entered(worksheet, 'A621', image_url_template.format(app.sunburstChart_result['3']['normal']))
            self.__write_with_user_entered(worksheet, 'A644', image_url_template.format(app.sunburstChart_result['3']['bad']))

        except Exception as error:
            print(f"スプレッドシートへの書き込みに失敗しました: {error}")
    
    '''
    value_input_option=USER_ENTEREDでワークシートに値を書き込む関数
    '''
    def __write_with_user_entered(self, worksheet, range_name: str, values: str):
        try:
            worksheet.update(range_name=range_name, values=values, value_input_option='USER_ENTERED')
        except Exception:
            raise

