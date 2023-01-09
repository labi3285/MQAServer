
import os
from django.conf import settings
from django.http import FileResponse

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import ids

def download_file(request):
    fileName = request.GET.get("fileName")
    if fileName == None or fileName == '':
        return response.ResponseError('fileName Not Exist')
    path = settings.BASE_DIR
    path = os.path.join(path, 'aws_mqaserver/files/' + fileName)
    file = open(os.path.abspath(path), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + fileName + '"'
    return response
