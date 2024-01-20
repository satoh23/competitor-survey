import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload

from conf import settings

class GoogleDriveOperation:

    def __init__(self) -> None:
        creds = None
        credentials_filename = 'credentials.json'
        token_filename = 'token.json'

        if os.path.exists(token_filename):
            creds = Credentials.from_authorized_user_file(token_filename, settings.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_filename, settings.SCOPES
                )
                creds = flow.run_local_server(port=0)
                with open(token_filename, 'w') as token:
                    token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    '''
    ローカルの画像をgoogle driveにアップロードするメソッド
    '''
    def upload_image(self, file_name: str) -> str:
        file_metadata = {
            'name': file_name,
            'parents': settings.GOOGLE_DRIVE_IMAGES_FOLDER_ID
        }
        media = MediaFileUpload(
            settings.IMAGES_DIR_PATH + file_name,
            mimetype=GoogleDriveOperation.__get_mimetype(file_name),
            resumable=True
        )
        try:
            # google driveに画像をアップロード
            result_file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

        return result_file.get('id')

    '''
    google driveに格納されているアプリ分析の結果出力用ワークブックのテンプレートを複製するメソッド
    '''
    def copy_workbook_template(self, sheet_name: str) -> str:
        now_datetime = datetime.date.today()
        date = now_datetime.strftime('%Y%m%d')
        file_name = date + '_' + sheet_name

        new_file_body = {
        'name': file_name,  # 処理結果のスプレッドシートのファイル名
        'parents': settings.RESULT_DIR_ID  # 処理結果のスプレッドシートを格納するフォルダーのID
        }
        try:
            # スプレッドシートを複製
            result_file = self.service.files().copy(
                fileId=settings.TEMPLATE_SPREADSHEET_ID,
                body=new_file_body
                ).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

        return result_file.get('id')
    
    '''
    画像ファイルの拡張子から適切なmimetypeを判定し、返却するメソッド
    '''
    def __get_mimetype(file_name: str) -> str:
        mimetype_dict = {'jpg': 'image/jpeg', 'png': 'image/png'}

        index = file_name.find('.')
        extension = file_name[index + 1:]

        return mimetype_dict[extension]
