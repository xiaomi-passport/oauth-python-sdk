#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'xiaomi passport (xiaomi-account-dev@xiaomi.com)'

'''
Python client SDK for xiaomi Open API
'''

from XMHttpClient import XMHttpClient
import xiaomi_conf
from urlparse import urljoin

class XMOAuthClient(XMHttpClient):
    
    OAUTH2_PATH = {'authorize':'/oauth2/authorize', 'token':'/oauth2/token'}
    
    def __init__(self, clientId, clientSecret, redirectUri):
        XMHttpClient.__init__(self, xiaomi_conf.OAUTH2_URL)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.redirectUri = redirectUri
        
    
    def getAuthorizeEndpoint(self):
        if not self.url:
            raise Exception("oauth url error", self.url)
        
        return urljoin(self.url, self.OAUTH2_PATH['authorize'])
    
    def getTokenEndpoint(self):
        if not self.url:
            raise Exception("oauth url error", self.url)
        
        return urljoin(self.url, self.OAUTH2_PATH['token'])
    

    def getAuthorizeUrl(self, responseType='code', display='',state='', scope=[]):
        params = {}
        params['client_id'] = self.clientId
        params['response_type'] = responseType
        params['redirect_uri'] = self.redirectUri
        
        if display:
            params['display'] = display
        if scope:
            params['scope'] = ' '.join(scope).strip();
        if state:
            params['state'] = state
        
        return self.getAuthorizeEndpoint() + '?' + self.buildQueryString(params)
        
    
    def getAccessTokenByAuthorizationCode(self, code):
        # Get access token  by authorization code.
        params = {}
        params['client_id'] = self.clientId
        params['client_secret'] = self.clientSecret
        params['redirect_uri'] = self.redirectUri
        params['grant_type'] = 'authorization_code'
        params['code'] = code
        params['token_type'] = 'mac'
        
        return self.getAccessToken(params);
        
    def getAccessTokenByRefreshToken(self, refreshToken):
        # Get access token  by refresh token.
        params = {}
        params['client_id'] = self.clientId
        params['client_secret'] = self.clientSecret
        params['redirect_uri'] = self.redirectUri
        params['grant_type'] = 'refresh_token'
        params['refresh_token'] = refreshToken
        params['token_type'] = 'mac'
        
        return self.getAccessToken(params);
           
    def getAccessToken(self, params):
        res = XMHttpClient.get(self, self.OAUTH2_PATH['token'], params)
        jsonObject = XMHttpClient.safeJsonLoad(self, res.read())
        return jsonObject
        
