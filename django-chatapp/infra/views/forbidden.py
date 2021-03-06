import time
from uuid import uuid4

from django.urls import resolve

from infra.utils.http_error import Forbidden
from infra.utils.loggers import log_request, log_response


def http_forbidden_view(request, *args, **kwargs):
    '''View handler for http 403 forbidden
    '''

    request_id = str(uuid4())
    request_epoch = time.time()*1000

    request_parameters = resolve(request.path_info)
    request.url_info = {
        'kwargs': request_parameters.kwargs,
        'url_name': request_parameters.url_name,
        'app_names': request_parameters.app_names,
        'app_name': request_parameters.app_name,
        'namespaces': request_parameters.namespaces,
        'namespace': request_parameters.namespace,
        'view_name': request_parameters.view_name
    }

    log_request(request_id, request, request_epoch, request_parameters.view_name)

    response = Forbidden().response

    log_response(request_id, request, request_epoch, response)

    return response
