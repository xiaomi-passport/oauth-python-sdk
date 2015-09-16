#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python client SDK for xiaomi Open API
'''

from XMHttpClient import XMHttpClient
from XMUtils import XMUtils
from urlparse import urlparse
import xiaomi_conf

class XMApiClient(XMHttpClient):
    
    def __init__(self, clientId, accessToken):
        XMHttpClient.__init__(self, xiaomi_conf.API_URL)
        self.clientId = clientId
        self.accessToken = accessToken
        self.xmUtils = XMUtils()
        self.host = urlparse(xiaomi_conf.API_URL).hostname
        
    def callApi(self, path, params, headers={}, method='GET'):
        if not self.url:
            raise Exception("open api url error,", self.url)
        res = self.request(path, method, params, headers);
        jsonObject = self.safeJsonLoad(res.read())
        return  jsonObject
    
    def callApiSelfSign(self, path, params, macKey, method='GET'):
        if params and not params.has_key('clientId') :
            params['clientId'] = self.clientId
        if params and not params.has_key('token') :
            params['token'] = self.accessToken
        
        nonce = self.xmUtils.getNonce()
        sign = self.xmUtils.buildSignature(nonce, method, self.host, path, params, macKey)
        headers = self.xmUtils.buildMacRequestHead(self.accessToken, nonce, sign)
        return self.callApi(path, params, headers, method);
