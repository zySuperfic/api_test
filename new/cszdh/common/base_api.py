# coding:utf-8
import json

import requests

from new.cszdh.common.readexcel import ExcelUtil
from new.cszdh.common.writeexcel import copy_excel, Write_excel

# 打印登录返回token必填值
def login():
    url = "http://v4.demo.qiyebox.com/auth/oauth/token?username=yanzi&pCode=R5eGR5f0xc5sJ5VeZIBxtg%3D%3D&randomStr=75461594192181112&code=6666&grant_type=password&scope=server"
    headers = {
        'Content-Type': "application/json;charset=UTF-8",
        'Authorization':"Basic cGlnOnBpZw=="
    }
    r = requests.get(url=url, headers=headers)
    return r.json()['access_token']
# print("bearer "+login())


def send_requests(s, testdata):
    '''封装requests请求'''
    method = testdata["method"]
    url = "http://v4.demo.qiyebox.com" + testdata["url"]
    content = testdata["content"]
    input = testdata["input"]

    # print(url)
    # url = testdata["url"]
    # url后面的params参数
    try:
        params = eval(testdata["params"])
    except:
        params = None
    # 请求头部headers
    try:
        # headers = eval(testdata["headers"])
        headers = {
            'Content-Type': "application/json;charset=UTF-8",
            "Authorization": "Bearer " + login()
        }
        print("请求头部：%s" % headers)

    except:
        headers = None
    # post请求body类型
    type = testdata["type"]

    test_nub = testdata['id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)
    print("前置条件：%s" % content)
    print("输入数据：%s" % input)

    # post请求body内容
    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata = {}
 
    # 判断传data数据还是json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata
    if method == "post":
        # print("post请求body类型为：%s ,body内容为：%s" % (type, body))
        print("post请求body类型为：%s"%(type))

    verify = False
    res = {}   # 接受返回数据


    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      data=body,
                      verify=verify
                       )
        # print("页面返回信息：%s" % r.content.decode("utf-8"))
        res['id'] = testdata['id']
        res['rowNum'] = testdata['rowNum']
        res["content"] = testdata["content"]
        res["statuscode"] = str(r.status_code)  # 状态码转成str
        res["text"] = r.content.decode("?utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""

        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        else:
            res["result"] = "fail"
        return res
    except Exception as msg:
        res["msg"] = str(msg)
        return res


def wirte_result(result, filename="result.xlsx"):
    # 返回结果的行数row_nub
    row_nub = result['rowNum']
    # 写入statuscode
    wt = Write_excel(filename)
    wt.write(row_nub, 9, result['statuscode'])       # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 10, result['times'])            # 耗时
    wt.write(row_nub, 11, result['error'])            # 状态码非200时的返回信息
    wt.write(row_nub, 13, result['result'])
    wt.write(row_nub, 14, result['msg'])           # 抛异常

if __name__ == "__main__":
    data = ExcelUtil("debug_api.xlsx").dict_data()
    print(data[0])
    s = requests.session()
    res = send_requests(s, data[0])
    copy_excel(r"C:\Users\Administrator\PycharmProjects\xin\new\cszdh\case\demo_api.xlsx", "result.xlsx")
    wirte_result(res, filename="result.xlsx")