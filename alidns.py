#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import hashlib
import hmac
import uuid
import base64
import json
import time

if sys.version_info < (3,):
    # python 2.x
    from httplib import HTTPSConnection
    import urllib
else:
    # python 3.x
    from http.client import HTTPSConnection
    import urllib.parse as urllib


__author__ = 'wafer lin'


class AliyunDNS(object):
    """
    Implementation of Aliyun Resolver API
    """

    def __init__(self, access_id, access_key):
        self.__url = "alidns.aliyuncs.com"
        self.__access_id = access_id
        self.__hash_key = access_key + '&'
        self.__method = "POST"
        self.__proxy = None

    def __signature(self, params):
        """
        计算签名,返回签名后的查询参数
        """
        params.update({
            'Format': 'json',
            'Version': '2015-01-09',
            'AccessKeyId': self.__access_id,
            'Timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': uuid.uuid4(),
            'SignatureVersion': "1.0",
        })
        query = urllib.urlencode(sorted(params.items()))
        sign = self.__method + "&" + \
            urllib.quote_plus("/") + "&" + urllib.quote(query, safe='')
        sign = hmac.new((self.__hash_key).encode('utf-8'),
                        sign.encode('utf-8'), hashlib.sha1).digest()
        sign = base64.b64encode(sign).strip()
        params["Signature"] = sign
        # sign.decode('utf-8').encode("base64").strip()
        return params

    def __request(self, param=None, **params):
        """
        发送请求数据
        """
        if param:
            params.update(param)
        params = self.__signature(params)
        if self.__proxy:
            conn = HTTPSConnection(self.__proxy)
            conn.set_tunnel(self.__url, 443)
        else:
            conn = HTTPSConnection(self.__url)
        conn.request(self.__method, '/', urllib.urlencode(params),
                     {"Content-type": "application/x-www-form-urlencoded"})
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if response.status < 200 or response.status >= 300:
            raise Exception(data)
        else:
            data = json.loads(data.decode('utf8'))
            return data

    def __get_domain_parms(self, domain):
        """
            切割域名获取主域名和子域名
            https://help.aliyun.com/document_detail/29755.html
        """
        data = self.__request(Action="GetMainDomainName", InputString=domain)
        sub, main = data.get('RR'), data.get('DomainName')
        rr = "_acme-challenge"
        if sub != "@":
            rr += "." + sub
        return rr, main

    def addDomainRecord(self, domain, value):
        """
        添加Domain记录
        """
        sub, main = self.__get_domain_parms(domain)
        data = self.__request(Action="AddDomainRecord", DomainName=main, RR=sub,
                              Type="TXT", Value=value)
        return data

    def delDomainRecord(self, domain):
        """
        添加Domain记录
        """
        sub, main = self.__get_domain_parms(domain)
        data = self.__request(Action="DeleteSubDomainRecords", DomainName=main, RR=sub,
                              Type="TXT")
        return data


if __name__ == '__main__':
    import os
    domain = os.environ['CERTBOT_DOMAIN']
    value = os.environ['CERTBOT_VALIDATION']
    access_id = os.environ['ALI_ID']
    access_key = os.environ['ALI_KEY']
    aliyunDns = AliyunDNS(access_id,
                          access_key)
    if os.environ.get("CERTBOT_AUTH_OUTPUT"):
        # manual clean hook
        aliyunDn
        s.delDomainRecord(domain)
        print('clean alidns auth recoard.')
    else:
        # manual auth hook
        aliyunDns.addDomainRecord(domain, value)
        print("waiting 120s...")
        time.sleep(120)
