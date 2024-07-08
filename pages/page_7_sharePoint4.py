# https://sumito.jp/2022/11/14/sharepoint-1g-file-upload/
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.creation_information import FileCreationInformation
import os

def get_sharepoint_context_using_user():
    sharepoint_url = 'https://goldenhummingbird-my.sharepoint.com/personal/humming_goldenhummingbird_onmicrosoft_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fhumming%5Fgoldenhummingbird%5Fonmicrosoft%5Fcom%2FDocuments%2FYO14%5Fcooking&FolderCTID=0x0120005232DCB058E3294C9AC5B2457E50AF74&view=0'
    # sharepoint_url = 'https://xxxxxxxxxx.sharepoint.com/sites/upload-test'
    user_credentials = UserCredential('userId', 'password')
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

create_sharepoint_directory('test-tsukada-dir-hoge')
