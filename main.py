#coding=utf-8
from pyDes import des, PAD_PKCS5, ECB
import os
import sys
import base64
import requests
import time
import json
import random
import net

dictKey = '0123456789abcdefghijklmnopqrstuvwxyz'

def getRandomIMEI():
    return ''.join(random.sample(list(dictKey),16))

def getSS(url,KEY1,KEY2):
    v='0.96'
    imei = 'di:{}'.format(getRandomIMEI())
    id_ = 6 #小于6的是vip节点
    #user = random.randint(2800000,2899999)
    cid = random.randint(0,20) #节点
    headers = {}
    postdata = {}
    postdata['v'] = v
    postdata['imei'] = imei
    postdata['id'] = id_
    postdata['user'] = id_
    postdata['cid'] = cid
    headers['User-Agent'] = 'okhttp/4.2.2'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    response = requests.post(url,data=postdata,headers=headers).text
    raw_data = base64.b64decode(response)
    des_obj = des(KEY2, ECB, KEY2, padmode=PAD_PKCS5)
    data = json.loads(des_obj.decrypt(raw_data).decode())
    #print('ret:{0}\nlocation:{1}\nping:{2}'.format(data['ret'],data['location'],data['ping']))
    link = base64.b64decode(data['link'])
    desLink = des(KEY1, ECB, KEY2, padmode=PAD_PKCS5)
    return desLink.decrypt(link).decode()

if __name__ == "__main__":
    if len(sys.argv) > 0:
        for i in range(5):
            link = getSS(sys.argv[1],sys.argv[2],sys.argv[3])
            if net.check(link):
                with open('latest.txt','w') as f:
                    f.write(base64.b64encode(link.encode()).decode())
            for file in [x for x in os.listdir() if 'subscribe' in x]:
                os.remove(file)
            with open(f'subscribe_{time.strftime("%Y_%m_%d", time.localtime(time.time()))}.txt','w') as f:
                f.write(base64.b64encode(link.encode()).decode())
