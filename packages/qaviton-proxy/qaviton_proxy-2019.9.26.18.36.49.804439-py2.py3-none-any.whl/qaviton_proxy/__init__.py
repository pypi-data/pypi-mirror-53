import requests
from flask import request, Response


excluded_headers = [
    'content-encoding',
    'content-length',
    'transfer-encoding',
    'connection']


def request_headers():
    return {key: value for (key, value) in request.headers if key != 'Host'}


def proxy_request(url):
    return requests.request(
        method=request.method,
        url=url,
        headers=request_headers(),
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        verify=False)


def proxy_new_headers(response):
    return [
        (name, value) if (name.lower() != 'location')
        else (name, request.host_url)
        for (name, value) in response.raw.headers.items()
        if name.lower() not in excluded_headers]


def proxy(url):
    response = proxy_request(url)
    headers = proxy_new_headers(response)
    return Response(
        response.content,
        response.status_code,
        headers
    )
