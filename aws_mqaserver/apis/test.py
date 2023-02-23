import sys, os
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from django.conf import settings
import datetime
import traceback

from aws_mqaserver.utils import value
from aws_mqaserver.utils import validator
from aws_mqaserver.utils import response
from aws_mqaserver.utils import token
from aws_mqaserver.utils import ids
from aws_mqaserver.utils import audit

from aws_mqaserver.models import User

import json

import logging
logger = logging.getLogger('django')

def test(request):
    params = json.loads(request.body.decode())
    text = validator.validate_not_empty(params, 'text')
    score = validator.validate_not_empty(params, 'score')
    result = audit.get_real_sample_size1(text, score)
    return response.ResponseData({
        'result': result,
    })
