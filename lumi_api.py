# -*- coding: utf-8 -*-
import requests
import json
import time


class LumiClient:
    '''
    :param port: api服务的端口号
    :param token: api服务的token
    '''

    def __init__(self, port: int, token: str) -> None:
        self.port = port
        self.host = "127.0.0.1"
        self.token = token
        self.url = f"http://{self.host}:{self.port}"

    def _build_headers(self):
        return {"Content-Type": "application/json", "token": self.token}

    def _post(self, path, data=None):
        return requests.post(self.url + path, json=data, headers=self._build_headers())

    def _get(self, path, data=None):
        return requests.get(self.url + path, params=data, headers=self._build_headers())

    '''
     健康检查,用于检查API服务是否正常运行,文档地址:https://lumibrowser.com/api/#/api_health
    '''

    def health(self):
        return self._get("/health").json()

    '''
    获取窗口列表,文档地址: https://lumibrowser.com/api/#/api_list
    :param dirId: 窗口id, 选填；如果填了就只查询这个窗口的信息
    :param page_index,page_size 分页参数,dirId 不填的时候有效
    :res 返回值参考文档
    '''

    def browser_list(self, dirId: str = "", page_index: int = 1, page_size: int = 15):
        return self._get("/browser/list", {"dirId": dirId, "page_index": page_index, "page_size": page_size}).json()

    '''
    创建窗口,文档地址: https://lumibrowser.com/api/#/api_create
    :param data: 创建窗口需要传的参数,参考文档说明
    :res 返回值参考文档
    '''

    def browser_create(self, data: dict = None):
        return self._post("/browser/create", data).json()

    '''
    修改窗口，文档地址: https://lumibrowser.com/api/#/api_mdf
    :param data: 创建窗口需要传的参数,参考文档说明
    :res 返回值参考文档
    '''

    def browser_mdf(self, data: dict):
        return self._post("/browser/mdf", data).json()

    '''
    删除窗口,文档地址:https://lumibrowser.com/api/#/api_delete
    :param data: 需要删除的窗口ID
    :res 返回值参考文档
    '''

    def browser_delete(self, data: dict):
        return self._post("/browser/delete", data).json()

    '''
    打开窗口,文档地址：https://lumibrowser.com/api/#/api_open
    :param dirId: 需要打开的窗口ID
    :res 返回值参考文档
    '''

    def browser_open(self, dirId: str, args=[]):
        return self._post("/browser/open", {"dirId": dirId, "args": args}).json()

    '''
    关闭窗口,文档地址:https://lumibrowser.com/api/#/api_close
    :param dirId: 需要关闭的窗口ID
    :res 返回值参考文档
    '''

    def browser_close(self, dirId: str):
        return self._post("/browser/close", {"dirId": dirId}).json()

    '''
    获取平台购买的静态IP,文档地址:https://lumibrowser.com/api/#/api_static_list
    :param page_index,page_size 分页参数
    :res 返回值参考文档
    '''

    def browser_static_ip_list(self, page_index: int = 1, page_size: int = 15):
        return self._get("/browser/static_list", {"page_index": page_index, "page_size": page_size}).json()

    '''
    获取已打开的浏览器,文档地址:https://lumibrowser.com/api/#/api_pid
    '''

    def browser_connection_info(self):
        return self._get("/browser/connection_info").json()


if __name__ == "__main__":
    client = LumiClient(port=50000, token="61d8c968f0a66dcf2b05982bdccb484b")
    # print(client.health())
    # print(client.browser_list())
    '''
    data = {
        "windowName":"启动时随机指纹",
        "coreVersion":"117",
        "os":"Windows",
        "cookie":[
            {
                "name":"testcookie",
                "value":"2324325",
                "domain":".facebook.com"
            },
              {
                "name":"testcookie2",
                "value":"2324325",
                "domain":".facebook.com"
            },
              {
                "name":"testcookie3",
                "value":"2324325",
                "domain":".facebook.com"
            }
        ],
        "windowRemark":"备注",
        "proxyInfo":{
            "proxyMethod":"import",
            "proxyType":"rotate",
            "proxyNetwork":"resi",
            "ipType":"IPV4",
            "protocol":"SOCKS5",
            "host":"xxx",
            "port":"1200",
            "proxyUserName":"xxx",
            "proxyPassword":"xxx"
        },
        "fingerInfo":{
            "randomFingerprint":True,
            "portScanProtect":False
        }
    }
    print(client.browser_create(data))

    data = {
        "dirId":"ac4bd731074a6ef3bbe1e8f4f6667749",
        "windowName":"修改窗口",
        "coreVersion":"109",
        "os":"macOS",
        "proxyInfo":{
            "port":"1000"
        }
    }
    print(client.browser_mdf(data))

    '''

    # print(client.browser_delete({"dirIds":["239983d08d11106a7f828bfb1651229b"]}))
    print(client.browser_open("485e3d3988be4e11a52acedb6f2f6ee8"))
    # print(client.browser_close("ac4bd731074a6ef3bbe1e8f4f6667749"))
    # print(client.browser_static_ip_list())
    print(client.browser_connection_info())
