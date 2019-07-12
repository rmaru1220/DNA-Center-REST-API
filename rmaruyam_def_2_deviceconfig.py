import requests
import json
import pprint
import os
import datetime
import re
import csv

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
        print(device['macAddress'])
        print(device['id'])
    print('----end----')

#ここから元のファイル
'''def get_deviceconfigall(token, url):
    api_call = '/dna/intent/api/v1/network-device/config'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print(json.dumps(response['response'], indent=4)) '''
#ここまで元ファイル

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
    '''with open('configdata.csv', 'w', newline='') as file:
        w = csv.Dictwriter(file, fieldnames=['runningConfig', 'id'])
        w.writeheader()
        w.writerow([configdata])'''

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


def get_enterprisessid(token, url):
    api_call = '/dna/intent/api/v1/enterprise-ssid'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print(json.dumps(response, indent=4))
    #print(response)

def get_overallnwhealth(token, url, unixtime):
    api_call = '/dna/intent/api/v1/network-health'
    url += api_call
    url += '?timestamp='
    url += unixtime
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print(json.dumps(response, indent=4))

def get_scheduledtasks(token, url):
    api_call = '/v1/scheduled-job'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    print(json.dumps(response['response'][0]))

def get_tasks(token, url):
    api_call = '/v1/task'
    url += api_call
    headers = {'X-Auth-Token':token}
    response = requests.request('GET', url, headers=headers, verify=False).json()
    #print(type(response['response']))
    #print(len(response['response']))
    print(json.dumps(response['response']))

def get_clientdetail(token, url, macaddr, unixtime):
    api_call = '/dna/intent/api/v1/client-detail'
    url += api_call
    headers = {
      'X-Auth-Token':token,
      'Content-Type':'application/json',
      '__runsync': "true",
      '__timeout': "30",
      '__persistbapioutput': "true",
    }
    querystring = {
      "timestamp":unixtime,
      "macAddress":macaddr,
    }
    response = requests.request("GET", url, headers=headers, params=querystring, verify=False).json()
    print(json.dumps(response))
