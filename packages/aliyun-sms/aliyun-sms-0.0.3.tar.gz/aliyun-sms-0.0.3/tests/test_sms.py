#!/usr/bin/python3
# @Time    : 2019-09-26
# @Author  : Kevin Kong (kfx2007@163.com)

import unittest
from aliyun_sms.aliyun_sms.sms import Sms


class TestSms(unittest.TestCase):

    def test_sign(self):
        # test = 'AccessKeyId=testId&Action=SendSms&Format=XML&OutId=123&PhoneNumbers=15300000001&RegionId=cn-hangzhou&SignName=阿里云短信测试专用&SignatureMethod=HMAC-SHA1&SignatureNonce=45e25e9b-0a6f-4070-8c85-2956eda1b466&SignatureVersion=1.0&TemplateCode=SMS_71390007&TemplateParam={"customer":"test"}&Timestamp=2017-07-12T02:42:19Z&Version=2017-05-25'
        # testencode = 'AccessKeyId=testId&Action=SendSms&Format=XML&OutId=123&PhoneNumbers=15300000001&RegionId=cn-hangzhou&SignName=%E9%98%BF%E9%87%8C%E4%BA%91%E7%9F%AD%E4%BF%A1%E6%B5%8B%E8%AF%95%E4%B8%93%E7%94%A8&SignatureMethod=HMAC-SHA1&SignatureNonce=45e25e9b-0a6f-4070-8c85-2956eda1b466&SignatureVersion=1.0&TemplateCode=SMS_71390007&TemplateParam=%7B%22customer%22%3A%22test%22%7D&Timestamp=2017-07-12T02%3A42%3A19Z&Version=2017-05-25'
        # testwithmethod = 'GET&%2F&AccessKeyId%3DtestId%26Action%3DSendSms%26Format%3DXML%26OutId%3D123%26PhoneNumbers%3D15300000001%26RegionId%3Dcn-hangzhou%26SignName%3D%25E9%2598%25BF%25E9%2587%258C%25E4%25BA%2591%25E7%259F%25AD%25E4%25BF%25A1%25E6%25B5%258B%25E8%25AF%2595%25E4%25B8%2593%25E7%2594%25A8%26SignatureMethod%3DHMAC-SHA1%26SignatureNonce%3D45e25e9b-0a6f-4070-8c85-2956eda1b466%26SignatureVersion%3D1.0%26TemplateCode%3DSMS_71390007%26TemplateParam%3D%257B%2522customer%2522%253A%2522test%2522%257D%26Timestamp%3D2017-07-12T02%253A42%253A19Z%26Version%3D2017-05-25'
        # sigin = "zJDF+Lrzhj/ThnlvIToysFRq6t4="
        # sms = Sms("testId", "testSecret")
        # s = sms.sendSms("15300000001", "阿里云短信测试专用", "SMS_71390007", {
        #                 "customer": "test"}, outid="123", signature="45e25e9b-0a6f-4070-8c85-2956eda1b466", timestamp="2017-07-12T02:42:19Z")
        # self.assertEqual(s, sigin)

        sms = Sms("LTAIwim6Dd4SuXSr", "DyONSbw0l85sHAHZpQQO1Q1MF8I4tJ")
        s = sms.sendSms("18561363632", "灰缇米兰", "SMS_174987631", {
                        "expressno": "1234", "message": "MX01254"})

if __name__ == "__main__":
    unittest.main()
