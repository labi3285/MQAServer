import keyring
from boxsdk import OAuth2, Client
from boxsdk import DevelopmentClient
import json
import traceback

from aws_mqaserver.utils import value

import logging
logger = logging.getLogger('django')

CLIENT_ID = 'tm3afpiehvcf8tf2ovcq9hlb5psoap32'
CLIENT_SECRET = 'BS0ScxYVag7XdDB2gtGT2lhjUQl7gROI'
BOX_ACCOUNT = 'hou_yi+developer@apple.com'

DEV_TOKEN = 'z8aSvH5TLRwGa757JIQZW9Ofbd8epl0g'
ROOT_ID = '140229589156'

global_client = None
global_folder_id_dict = {}

def box_get_authorization(request):
    logger.info('>>>>>>>>>>>')
    logger.info(request)

def _read_tokens():
    """Reads authorisation tokens from keyring"""
    # Use keyring to read the tokens
    auth_token = keyring.get_password('Box_Auth', BOX_ACCOUNT)
    refresh_token = keyring.get_password('Box_Refresh', BOX_ACCOUNT)
    return auth_token, refresh_token

def _store_tokens(access_token, refresh_token):
    """Callback function when Box SDK refreshes tokens"""
    # Use keyring to store the tokens
    keyring.set_password('Box_Auth', BOX_ACCOUNT, access_token)
    keyring.set_password('Box_Refresh', BOX_ACCOUNT, refresh_token)
    print('store')

def _check_or_setup_box():
    global global_client
    if global_client != None:
        return
    oauth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=DEV_TOKEN,
        # access_token=access_token,
        # refresh_token=refresh_token,
        store_tokens=_store_tokens,
    )
    global_client = Client(oauth)
    current_user = global_client.user(user_id='me').get()
    print('[box] setup, user:', current_user.name)

def _create_folder(parent_id, folder_name):
    global global_client
    _check_or_setup_box()
    return global_client.folder(parent_id).create_subfolder(folder_name).id

def _get_folder_items(parent_id):
    global global_client
    _check_or_setup_box()
    return global_client.folder(folder_id=parent_id).get_items(fields=[
        'type',
        'id',
        'name',
    ])

# This method will auto create folder if folder not exsit.
# It will also cache folder ids in the first time when request for an folder id in box
# which prevent this system from frequency requests with box.
def _auto_get_folder_id(folder_path):
    global global_client
    _check_or_setup_box()
    global global_folder_id_dict
    id = value.safe_get_in_key(global_folder_id_dict, folder_path)
    if id != None:
        return id
    names = folder_path.split('/')
    next_id = global_client.root_folder().get().id
    next_parent_path = ''
    for name in names:
        if name != '':
            items = _get_folder_items(next_id)
            find = False
            for item in items:
                global_folder_id_dict[next_parent_path + '/' + item.name] = item.id
                if item.name == name:
                    next_id = item.id
                    find = True
            if not find:
                logger.info('[box] create folder ' + next_parent_path + '/' + item.name)
                next_id = _create_folder(next_id, name)
                global_folder_id_dict[next_parent_path + '/' + item.name] = next_id
            next_parent_path += '/' + name
    return next_id

def upload_file(folder_path, file_name, file_stream):
    global global_client
    _check_or_setup_box()
    folder_id = _auto_get_folder_id(folder_path)
    global_client.folder(folder_id).upload_stream(file_stream, file_name)
    logger.info('[box] file:' + file_name + ' uploaded to folder:' + folder_path)

def box_test(request):
    stream = open('/Users/labi3285/Desktop/BrittleStation.json', 'rb')
    name = 'BrittleStation.json'
    upload_file('/a/b/c', name, stream)








