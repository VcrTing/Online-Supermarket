import json
import requests

class YunPian(object):
    def __init__(self, apikey):
        self.apikey = apikey
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, phone):
        params = {
            'apikey': self.apikey,
            'mobile': phone,
            'text': '欢迎使用{web_name}，您的手机验证码是{code}。本条信息无需回复'.format(web_name='VcrT在线超市', code=code)
        }
        """
        response = requests.post(self.single_send_url, data=params)
        re_dict = json.loads(response.text)
        print('re_dict =', re_dict)
        return re_dict
        """
        return {
            'code': 1,
            'msg': '发送成功',
            'mobile': '13576639986',
            'sid': '199828',
            'count': 1,
            'unit': 'RMB',
            'fee': 0.05
        }

if __name__ == '__main__':
    yp = YunPian('')
    yp.send_sms('2017', '13576639986')