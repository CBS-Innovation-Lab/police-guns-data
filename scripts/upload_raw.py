"""
Uploads all files in all folders in the raw folder to Google Drive
so non-technical staff can access them, and I don't have to manually upload
new files every time I get a new one.
"""

import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def create_folder(drive, folder_name, parent_id=None):
    """Creates a folder in Google Drive and returns the ID."""
    folder_metadata = {
        "title": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        folder_metadata["parents"] = [{"id": parent_id}]
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder["id"]


def upload_files_to_folder(drive, folder_id, local_directory):
    """
    Uploads all files in a local directory to a folder in Google Drive.
    If folders in the local directory do not exist in Google Drive, they will be created.
    """
    for root, _, files in os.walk(local_directory):
        rel_root = os.path.relpath(root, local_directory)
        if rel_root != ".":
            parent_id = folder_id
            for folder in rel_root.split(os.sep):
                folder_query = (
                    f"title='{folder}' and mimeType='application/vnd.google-apps.folder' "
                    f"and trashed=false and '{parent_id}' in parents"
                )
                folders = drive.ListFile({"q": folder_query}).GetList()
                if not folders:
                    parent_id = create_folder(drive, folder, parent_id)
                else:
                    parent_id = folders[0]["id"]
        else:
            parent_id = folder_id

        for filename in files:
            file_path = os.path.join(root, filename)
            file_query = (
                f"title='{filename}' and trashed=false and '{parent_id}' in parents"
            )
            existing_files = drive.ListFile({"q": file_query}).GetList()

            local_file_size = os.path.getsize(file_path)
            should_upload = True

            if existing_files:
                gdrive_file = existing_files[0]
                gdrive_file_size = int(gdrive_file.get("fileSize", "0"))
                if local_file_size <= gdrive_file_size:
                    should_upload = False

            if should_upload:
                file = drive.CreateFile(
                    {"title": filename, "parents": [{"id": parent_id}]}
                )
                file.SetContentFile(file_path)
                file.Upload()
                print(f'Uploaded "{file_path}" to the folder.')
            else:
                print(f'"{file_path}" already exists in drive. Skipping.')


if __name__ == "__main__":
    FOLDER_ID = "1IwieEoK73LXMIZS-yp8wTMLoCYrYAVlV"
    LOCAL_DIRECTORY = "raw"
    CREDS_PATH = "credentials.json"

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(CREDS_PATH)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile(CREDS_PATH)
    gdrive = GoogleDrive(gauth)
    upload_files_to_folder(gdrive, FOLDER_ID, LOCAL_DIRECTORY)
