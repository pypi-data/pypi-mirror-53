#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-09-26 10:39:47


from baidu.exceptions import BaiduException
import requests
from urllib.parse import urljoin


class BaseBaiduAPI(object):
    base_url = "https://aip.baidubce.com/rest/2.0/"

    def __init__(self, client=None):
        self._client = client

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def session(self):
        return self._client.session


class TextCensor(BaseBaiduAPI):
    api_url = "antispam/v2/spam"
    name = "文本审核"

    def call(self, text):
        res = requests.post(
            url=urljoin(self.base_url, self.api_url),
            params={
                "access_token": self._client.access_token,
            },
            data={
                "content": text,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        if "error_code" in res.json():
            raise BaiduException(res.json())
        return res.json()

    def is_allowed(self, text):
        """
        检查一段文字是否符合社会主义核心价值观
        :return: 
            ("allowed", None)  # 符合
            ("rejected", detail)  # 违禁
            ("check", detail)  # 人工复审
        """
        RESULT = {
            0: "allowed",
            1: "rejected",
            2: "check",
        }
        result = self.call(text)
        return RESULT[result["result"]["spam"]], result["result"]
