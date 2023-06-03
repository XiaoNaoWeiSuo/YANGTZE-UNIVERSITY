import requests
import json
from pyDes import des, ECB, PAD_PKCS5 
import binascii
def get_pwd(s):
        KEY = '51434574'
        secret_key = KEY
        k = des(secret_key, ECB, pad=None, padmode=PAD_PKCS5) 
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return binascii.b2a_hex(en).upper().decode('utf-8')
class LoginImage(object):
    def image(account):
        url=f"http://q2.qlogo.cn/headimg_dl?dst_uin=%s&spec=640" % (account)
        
        with open("data.json","r+") as word:
            dat=json.loads(word.read())
        with open("data.json","r+") as word:
            if account!="":
                dat["user"]["statu"]="200"
                response=requests.get(url)
                data=response.content
                with open("./image/profile.png","wb") as file:
                    file.write(data)
            else:
                dat["user"]["statu"]="404"
            word.write(json.dumps(dat))
        
    def dmkj(phone,password):
        headers = { 
        'standardUA': '{"channelName": "dmkj_Android", "countryCode": "CN", "createTime": 1604663529774, "device": "HUAWEI vmos","hardware": "vphw71", "modifyTime": 1604663529774, "operator": "%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8","screenResolution": "1080-2115", "startTime": 1605884705024, "sysVersion": "Android 25 7.1.2","system": "android", "uuid": "12:34:56:31:97:80", "version": "4.5.3"}', 
        'Content-Type': 'application/x-www-form-urlencoded', 
        'Content-Length': '309', 
        'Host': 'appdmkj.5idream.net', 
        'Connection': 'Keep-Alive', 
        'Accept-Encoding': 'gzip', 
        'User-Agent': 'okhttp/3.11.0', 
    }
        url = 'https://appdmkj.5idream.net/v2/login/phone'

        pwsd=get_pwd(password)
        data = { 
                'pwd': pwsd, 
                'account': phone, 
                'version': '4.5.3' 
            }
        response=requests.post(url=url,headers=headers,data=data).json()
        with open("data.json","r+") as word:
                dat=json.loads(word.read())
        try:
            if response["code"]=="100":
                dat["user"]["statu"]="100"
                dat["user"]["phone"]=response["data"]["phone"]
                dat["user"]["ID"]=response["data"]["studentId"]
                dat["user"]["email"]=response["data"]["email"]
                dat["user"]["school"]=response["data"]["collegeName"]
                dat["user"]["name"]=response["data"]["name"]
                dat["user"]["profile"]=response["data"]["avatar"]
                url=response["data"]["avatar"]
                response=requests.get(url)
                data=response.content
                with open("./image/profile.png","wb") as file:
                    file.write(data)
            else:
                dat["user"]["statu"]="404"
            with open("data.json","w+") as word:
                word.write(json.dumps(dat))
            
        except:
            print("密码错误")