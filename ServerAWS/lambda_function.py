import boto3
import json
from datetime import datetime,date
from boto3.dynamodb.conditions import Key, Attr
# ①ライブラリのimport
import logging
import decimal
import traceback
import sys

import os
import urllib.request, urllib.parse
import random

import base64
import hashlib
import hmac


def lambda_handler(request, context):
    # リクエストの検証を行う
    channel_secret = 'CHANNEL_ID'
    # LINEへのアクセスtoken
    access_token='token'
    # talkの送り主
    # とりあえずは決め打ち
    # userId='Ud480f7576a7a1f4d8777d459fe5f5cd0'
    userId='USEID'

    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('RMS_DB')

    res = table.query(
        IndexName='UserID-index',
        KeyConditionExpression=Key('UserID').eq(userId)
    )
    #for row in res['Items']:
    #    print(row)
    print (res)

    # init
    #time=datetime.now().strftime('%D')
    #time2=datetime.now()
    #now_hour = datetime.now().strftime('%H')

    #print (time)
    #print(time2)

    #print (res['Items'][0]['ExYear'])

    CollectList = [-99] * res['Count']
    CCount=0
    #賞味期限を3日早めてalarmを出せるように
    for i in range(res['Count']):
         year=int(res['Items'][i]['ExYear'])
         month=int(res['Items'][i]['ExMonth'])
         day=int(res['Items'][i]['ExDay'])-4
         #print (year)
         #print (month)
         #print (day)
         #datetime=datetime.now()
         target=datetime(year,month,day)
         nowTime = datetime.now()
         print (target)
         print(nowTime)
         if nowTime>=target:
             print ('賞味期限切れになりそう')
             CollectList[i]=200
             CCount=CCount+1
             print (target)
    print (CollectList)

    insertCount=0
    #辞書型整形

    dict={
                  "Items": [
                      {'ExDay': '18',
                  'FoodName': 'りんご',
                  'UserID': 'god',
                  'ItemID': '103',
                  'ExYear': '2018',
                  'Barcode': '1129',
                  'ExMonth': '10',
                  'imageURL': 'ダミー'}],
                  'Count': 5,
                  'ScannedCount': 5,
                  'ResponseMetadata': {
                      'RequestId': 'T8JUN14OLF3OVP4DBVG8C8EDMJVV4KQNSO5AEMVJF66Q9ASUAAJG',
                  'HTTPStatusCode': 200,
                  'HTTPHeaders': {'server': 'Server',
                  'date': 'Sat, 20 Oct 2018 14:12:05 GMT',
                  'content-type': 'application/x-amz-json-1.0', 'content-length': '822', 'connection': 'keep-alive',
                  'x-amzn-requestid': 'T8JUN14OLF3OVP4DBVG8C8EDMJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '4179801121'}, 'RetryAttempts': 0}
    }

    print (res['Count'])
    for i in range(res['Count']):
        #対象外のデータ
        if CollectList[i]==-99:
            continue
        #対象の賞味期限が切れたデータを格納
        else:
            if insertCount==0:
                print("0番目!!!!!!!!")
                dict={
                  "Items": [{'ExDay': res['Items'][i]['ExDay'],
                  'FoodName': res['Items'][i]['FoodName'],
                  'UserID': res['Items'][i]['UserID'],
                  'ItemID': int(res['Items'][i]['ItemID']),
                  'ExYear': res['Items'][i]['ExYear'],
                  'Barcode': res['Items'][i]['Barcode'],
                  'ExMonth': res['Items'][i]['ExMonth'],
                  'imageURL': res['Items'][i]['imageURL']}],
                  'Count': int(res['Count']),
                  'ScannedCount':res['ScannedCount'],
                  'ResponseMetadata': res['ResponseMetadata']
                }

            else:
                print('通った!!')
                dictS={'ExDay': res['Items'][i]['ExDay'], 'FoodName':  res['Items'][i]['FoodName'], 'UserID': res['Items'][i]['UserID'],
                'ItemID': res['Items'][i]['ItemID'], 'ExYear':  res['Items'][i]['ExYear'],
                'Barcode': res['Items'][i]['Barcode'], 'ExMonth': res['Items'][i]['ExMonth'],'imageURL': res['Items'][i]['imageURL']}
                dict['Items'].append(dictS)
            insertCount=insertCount+1
    dict['Count']=insertCount
    print("=================")
    print(dict)
    for i in range(res['Count']):
        # 賞味期限が切れそうなときor着れている時の処理
        if CollectList[i]==200:
            outfoods = outFood(dict)
            sendMessage(request,access_token,userId)
            showcarousel(request,access_token,outfoods,userId)
            return dict['Items']
            return "とりあえず表示"
    return 'no trash data'
  #  return dict

# 実際にLINEに送信する処理
def sendMessage(request,access_token,userId):
    message_txt="期限がきれちゃう前に食べてね。"
    # LINE に発言する
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +access_token,
    }
    body = {
        "to":userId,
        'messages': [
            {
                'type': 'text',
                'text': message_txt,
            }
        ]
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        res_body = res.read().decode('utf-8')
        if res_body != '{}':
            logger.info(res_body)

# carouselの表示
def showcarousel(request,access_token,jsonData,userId):
    # LINEServerへ"push"
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +access_token,
    }
    body = {
        "to":userId,
        'messages': [jsonData]
    }

    print("============")
    print("body")
    print(body)
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        res_body = res.read().decode('utf-8')
        if res_body != '{}':
            logger.info(res_body)

def outFood(outfood):
    line_json=makeJson()

    # addJson(line_json,res['Items'])
    print("--------out--------")
    print(outfood['Items'])
    print(line_json)
    print("--------Items--------")
    # print(res['Items'][0])]
    for i in range(outfood['Count']):
        addJson(line_json,outfood['Items'][i])

    print(line_json)
    # line_json['contents'].append(tmp)
    line_json={
        "type": "flex",
        "altText": "【賞味期限のお知らせだよ。】",
        "contents":line_json
    }
    return line_json

def makeJson():
    tmpjson={
        "type": "carousel",
        "contents": []
    }
    return tmpjson

def addJson(line_json,add):
    print("=====================")
    # Deleteのエンドポイント
    endpoint="https://4l6jtib5yd.execute-api.ap-northeast-1.amazonaws.com/dev/RMS_DeleteItem/Delete?"
    tmp={
        "type": "bubble",
        "hero": {
          "type": "image",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover",
          "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"
        },
        "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "text",
              "text": "商品名",
              "wrap": True,
              "weight": "bold",
              "size": "xl"
            },
            {
              "type": "box",
              "layout": "baseline",
              "contents": [
                {
                  "type": "text",
                  "text": "賞味期限：XXXX",
                  "wrap": True,
                  "weight": "bold",
                  "size": "xl",
                  "flex": 0
                }
              ]
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "action": {
                "type": "uri",
                "label": "食べた",
                "uri": "https://4l6jtib5yd.execute-api.ap-northeast-1.amazonaws.com/dev/RMS_DeleteItem?"
              }
            },
            {
              "type": "button",
              "action": {
                "type": "uri",
                "label": "すてた",
                "uri": "https://4l6jtib5yd.execute-api.ap-northeast-1.amazonaws.com/dev/RMS_DeleteItem?"
              }
            }
          ]
      }
    }

    print(add)
    tmp['hero']['url']=add['imageURL']
    print(add['ItemID'])
    tmp['body']['contents'][0]['text']=add['FoodName']
    tmp['body']['contents'][1]['contents'][0]['text']="賞味期限："+add['ExYear']+"/"+add['ExMonth']+"/"+add['ExDay']
    print(tmp['footer']['contents'][0]['action'])
    # print(tmp['footer']['contents'][0]['action']+"UserUD=god&ItemID="+add['ItemID'])
    # tmp['footer']['contents'][0]['action']=endpoint+"UserUD=god&ItemID=110"
    # tmp['footer']['contents'][1]['action']="ボタン２を変更しよう"

    print(tmp['footer']['contents'][0]['action'])

    # display
    print("画像のURL")
    print(tmp['hero']['url'])
    print("---")
    print("商品名")
    print(tmp['body']['contents'][0]['text'])
    print("---")
    print("賞味期限")
    print(tmp['body']['contents'][1]['contents'][0]['text'])
    print("---")
    print(tmp['footer']['contents'][0]['action'])
    print(tmp['footer']['contents'][1]['action'])
    # jsonに追加
    line_json['contents'].append(tmp)
