import requests
class Qiye_weixin_api():
    def __init__(self,corp_id,secret):
        #获取企业微信用户信息url
        self.huoqu_weixin_yonghu_url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s'
        #获取企业微信token
        self.huoqu_qyweixin_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'
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
