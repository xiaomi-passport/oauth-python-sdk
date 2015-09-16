#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python client SDK for xiaomi Open API
'''

import urllib2
import urllib
import json
import types
from urlparse import urljoin

class XMHttpClient(object):
    def __init__(self, url):
        self.url = url
        
    def get(self, path, params, header={}):
        return self.request(path, 'GET', params, header)
 
 
    def post(self, path, params, header={}):
        return self.request(path, 'POST', params, header)
    
#     发送http请求
#         path： url的path
#         method： GET POST
#         headers： 请求的head部分
#         params： dictionary类型的参数
    def request(self, path, method, params=None, headers={}):
        if method != 'GET' and method != 'POST':
            raise Exception("input method name error, " + method)
        
        data = self.buildQueryString(params)
        httpUrl = '%s?%s' % (urljoin(self.url, path), data) if method == 'GET' else urljoin(self.url, path)
        postData = data if method == 'POST' else None
        req = urllib2.Request(httpUrl, headers=headers, data=postData)
        res = '[]'
        try:
            res = urllib2.urlopen(req)
        except urllib2.HTTPError, err:
            raise err
        return res
        
    def buildQueryString(self, params):
        if not params or type(params) is not types.DictType:
            return None
        return urllib.urlencode(params)
    
#     服务器返回的json可能有前缀
#     jsonStr： server返回的字符串
    def safeJsonLoad(self, jsonStr):
        start = jsonStr.find('{');
        start = jsonStr.find('[') if start == -1 else start;
        if start >= 0:
            ret = json.loads(jsonStr[start:])
            return ret
        return None;
