# 小米帐号开放平台OAuth python SDK使用说明

------
### 小米OAuth简介
http://dev.xiaomi.com/docs/passport/oauth2/

### 小米帐号开放平台文档
http://dev.xiaomi.com/docs/passport/user_guide/

### python SDK说明
> * XMHttpClient.py -- 基础Http请求封装
> * XMOAuthClient.py -- 针对OAuth授权流程相关http请求封装
> * XMApiClient.py -- 针对api请求相关http请求封装

### DEMO
#### 1.  获取授权URL DEMO
```PHP
按照稳定说明构造授权url:https://account.xiaomi.com/oauth2/authorize?client_id=xxx&response_type=code&redirect_uri=xxxx
```
复制授权url到浏览器, 输入用户名密码, 浏览器跳转到http://xiaomi.com?code=code-value
复制code-value作为步骤2的输入
#### 2.  获取accessToken DEMO
```php
oauthClient = XMOAuthClient(clientId, clientSecret, 'http://xiaomi.com')
code = 'code-value'
accessToken=oauthClient.getAccessTokenByAuthorizationCode(code)
```
AccessToken包括如下信息:
```php
String accessTokenId;
String refreshToken;
String scope;
long expiresIn;
String tokenType;
String macKey;
String macAlgorithm;
```  
#### 3.  通过refreshToken 换取 accessToken DEMO
```java
oauthClient = XMOAuthClient(clientId, clientSecret, 'http://xiaomi.com')
refreshToken = 'refreshToken' //第二步返回结果
accessToken=oauthClient.getAccessTokenByRefreshToken(code)
```
#### 3.  访问open api DEMO(以获取userprofile为例)
```java
macKey = 'macKey'
xu = XMUtils();
nonce = xu.getNonce()
method = 'GET'
host = 'open.account.xiaomi.com'
path = '/user/profile'
params = {'clientId' : clientId, 'token' : token} 
sign = xu.buildSignature(nonce, method, host, path, params, macKey)

headers = xu.buildMacRequestHead(token, nonce, sign)
apiClient = XMApiClient(clientId, token)
apiClient.callApi(path, params, headers, method)

//callApiSelfSign 会自己完成签名和header添加, 相当于上面的代码
apiClient.callApiSelfSign(path, params, macKey, method);
```
