import requests
import json
import execjs

word = 'shit'

with open('jjss.js', 'r') as f:
    ctx = execjs.compile(f.read())
sign = ctx.call('e', word)

headers = {
    'cookie': 'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22pt%22%2C%22text%22%3A%22%u8461%u8404%u7259%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1583329992,1583330087,1583330582,1583396309; BAIDUID=DC75ABD95EB686EECD1F7A77B2D1EA67:FG=1; yjs_js_security_passport=52fd5c112066844d9f99f9dba976be5ad0b97659_1583397722_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1583397726; __yjsv5_shitong=1.0_7_9890d05d7c639b55b08c596576ddef114bcf_300_1583397731225_123.54.158.14_593c06da',
    'origin': 'https://fanyi.baidu.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'referer': 'https://fanyi.baidu.com/?aldtype=16047',
    'authority': 'fanyi.baidu.com',
    'x-requested-with': 'XMLHttpRequest',
}

params = (
    ('from', 'en'),
    ('to', 'zh'),
)

data = {
  'from': 'en',
  'to': 'zh',
  'query': word,
  'simple_means_flag': '3',
  'sign': sign,
  'token': '95c1b8910af22f5a8cd40d29e11955bc',
  'domain': 'common'
}

response = requests.post('https://fanyi.baidu.com/v2transapi', headers=headers, data=data)
print(json.loads(response.text))
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://fanyi.baidu.com/v2transapi?from=en&to=zh', headers=headers, data=data)
