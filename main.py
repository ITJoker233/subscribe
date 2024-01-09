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
from fake_useragent import UserAgent

dictKey = '0123456789abcdefghijklmnopqrstuvwxyz'
useragent = UserAgent()
http = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54',
    'Content-Type': 'application/x-www-form-urlencoded',
    'agentX': 'super-ok-http'
}
error_msg = ''
def getRandomIMEI():
    return 'di:'+''.join(random.sample(list(dictKey),16))

phone_imei = getRandomIMEI()

def getInfo(host,KEY1):
    url = f'{host}/api/user/getInfo'
    payload = {
        'a':random.randint(6,14),
        'b':getRandomIMEI(),
        'c':''.join(random.sample(list(dictKey),5)),
        'd':'fuxi',
        'v':'0.97',
        'imei':phone_imei,
    }
    response = http.post(url,data=payload,headers=headers).text
    raw_data = base64.b64decode(response)
    des_obj = des(KEY1, ECB, KEY1, padmode=PAD_PKCS5)
    data = json.loads(des_obj.decrypt(raw_data).decode())
    print(data)

def getSS(host,KEY1,KEY2,cid):
    url = f'{host}/api/user/getserver'
    payload = {
        'v':0.97,
        'imei':phone_imei,
        'id':0,
        'user':int(time.time()*1000)/10000000,
        'cid':cid,
    }
    headers['User-Agent'] = useragent.random #'okhttp/4.2.2'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['x-forwarded-for'] = ( str(random.randint(0, 256))+'.'+str(random.randint(0, 256))+'.'+str(random.randint(0, 256))+'.'+str(random.randint(0, 256)) )
    response = http.post(url,data=payload,headers=headers).text
    try:
        raw_data = base64.b64decode(response)
        des_obj = des(KEY1, ECB, KEY1, padmode=PAD_PKCS5)
        data = json.loads(des_obj.decrypt(raw_data).decode())
        if data['ret'] == 2:
            name = data['location']
            link = base64.b64decode(data['link'])
            desLink = des(KEY2, ECB, KEY2, padmode=PAD_PKCS5)
            return name,desLink.decrypt(link).decode()
        else:
            return '',None
    except Exception as e:
        print(e)
        error_msg+=e
        return '',None

if __name__ == "__main__":
    if len(sys.argv) > 0:
        result = {}
        url = sys.argv[1]
        key1 = sys.argv[2]
        key2 = sys.argv[3]
        for i in range(9):
            for j in range(10):
                name,link = getSS(url,key1,key2,2)
                print(f'{i}{j} Name:{name} Link:{link}')
                if link is not None and link != '':
                    result[name] = link
                time.sleep(0.5)
        print(len(result))
        print(result)
        for key in result:
            link = result[key]
            #if net.check(link):
            with open('latest.txt','w') as f:
                f.write(base64.b64encode(link.encode()).decode())
            for file in [x for x in os.listdir() if 'subscribe' in x]:
                os.remove(file)
            with open(f'subscribe_{time.strftime("%Y_%m_%d", time.localtime(time.time()))}.txt','w') as f:
                f.write(base64.b64encode(link.encode()).decode())
        if error_msg != '':
            with open('error.md','w') as f:
                f.write(error_msg)
