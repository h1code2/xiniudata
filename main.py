

import requests
import json
import execjs

with open("js_.js", 'r', encoding="utf-8") as file:
    js_code = file.read()

ctx = execjs.compile(js_code)

def parse_news(start,limit = 20):
    payload = ctx.call("get_payload", start,limit)
    sig = ctx.call("get_sig", payload)

    print(payload)
    print(sig)

    response = requests.post(
        'http://www.xiniudata.com/api2/service/x_service/person_news/list_news_info',
        data=json.dumps({"payload": payload, "sig": sig, "v": 1}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Origin": "http://www.xiniudata.com",
            "Referer": "http://www.xiniudata.com/info/news/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }
    )

    d = response.json().get("d")
    json_data = ctx.call("parse_data", d)
    json_data_list = json.loads(json_data).get("list")
    for i in json_data_list:
        i = json.loads(i)
        print(i.get("title"))

if __name__ == "__main__":
    for i in range(10,100,20):
        parse_news(i)