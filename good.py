import requests
import json
from urllib.parse import quote_plus
import webbrowser

class Connect(object):
    def __init__(self,cid,tid):
        url="https://clown.pxtl.com.cn/ajax.php"
        resp=requests.get(url=url,headers=self.Headers())
        doc=resp.headers["Set-Cookie"]
        self.mysid=self.load("mysid=",doc,";")
        self.PHPSESSID=self.load("PHPSESSID=",doc,";")
        print("mysid= ",self.mysid," PHPSESSID= ",self.PHPSESSID)
        #self.user_token="845cE01JDolEDduhYAGPPDifUn%2Fy8rRpsmVi1%2FVjT%2B0bgc3gSy7YQ8O1Pflc5LG15JgvrL6IvLmNJr5u8KgppYeL2A"
        self.Hm_lvt="Hm_lvt_86e34d0538d074686ffd6135e40bcc5d=1685554595,1685560097,1685611684,1685628893"
        self.Hm_lpvt="Hm_lpvt_86e34d0538d074686ffd6135e40bcc5d=1685642104"

        #获取sec_defend验证令牌
        self.url_den = "https://clown.pxtl.com.cn/?cid=%s&tid=%s"%(cid,tid)
        headers_den=self.Headers()
        headers_den["sec-fetch-mode"]="cors"
        headers_den["sec-fetch-dest"]="empty"
        headers_den["cache-control"]="max-age=0"
        headers_den["sec-fetch-user"]="?1"
        call=requests.get(url=self.url_den,headers=headers_den)
        self.sec_defend=self.load("setCookie('sec_defend',",call.text,";")
        self.sec_defend=self.sec_defend[:-1]#sec_defend值最后一句多出一个“)”，故写此
        self.sec_defend=self.translate(self.sec_defend)
        self.cookie=f"mysid=%s; op=false; PHPSESSID=%s; %s; sec_defend=%s; counter=6; %s"%(self.mysid,self.PHPSESSID,self.Hm_lvt,self.sec_defend,self.Hm_lpvt)
        with open("cookie","w+") as file:
            file.write(self.cookie)
        headers=self.Headers()
        headers["cookie"]=self.cookie
        headers["sec-fetch-user"]="?1"
        #发送GET请求，提取hashsalt
        response=requests.get(url=self.url_den,headers=headers)
        self.hashsalt=self.load("hashsalt=",response.text,";")
        self.hashsalt=self.translate(self.hashsalt)
    def Headers(self):
        with open("headers.json","r") as file:
            return json.load(file)

    def translate(self,code):
        code = quote_plus(code)
        HashSalt_API=f"http://iyuca.cn:8080/api/main/code?code=%s"%(code)
        response=requests.get(HashSalt_API).json()
        return response["data"]
    def load(self,name,source,tip):
        print(name)
        doc=source.replace(" ","")
        position = doc.find(name)
        rule=position+len(name)
        state=True
        value=""
        while state==True:
            value+=doc[rule]
            rule+=1
            if doc[rule]==tip:
                state=False
        return value
    def getshuoshuo(self,account):
        headers=self.Headers()
        headers["cookie"]=self.cookie
        headers["sec-fetch-mode"]="cors"
        headers["sec-fetch-dest"]="empty"
        headers["referer"]=self.url_den
        headers["x-requested-with"]="XMLHttpRequest"
        act="getshuoshuo"
        page="1"
        Url=f"https://clown.pxtl.com.cn/ajax.php?act=%s&uin=%s&page=%s&hashsalt=%s"%(act,account,page,self.hashsalt)
        response=requests.get(url=Url,headers=headers).json()
        with open(f"%s.json"%(account),"w+") as file:
            file.write(json.dumps(response))
    def pay(self,tid,account,shuoID,value3,num,way):
        pay_url="https://clown.pxtl.com.cn/ajax.php?act=pay"
        pay_data={
            "tid":tid,
            "inputvalue":account,
            "inputvalue2":shuoID,
            "inputvalue3":value3,
            "num":num,
            "hashsalt":self.hashsalt
        }
        if shuoID==None:
            pay_data.pop("inputvalue2")
        if value3==None:
            pay_data.pop("inputvalue3")
        header=self.Headers()
        header.pop("upgrade-insecure-requests")
        header["cookie"]=self.cookie
        header["content-type"]="application/x-www-form-urlencoded; charset=UTF-8"
        header["content-length"]=str(len(pay_data))
        header["x-requests-with"]="XMLHttpRequest"
        header["origin"]="https://clown.pxtl.com.cn"
        header["sec-fetch-mode"]="cors"
        header["sec-fetch-dest"]="empty"
        header["accept"]="application/json, text/javascript, */*; q=0.01"
        header["referer"]=self.url_den
        #提交订单，获取订单号
        response=requests.post(url=pay_url,headers=header,data=pay_data).json()
        self.trade=response["trade_no"]
        self.need=response["need"]
        print("订单号：",self.trade)
        iss_url=f"https://clown.pxtl.com.cn/other/submit.php?type=%s&orderid=%s"%(way,self.trade)
        iss_headers=self.Headers()
        iss_headers["cookie"]=self.cookie
        iss_headers["referer"]=self.url_den

        iss_respon=requests.get(url=iss_url,headers=iss_headers)
        iss_respon=iss_respon.text
        money=self.load("\'money\'value=\'",iss_respon,"\'")
        name=self.load("\'name\'value=\'",iss_respon,"\'")
        notify_url=self.load("\'notify_url\'value=\'",iss_respon,"\'")
        out_trade_no=self.load("\'out_trade_no\'value=\'",iss_respon,"\'")
        pid=self.load("\'pid\'value=\'",iss_respon,"\'")
        return_url=self.load("\'return_url\'value=\'",iss_respon,"\'")
        sitename=self.load("\'sitename\'value=\'",iss_respon,"\'")
        sign=self.load("\'sign\'value=\'",iss_respon,"\'")
        sign_type=self.load("\'sign_type\'value=\'",iss_respon,"\'")
        money_data={
            "money":money,
            "name":name,
            "notify_url":notify_url,
            "out_trade_no":out_trade_no,
            "pid":pid,
            "return_url":return_url,
            "sitename":sitename,
            "type":way,
            "sign":sign,
            "sign_type":sign_type,
        }
        money_header=self.Headers()
        money_header["content-length"]=str(len(money_data))
        money_header["cache-control"]="max-age=0"
        money_header["upgrade-insecure-requests"]="1"
        money_header["origin"]="https://clown.pxtl.com.cn"
        money_header["sec-fetch-site"]="cross-site"
        money_header["referer"]="https://clown.pxtl.com.cn/"
        if way=="qqpay":
            print("QQ支付")
            money_header["host"]="api.ccmyun.cc"
            money_response=requests.post(url="https://api.ccmyun.cc/submit.php",headers=money_header,data=money_data)
            address="https://api.ccmyun.cc/"+self.load("location.replace(\'",money_response.text,"\'")
            print(address)
        elif way=="alipay":
            print("支付宝")
            money_header["host"]="suv.kdeye.cn"
            money_response=requests.post(url="https://suv.kdeye.cn/submit.php",headers=money_header,data=money_data)
            address=self.load("location.replace(\'",money_response.text,"\'")
            print(address)
        webbrowser.open(address)
#Connect(33,5115).getshuoshuo(3517049357)
#Connect(33,5168).pay(5168,3517049357,"0deaa1d1f161766418340500",2,"alipay")#测试说说点赞通过
#Connect(92,3670).pay(3670,"https://v.douyin.com/UCBWtAR/",None,2,"qqpay")#抖音刷赞测试通过
Connect(32,1061).pay(1061,"3517049357",None,None,1,"qqpay")