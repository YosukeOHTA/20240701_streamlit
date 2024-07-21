# https://sumito.jp/2022/11/14/sharepoint-1g-file-upload/

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.creation_information import FileCreationInformation
import os

def get_sharepoint_context_using_user():
    sharepoint_url = 'https://xxxxxxxxxx.sharepoint.com/sites/upload-test'
    user_credentials = UserCredential('xxxxxxxxxx@sumito.jp', 'password')
    ctx = ClientContext(sharepoint_url).with_credentials(user_credentials)
    return ctx

def create_sharepoint_directory(dir_name: str):
    """
    Creates a folder in the sharepoint directory.
    """
    if dir_name:
        ctx = get_sharepoint_context_using_user()
        result = ctx.web.folders.add(f'Shared Documents/{dir_name}').execute_query()

    if result:
        # documents is titled as Shared Documents for relative URL in SP
        relative_url = f'Shared Documents/{dir_name}'
    return relative_url

target_url = "/sites/upload-test/Shared Documents/test-tsukada-dir-hoge"
ctx = get_sharepoint_context_using_user()
target_folder = ctx.web.get_folder_by_server_relative_url(target_url)
size_chunk = 1000000
local_path = "1G.csv"

def print_upload_progress(offset):
    file_size = os.path.getsize(local_path)
    print("Uploaded '{0}' bytes from '{1}'...[{2}%]".format(offset, file_size, round(offset / file_size * 100, 2)))

create_sharepoint_directory('test-tsukada-dir-hoge')
with open(local_path, 'rb') as f:
    uploaded_file = target_folder.files.create_upload_session(f, size_chunk,print_upload_progress).execute_query()