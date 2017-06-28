#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import requeststudy

class RequestTestSuite(unittest.TestCase):
    """test case"""

    def test_invalid_url(self):
        self.assertRaises(ValueError, requeststudy.get, 'hisdfsd')

    def test_HTTP_200_OK_GET(self):
        r = requeststudy.get("http://www.baidu.com")
        self.assertEqual(r.status_code, 200)

    def test_HTTPS_200_OK_GET(self):
        r = requeststudy.get("https://www.baidu.com")
        self.assertEqual(r.status_code, 200)

    def test_AUTH_HTTPS_200_OK_GET(self):
        auth = requeststudy.AuthObject('requeststest', 'requeststest')
        url = 'https://convore.com/api/account/verify.json'
        r = requeststudy.get(url, auth=auth)

        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
