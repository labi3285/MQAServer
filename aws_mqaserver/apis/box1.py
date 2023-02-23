import keyring
from boxsdk import JWTAuth, Client
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

def test():
    auth = JWTAuth.from_settings_file('box_config.json')
    client = Client(auth)
    service_account = client.user().get()
    print(f'Service Account user ID is {service_account.id}')

    items = client.root_folder().get_items(fields=[
        'type',
        'id',
        'name',
    ])
    for e in items:
        print(e.name)

    # oauth = OAuth2(
    #     client_id=CLIENT_ID,
    #     client_secret=CLIENT_SECRET,
    #     store_tokens=_store_tokens,
    # )
    # auth_url, csrf_token = oauth.get_authorization_url('http://YOUR_REDIRECT_URL')


test()