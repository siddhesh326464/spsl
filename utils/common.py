from requests import request
from rest_framework.response import Response
from rest_framework import status
from api.messages import messages
from django.http import HttpResponseNotFound
from django.template.loader import get_template

def error_response(Error):
    return Response(Error["error"], Error["status"])

def dispatch_response(status_code, status_res=None):
    if status_code == 4000:
        return Response([], status=status.HTTP_200_OK)
      
    if status_code == 4001:
        return Response([], status=status.HTTP_201_CREATED)

    if status_code == 6002:
        return Response([], status=status.HTTP_404_NOT_FOUND)

    if isinstance(status_code, dict) or isinstance(status_code, list):
        data_dict = {
            'status_code': status_res or status.HTTP_200_OK,
            'msg': "",
            'response': status_code if isinstance(status_code, list) else status_code
        }
        
        return Response(data_dict, status=status_res or status.HTTP_200_OK)

    return error_response(messages[status_code])

# extract requested args from provided request

def extract_from_request(request, *args):
    values = []
    source = request.data

    if len(request.data) == 0:
        source = request.query_params

    for var in args:
        value = source.get(var, None)
        if value:
            value = value.strip()
        values.append(value)

    if len(values) == 1:
        return values[0]
    else:
        return values
    
def makePostCall(url,payload,token=None):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("POST", url=url, headers=headers, data=payload)
    return response


def makeJobPutCall(url,payload,token=None):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("PUT", url=url, headers=headers, data=payload)
    return response

def makePutCall(url,payload,files,token=None):
    headers = {
        'Accept': 'application/json',
        
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("PUT", url=url, headers=headers, data=payload,files=files)
    return response

def makeGetCall(url,payload,token=None):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("GET", url=url, headers=headers, data=payload)
    return response

def set_cookies(response,token):
    response.set_cookie('refresh_token', token['refresh'].replace('Bearer','').strip())
    response.set_cookie('access_token', token['access'].replace('Bearer','').strip())
    return response

def get_cookies(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    return access_token,refresh_token

def sendmsg_post_call(url,payload,files,token=None):
    headers = {
        'Accept': 'application/json',    
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("POST", url=url, headers=headers, data=payload,files=files)
    return response

def campaign_post_api(url,payload,token=None):
    headers = {
        'Accept': 'application/json',    
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("POST", url=url, headers=headers, data=payload)
    return response


def logout_post_call(url,payload,token=None):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    if token:
        headers.update({
            'Authorization': token
        })
    response = request("POST",url=url,headers=headers,data=payload)
    return response

def deletefile_put_api(url,payload,token=None):
    headers = {
        'Accept': 'application/json',    
    }
    if token:
        headers.update({
            'Authorization' : token
        })

    response = request("PUT", url=url, headers=headers, data=payload)
    return response


class TemplateErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            template = get_template('common/404.html')
            response = HttpResponseNotFound(template.render())
        elif response.status_code == 500:
            template = get_template('common/500.html')
            response = HttpResponseNotFound(template.render())
        return response