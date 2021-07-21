# coding=utf8
import base64
import os

def check(new_ss=''):
    if new_ss!='':
        new_t_ss = base64.b64decode(new_ss[5::]).decode().split(':')
        new_host = new_t_ss[1].split('@')[1]
        new_password = new_t_ss[1].split('@')[0]
        new_port = new_t_ss[2]
        with open('data.txt','r+') as f:
            result = base64.b64decode(f.read()).decode()
        result = sorted(list(set(result.split('\n'))))
        
        for ss in result:
            t_ss = base64.b64decode(ss[5::]).decode().split(':')
            host = t_ss[1].split('@')[1]
            password = t_ss[1].split('@')[0]
            port = t_ss[2]
            if new_host == host and new_port == port and new_password == password:
                return False
            elif new_host == host and new_port == port and new_password != password:
                result.remove(ss)
                result.append(new_ss)
                result = '\n'.join(sorted(list(set(result))))
                with open('data.txt','w+') as f:
                    f.write(result)
                return True
    return False
if __name__ == '__main__':
    result = check('ss://YWVzLTEyOC1nY206dXNmb3R3MmlXQG0zLm1vZ3U2Ni5jb206MjA2')
    if result:
        with open('data.txt','w+') as f:
            f.write(base64.b64decode(result).decode())