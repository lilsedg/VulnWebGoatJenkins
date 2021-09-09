## Import libraries
# !/usr/bin/env python
import time
import os
import glob
import json
import logging
from datetime import datetime
import requests

## Log file name
LOGFILE_NAME = "Dependency Check" + '_import.log'
LOGFILE_NAME = LOGFILE_NAME.replace(' ', '_').lower()

## Initiating the logger
logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO, format='%(levelname)s: %(message)s -- %(asctime)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

## Initiating the log writing
logging.info('------------------------------------------')
logging.info('Scan started')

SCRIPT_VERSION = '1.0'
logging.info('Script Version : ' + SCRIPT_VERSION)


## Endpoint to fetch secure one-time url to upload scan files
url_upload = 'https://app.armorcode.com/client/utils/s3/upload'

## Api key to secure the access of url_upload
api_key = '3dcff0c6-eec6-4800-bc31-e3a9b1b30816'  ## Kindly download the API Key from ArmorCode website and place it here.

folder_name = r"/home/vsts/work/1/TestResults/dependency-check/"
file_extension = "dependency-check-report.xml"

## Headers for accessing the upload url
headers = {
    'Authorization': 'Bearer ' + api_key,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


## Metadata of the scan tool
data_json = {
    'env': "Production",
    'product': 768,
    'subProduct': 1852,
    'scanTool': "Dependency Check Scan",
    'tags': "",
    'fileName': ''
}


def get_latest_file(folder_name, file_extension):
    '''
    Purpose: This function is used to fetch the latest scan file of the tool based on the following parameters
    :param folder_name: Full path of the folder where scan files are getting stored
    :param file_extension: File extension of the scan files, its pre defined for all the tools.
    :return: latest_file, its the latest file of the tool.
    '''
    latest_file = ''
    try:
        files = []
        folder_name = folder_name.strip()
        file_extension = file_extension.strip()
        for file_name in glob.glob(folder_name + '*' + file_extension):
            files.append(file_name)
        if files:
            latest_file = max(files, key=os.path.getctime)
            logging.info('latest file identified : ' + latest_file)
        else:
            print('No such file found in the directory.')
            logging.error('No such file found in the directory.')
    except Exception as e:
        print('Error in getting latest file')
        logging.error('Error in getting latest file: ' + str(e))
    return latest_file


def get_signed_url(url, header, json_data):
    '''
    Purpose: This function returns a secure one-time url to upload the scan file
    :param url: Its the endpoint to hit for getting the signed url
    :param header: Header object to hit the above endpoint
    :param json_data: Metadata of the scan
    :return: url, its a secure one-time use url to upload the scan file
    '''
    url_signed = ''
    try:
        if 'please_insert_api_key_here' in header['Authorization']:
            print('\nAPI Key not updated!!\nKindly update the API Key to run this script.\n')
            logging.error('API Key not updated, kindly update the API Key to run this script.')
            return url_signed

        response = requests.post(url, json=json_data, headers=header)
        response_json = json.loads(response.text.encode('utf8'))
        url_signed = response_json.get('signedUrl', '')
    except Exception as e:
        print('Error in getting signed url')
        logging.error('Failed to fetch signed url: ' + str(e))
        pass
    return url_signed


def upload_file(url_api, headers, json_data):
    '''
    Purpose: This function upload the scan file to our plateform
    :param url_api: Its the endpoint to hit for getting the signed url
    :param headers: Header object to hit the above endpoint
    :param json_data: Metadata of the scan
    :return: flag, 0 or 1 to indicate the success or failure
    '''
    try:
        file_name = json_data.get('fileName', '')
        json_data['fileName'] = json_data['fileName'].split('/')[-1]
        json_data['fileName'] = json_data['fileName'].split('\\')[-1]
        url_signed = get_signed_url(url_api, headers, json_data)
        ##print(url_signed)
        if not url_signed:
            print('Signed Url not generated.')
            logging.error('Signed Url not generated.')
            return 0

        contents = ''
        with open(file_name, 'rb') as f:
            contents = f.read()
        requests.put(url_signed, contents)
    except Exception as e:
        print('Error in uploading file.')
        logging.error('Failed to upload file: ' + str(e))
        return 0
    return 1

def main():
    '''
    Purpose: This function initiates the uploading of the scan file
    :return: flag, 0 or 1 to indicate the success or failure
    '''

    global folder_name, file_extension
    try:
        if '/' not in folder_name[-1]:
            folder_name = folder_name + '/'

        latest_file = get_latest_file(folder_name, file_extension)

        if latest_file:
            print('\nLatest file identified for scan : ' + str(latest_file))
            data_json['fileName'] = latest_file

            import_flag = upload_file(url_upload, headers, data_json)
            if import_flag:
                print('\nFile upload Successful.\n')
            else:
                print('\nFile upload failed.\n')

    except Exception as e:
        print('Error in processing latest file')
        logging.error('Error in processing latest file: ' + str(e))

    logging.info('Finished at: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    return 1


if __name__ == '__main__':

    ## Initiate the upload of the scan file.
    main()
