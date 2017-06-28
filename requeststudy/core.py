# coding:utf-8
import urllib
import urllib2

__title__ = 'requests'
__version__ = '0.0.2'
__build__ = 0x000002
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'

AUTHOAUTHS = []


class _Request(urllib2.Request):
    ''''''

    def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None):
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)
        self.method = method

    def get_method(self):
        if self.method:
            return self.method
        return urllib2.Request.get_method(self)


class Request(object):
    """
    the class `Request` object. It's awesome.
    """
    _METHODS = ('GET', 'HEAD', 'PUT', 'POST', 'DELETE')

    def __init__(self):
        self.url = None
        self.headers = dict()
        self.method = None
        self.params = {}
        self.data = {}
        self.response = Response()
        self.auth = None
        self.sent = False

    def __setattr__(self, name, value):
        '''调用__setattr__  方法，对参数校验，通过后赋值'''
        if (name == 'method') and value:
            if not value in self._METHODS:
                raise InvalidMethod()

        object.__setattr__(self, name, value)

    def _checks(self):
        # TODO 检查
        if not self.url:
            raise URLRequired

    def _get_opener(self):
        '''为urllib2创建合适的开启对象'''
        if self.auth:
            authr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            authr.add_password(None, self.url, self.auth.username, self.auth.password)
            handler = urllib2.HTTPBasicAuthHandler(authr)
            opener = urllib2.build_opener(handler)

            return opener.open
        else:
            return urllib2.urlopen

    def send(self, anyway=False):
        '''send the request
        If True, request will be sent, even if it has already been sent.
        '''
        self._checks()

        success = False

        if self.method in ('GET', 'HEAD', 'DELETE'):
            if (not self.sent) or anyway:

                # url encode GET method if it's a dict
                if isinstance(self.params, dict):
                    params = urllib.urlencode(self.params)
                else:
                    params = self.params

                req = _Request(("%s?%s" % (self.url, params)), method=self.method)

                if self.headers:
                    req.headers = self.headers

                opener = self._get_opener()

                try:
                    resp = opener(req)

                    self.response.status_code = resp.code
                    self.response.headers = resp.info().dict
                    if self.method.lower() == 'get':
                        self.response.content = resp.read()

                    success = True
                except urllib2.HTTPError, why:
                    self.response.status_code = why.code


        elif self.method == 'PUT':
            if (not self.sent) or anyway:

                req = _Request(self.url, method='PUT')
                if self.headers:
                    req.headers = self.headers
                req.data = self.data

                try:
                    opener = self._get_opener()
                    resp = opener(req)

                    self.response.status_code = resp.code
                    self.response.headers = resp.info().dict
                    self.response.content = resp.read()

                    success = True

                except urllib2.HTTPError, why:
                    self.response.status_code = why.code


        elif self.method == 'POST':
            if (not self.sent) or anyway:

                req = _Request(self.url, method='POST')

                if self.headers:
                    req.headers = self.headers
                # TODO 这里对参数进行拼接处理
                if isinstance(self.data, dict):
                    req.data = urllib.urlencode(self.data)
                else:
                    req.data = self.data

                try:

                    # TODO 创建密码管理器
                    opener = self._get_opener()
                    resp = opener(req)

                    self.response.status_code = resp.code
                    self.response.headers = resp.info().dict
                    self.response.content = resp.read()

                    success = True

                except urllib2.HTTPError, why:
                    self.response.status_code = why.code

        elif self.method.lower() == 'delete':
            if (not self.sent) or anyway:
                pass
        else:
            raise InvalidMethod

        self.sent = True if success else False

        return self.sent


class Response(object):
    def __init__(self):
        self.content = None
        self.status_code = None
        self.headers = dict()


class AuthObject(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password


def get(url, params={}, headers={}, auth=None):
    r = Request()

    r.method = 'GET'
    r.url = url
    r.params = params
    r.headers = headers
    # TODO auth校验
    r.auth = _detect_auth(url, auth)

    r.send()
    return r.response


def post():
    pass


def put():
    pass


def delete():
    pass


def add_autoauth(url, authobject):
    '''
    在这里添加auth记录
    :param url:
    :param authobject:
    :return:
    '''
    global AUTHOAUTHS

    AUTHOAUTHS.append((url, authobject))


def _detect_auth(url, auth):
    '''
    检测auth
    :param url:
    :param auth:
    :return:
    '''
    return _get_autoauth(url) if not auth else auth


def _get_autoauth(url):
    '''
    校验是否有验证记录
    :param url:
    :return:
    '''
    for (autoauth_url, auth) in AUTHOAUTHS:
        if autoauth_url in url:
            return auth
    return None


class RequestException(Exception):
    ''''''


class AuthenticationError(RequestException):
    ''''''


class URLRequired(RequestException):
    ''''''


class InvalidMethod(Exception):
    """"""
