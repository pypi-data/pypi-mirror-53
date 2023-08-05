import requests
"""
api参考微信企业号开发者文档:
  https://qydev.weixin.qq.com/wiki/index.php?title=OAuth%E9%AA%8C%E8%AF%81%E6%8E%A5%E5%8F%A3

"""

class Qiye_weixin_api():
    def __init__(self,corp_id,secret):
        #获取企业微信用户信息url
        self.huoqu_weixin_yonghu_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s'
        #获取企业微信token
        self.huoqu_qyweixin_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'
        #获取成员详情，包括手机号和邮箱
        self.huoqu_qiywein_chengyuan_xiangqing_url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserdetail?access_token=%s"

        self.corp_id = corp_id
        self.secret =secret

    def huoqu_access_token(self):
        """
        获取微信访问token
        :return: 返回token
        """
        r1 = requests.get(self.huoqu_qyweixin_token_url % (self.corp_id,self.secret))
        r2 = r1.json()
        print(r2)
        token = r2.get('access_token', False)
        if token:
            print("token获取成功 %s" % token)
            return token
        else:
            print("token获取失败")
            return False

    def __yonghuxinxi(self,token,code):
        r1 = requests.get(self.huoqu_weixin_yonghu_url % (token,code))
        r2 = r1.json()
        wx_id = r2.get('UserId', None)
        if wx_id:
            return r2
        else:
            return False
    def huoqu_weixin_id(self,code):
        token = self.huoqu_access_token()
        if token:
            r1 = self.__yonghuxinxi(token=token,code=code)
            r2 = r1.json()
            weixin_id = r2.get("UserId",None)
            if weixin_id:
                print("获取微信用户ID成功")
                return weixin_id
            else:
                print("获取微信用户ID失败")
                return False
        else:
            print("token获取失败")
            return False

    def huoqu_chengyuan_xiangqing(self,code):
        """
        获取用户详情，包括手机号和邮箱地址,但要在Url跳转的scope设置为手动授权
        :return:
        """
        token = self.huoqu_access_token()
        yonghu_xin= self.__yonghuxinxi(token=token,code=code)
        data = {"user_ticket":yonghu_xin["user_ticket"]}
        r1 = requests.post(url=self.huoqu_qiywein_chengyuan_xiangqing_url % token,data=data)
        return r1.json()


def test1():
    """
    测试方法
    """
    #传入 corp_id 和 secret
    qwa = Qiye_weixin_api(1, 2)
    #得到token
    qwa.huoqu_access_token()
    #得到weixinid,传入code
    qwa.huoqu_weixin_id(code=123)

if __name__ == '__main__':

    test1()
