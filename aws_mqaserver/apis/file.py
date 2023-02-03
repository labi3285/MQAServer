import sys, os
from django.conf import settings
from django.http import FileResponse

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import ids

def download_file(request):
    filePath = request.GET.get("filePath")
    if filePath == None or filePath == '':
        return response.ResponseError('filePath Not Exist')
    path = settings.BASE_DIR
    path = os.path.join(path, 'aws_mqaserver/' + filePath)
    fileName = os.path.basename(filePath)
    file = open(os.path.abspath(path), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + fileName + '"'
    return response
