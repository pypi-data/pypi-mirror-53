#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-26 10:36:45
import logging
import requests
from baidu.exceptions import BaiduException
from baidu.session.memorystorage import MemoryStorage

logger = logging.getLogger(__name__)


class BaiduClient(object):
    """
    百度 API 操作类
    通过这个类可以操作百度 API。
    """

    def __init__(self, app_id, api_key, secret_key, access_token=None, session=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.app_id = app_id
        self.session = session or MemoryStorage()

    def fetch_access_token(self):
        """
        获取 access token
        详情请参考 https://ai.baidu.com/docs#/Auth/top
        :return: 返回一个
        """
        res = requests.post(
            url="https://aip.baidubce.com/oauth/2.0/token",
            headers={
                "Content-Type": "applicaiont/json; charset=UTF-8",
            },
            params={
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key,
            }
        )
        if res.status_code != 200:
            raise BaiduException(res.json())
        result = res.json()
        expires_in = result["expires_in"]
        self.session.set(
            self.access_token_key,
            result["access_token"],
            expires_in
        )
        return result

    @property
    def access_token_key(self):
        return "{}_access_token".format(self.app_id)

    @property
    def access_token(self):
        access_token = self.session.get(self.access_token_key)
        if access_token:
            return access_token
        self.fetch_access_token()
        return self.session.get(self.access_token_key)
