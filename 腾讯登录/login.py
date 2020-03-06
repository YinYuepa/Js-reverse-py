import requests
import execjs
import random
import time



def get_check_params(qqMsg):

    '''
    :param qqMsg: 传递账号，访问 check url用于获取客户端返回字段
    :return: 将需要登录的参数返回
    '''

    checkUrl = '''https://ssl.ptlogin2.qq.com/check?
    regmaster=&pt_tea=2&pt_vcode=1&uin=%s&appid=522005705
    &js_ver=20021917&js_type=1&login_sig=&u1=
    https://mail.qq.com/cgi-bin/readtemplate?check=false&t=loginpage_new_jump&vt=
    passport&vm=wpt&ft=loginpage&target=&r=%.17f&pt_uistyle=25''' % (qqMsg['Account'], random.random())

    response = requests.get(checkUrl)
    paramsList = response.text.replace('ptui_checkVC', '')\
        .replace(')', '')\
        .replace("'", '')\
        .replace("(", '')\
        .split(',')
    params = {
        'verifycode': paramsList[1],
        'pt_verifysession_v1': paramsList[3],
        'ptdrvs': paramsList[5],
    }
    return params


def get_password(account, password, verifycode):

    '''
    :param account: 传递账号
    :param password: 传递密码
    :param verifycode: 传递服务器返回的验证码
    :return: 将加密后的密码返回
    '''
    with open('password.js', 'r', encoding='utf-8') as f:
        jsCode = f.read()
    p = execjs.compile(jsCode).call('$.Encryption.getEncryption', password, account, verifycode, '')
    return p


def login(sess, params):

    '''
    :param sess: 传递session，因为session中携带cookies
    :param params: 登录所需要的参数
    :return: 返回重定向链接
    '''

    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'accept': '*/*',
        'referer': 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?target=self&appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/readtemplate?check=false%26t=loginpage_new_jump%26vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input_for_xmail440503.css',
        'authority': 'ssl.ptlogin2.qq.com'
    }

    url = 'https://ssl.ptlogin2.qq.com/login?u=' + params['Account'] + '&verifycode=' + params['verifycode'] +\
          '&pt_vcode_v1=0&pt_verifysession_v1=' + params['pt_verifysession_v1'] +'&p=' + params['p'] +\
          '&pt_randsalt=2&u1=https%3A%2F%2Fmail.qq.com%2Fcgi-bin%2Freadtemplate%3Fcheck%3Dfalse%26t%3Dloginpage_new_jump%26vt%3Dpassport%26vm%3Dwpt%26ft%3Dloginpage%26target%3D%26account%3D' +\
          params['Account'] + '&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=8-48-' + str(int(round(time.time()*1000))) +\
          '&js_ver=20021917&js_type=1&login_sig=&pt_uistyle=25&aid=522005705&daid=4&ptdrvs=' + params['ptdrvs'].replace(' ','')
    response = sess.get(url, headers=headers)
    return response


def get_cookies(sess, account, ptsigx):

    '''
    :param sess: 永久会话
    :param account: 账号
    :param ptsigx: 检查登录的参数
    :return: 返回已经已经存入cookies的session
    '''

    headers = {
        'authority': 'ssl.ptlogin2.mail.qq.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'referer': 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?target=self&appid=522005705&daid=4&s_url=https://mail.qq.com/cgi-bin/readtemplate?check=false%26t=loginpage_new_jump%26vt=passport%26vm=wpt%26ft=loginpage%26target=&style=25&low_login=1&proxy_url=https://mail.qq.com/proxy.html&need_qr=0&hide_border=1&border_radius=0&self_regurl=http://zc.qq.com/chs/index.html?type=1&app_id=11005?t=regist&pt_feedback_link=http://support.qq.com/discuss/350_1.shtml&css=https://res.mail.qq.com/zh_CN/htmledition/style/ptlogin_input_for_xmail440503.css',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    params = [
        ['pttype', '1'],
        ['uin', account],
        ['service', 'login'],
        ['nodirect', '0'],
        ['ptsigx', ptsigx],
        ['s_url', 'https://mail.qq.com/cgi-bin/readtemplate?check=false&t=loginpage_new_jump&vt=passport&vm=wpt&ft=loginpage&target=&account=%s' % (account)],
        ['f_url', ''],
        ['ptlang', '2052'],
        ['ptredirect', '100'],
        ['aid', '522005705'],
        ['daid', '4'],
        ['j_later', '0'],
        ['low_login_hour', '0'],
        ['regmaster', '0'],
        ['pt_login_type', '1'],
        ['pt_aid', '0'],
        ['pt_aaid', '0'],
        ['pt_light', '0'],
        ['pt_3rd_aid', '0'],
    ]
    sess.get('https://ssl.ptlogin2.mail.qq.com/check_sig', headers=headers, params=params)
    url = "https://mail.qq.com/cgi-bin/login?vt=passport&vm=wpt&ft=loginpage&target="
    sess.get(url, headers=headers)
    return sess

if __name__ == '__main__':

    '''
    !!!warning!!!
    使用本脚本登录前请将邮箱独立密码关闭！
    '''

    qqMsg = {
        'Account': '账号', #此处输入自己的账号
        'Password': '密码', #此处输入自己的密码
    }
    params = get_check_params(qqMsg)#获取部分参数用于提交的字段
    params['p'] = get_password(qqMsg['Account'], qqMsg['Password'], params['verifycode'])#获取加密的密码
    params.update(qqMsg)#参数dir合并
    sess = requests.session()#创建一个永久会话
    response = login(sess, params)#提交各种参数并拿到重定向HTML文本
    url = 'http' + response.text.split('http')[1].split('aid=0')[0] + 'aid=0'#获取重定向链接
    ptsigx = url.split('ptsigx=')[1].split('&s')[0]#摘取重定向链接内的ptsigx，用于检查登录流程
    sess = get_cookies(sess, qqMsg['Account'], ptsigx)#正式登录并拿到已经存入cookies的session
    print('----------恭喜发财----------\n\n测试登录成功\ncookies已保存至sess\n'
          '将此脚本当做胶水传递sess\n可以使用sess进行其他操作\n\n-----------奥利给-----------')
