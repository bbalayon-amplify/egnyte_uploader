"""Service layer for download DYD reports"""

import os
import requests
from common.logging import get_logger
from common.constants import FILE_NAME, REMOTE_FOLDER_PATH
import egnyte


logger = get_logger(__name__)
AUTH_TOKEN_URL = "https://amplifyeducation.egnyte.com/puboauth/token"
AUTH_REQUEST_HEADERS = {'Content-type': 'application/x-www-form-urlencoded'}
AUTH_REQUEST_DATA = {
    "grant_type": "password",
    "username": "x",
    "password": "x",
    "client_id": "x"
}


def _get_client():
    logger.info("Getting Egnyte auth token")
    header = {'Content-type': 'application/x-www-form-urlencoded'}
    request = requests.post("https://amplifyeducation.egnyte.com/puboauth/token", headers=header, params=AUTH_REQUEST_DATA)
    token = request.json()['access_token']
    client_parmas = {
        "domain": "amplifyeducation.egnyte.com", 
        "access_token": token,
    }
    return egnyte.EgnyteClient(client_parmas)

def _upload_to_folder(client):
    dyd_reports = FILE_NAME.values()
    full_path = map(lambda report: f"./tmp/{report}", dyd_reports)
    for file_name, local_path in zip(dyd_reports, full_path):
        fileobj = client.file(f"{REMOTE_FOLDER_PATH}/{file_name}")
        logger.info(f"Uploading {file_name}")
        with open(local_path,'rb') as to_upload:
            fileobj.upload(to_upload)


def upload_report(local_path: str, file_name: str):
    """Connect to Egnyte and transfer the DYD report to Egnyte folder"""
    try:
        client = _get_client()
        _upload_to_folder(client)
        logger.info("Upload to Egnyte complete!")
    except Exception as ex:
        logger.exception(f"Error with uploading report to Egnyte: {ex}")
        raise ex