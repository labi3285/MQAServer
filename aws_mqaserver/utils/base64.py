
import base64

def stringToBase64(s):
    strEncode = base64.b64encode(s.encode('utf8'))
    return str(strEncode, encoding='utf8')

def base64ToString(s):
    strDecode = base64.b64decode(bytes(s, encoding='utf8'))
    return str(strDecode, encoding='utf8')