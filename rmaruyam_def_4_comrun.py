import requests
import json
import pprint
import os
import datetime
import re
import csv
import http.client
import socket

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

DNAC_URL = 'https://10.71.130.60/api'
DNAC_URI = 'https://10.71.130.60'
DNAC_USER = 'admin'
DNAC_PASSWORD = 'C1sco12345!'

def get_token(url, user, password):
    api_call = '/system/v1/auth/token'
    url += api_call
    response = requests.post(url=url, auth=(user, password), verify=False).json()
    return response["Token"]

def get_devicelist(token, url):
    api_call = '/dna/intent/api/v1/network-device'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print(json.dumps(response['response'], indent=4))

def get_devicelist_filtered(token, url):
    api_call = '/dna/intent/api/v1/network-device'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print(json.dumps(response['response'], indent=4))
    for device in response['response']:
        print('--------')
        print(device['hostname'])
        print(device['softwareVersion'])
        print(device['serialNumber'])
        print('---deviceid---')
        print(device['id'])
        print('---instanceUuid---')
        print(device['instanceUuid'])
    print('-----end-----')

#ここからconfigall改造版
def get_deviceconfigall(token, url):
    api_call = '/dna/intent/api/v1/network-device/config'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()

    #responseをjson型から文字列に変換（dumps処理）
    #config文字列の中にある「\\n」を「\n」に変換（replace処理）して改行表示させる
    configdata = json.dumps(response, indent=4).replace('\\n', '\n')
    print(configdata)
    configtxt = str(configdata)
    #print(configtxt)

    '''#textファイルに出力
    with open("configdata.txt", "w") as file:
        file.write(configtxt)
        '''
    with open('configdata.csv', 'w', newline='') as file:
        w = csv.Dictwriter(file, fieldnames=['runningConfig', 'id'])
        w.writeheader()
        w.writerow([configdata])
#ここまでconfigall改造版

#特定の機器IDに紐付くコンフィグを表示、テキストファイルへ出力する
def get_deviceconfigbyid(token, url):
    deviceid = input('Please enter device id -> ')

    api_call = '/dna/intent/api/v1/network-device/'
    url += api_call
    url += deviceid
    url += '/config'
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    configdata = json.dumps(response, indent=4).replace('\\n', '\n')
    print(configdata)

    #datetimeモジュールを使用して、プログラム実行時の時間を取得して、「d」に代入しておく
    d = datetime.datetime.now()
    hn = str()

    #config.txtを新規作成。configdataを書き込む。
    with open("configbyid.txt", "w") as file:
        file.write(configdata)

    #textファイルをreadで開き、データ内容から「hostname」が含まれる行を検索する。
    ld = open('configbyid.txt', 'r')
    lines = ld.readlines()
    ld.close()
    for line in lines:
        if line.find("hostname") >= 0:
            #一致する行が見つかったら、hnに代入する。
            hn = str(line[:-1])
            #hn の状態では、hostname+半角スペースが余計なので、これをreplaceで無文字に置換。実質削除。
            hn2 = hn.replace("hostname ","")

    #textファイルをwriteで開いて、コンフィグデータを書き込む。
    with open("configbyid.txt", "w") as file:
        file.write(configdata)
        #テキストファイルのリネーム。formatを使うことで時間(d)とhostname(hn)をファイル名に代入する。
        os.rename('configbyid.txt', 'configbyid_{0:%Y-%m-%d %H：%M：%S}_{1}.txt'.format(d,hn2))

#コマンドランナーの実行（ex.show run and show start）
def command_runner(token, url):
    api_call = 'api/v1/network-device-poller/cli/read-request'
    payload = {
        "commands": [
            "show running-config",
            "show startup-config"
        ],
        "description": "test show run",
        "deviceUuids": [
            "e8fa4b73-b6ac-44f5-8d9b-59b5aa5e9758"
        ],
        "name": "show-run and show-start"
    }
    headers = {'X-Auth-Token':token,
               'Content-Type': "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    print(response.text)
