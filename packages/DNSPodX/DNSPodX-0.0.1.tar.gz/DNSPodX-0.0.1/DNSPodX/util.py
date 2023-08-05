# coding=utf-8
import json
import DNSPodX
import requests


class DNSPodApiException(Exception):
    pass


def http_post(method, login_token, params):
    url = "https://dnsapi.cn/" + method
    params['lang'] = 'cn'
    params['format'] = 'json'
    params['login_token'] = login_token
    params['error_on_empty'] = 'no'
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/json",
        "User-Agent": "DNSPodX/0.01 (me@wolfbolin.com; DNSPod.CN API v4.6)"
    }
    proxies = {'http': DNSPodX.http_proxy, 'https': DNSPodX.https_proxy}
    response = requests.post(url, data=params, headers=headers, proxies=proxies)
    data = json.loads(response.text)
    if data.get("status", {}).get("code") == "1":
        return data
    else:
        raise DNSPodApiException(data)


def remove_none(data):
    result = {}
    for key in data:
        if data[key] is not None:
            result[key] = data[key]
    return data
