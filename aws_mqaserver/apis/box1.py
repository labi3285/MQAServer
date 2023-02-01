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

def test():
    oauth = OAuth2(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        store_tokens=_store_tokens,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://YOUR_REDIRECT_URL')


test()