#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python client SDK for xiaomi Open API
'''

import random
import sys
import time
import hmac, hashlib
from urllib import quote

class XMUtils():
    '''
     获取一个随机字符串
     获取随机nonce值 : 格式为  随机数:分钟数
    '''
    def getNonce(self):
        r = random.randint(-sys.maxint, sys.maxint)
        m = (int)(time.time() / 60)
        return '%d:%d' % (r, m)
    
    '''
    构造mac type签名串
    '''
    def getSignString(self, nonce, method, host, path, params):
        if nonce == None or nonce.index(':') == -1:
            raise Exception("input nonce error, " + nonce);
        if (method != 'GET' and method != 'POST') or not host:
            raise Exception("input param error");
        
        sign = []
        
        sign.append(nonce)
        sign.append(method)
        sign.append(host)
        path = path if path else "";
        sign.append(path)
        
        paramsKeys = params.keys()
        paramsKeys.sort()
        items = []
        for key in paramsKeys:
            items.append("%s=%s" % (key, params.get(key)))
            
        if items :
            sign.append('&'.join(items))
        else:
            sign.append('')
        
        return '\n'.join(sign) + '\n'
     
    '''
     mac type签名算法
    '''
    def buildSignature(self, nonce, method, host, path, params, secret):
        signString = self.getSignString(nonce, method, host, path, params)
        h = hmac.new(secret, signString, hashlib.sha1)
        s = h.digest()
        signature = s.encode('base64').strip()
        return signature

    '''
     获取mac type access token请求api的头部信息
    '''    
    def buildMacRequestHead(self, accessToken, nonce, sign):
        macHeader = 'MAC access_token="%s", nonce="%s",mac="%s"' % (quote(accessToken), nonce, quote(sign))
        header = {}
        header['Authorization'] = macHeader
        return header
        
        
