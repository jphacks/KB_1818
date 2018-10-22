import logging

import os
import urllib.request, urllib.parse
import json
import random

import base64
import hashlib
import hmac
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(request, context):
    # messageの内容
    message_txt="これが出たらif文ミスってそう"

    # リクエストの検証を行う
    channel_secret = 'API_CHANNEL_ID'
    # LINEへのアクセスtoken
    access_token='API_TOKEN_ID'
    # talkの送り主
    useId=request['events'][0]['source']['userId']

    print(request['events'])
    # print("***********\n")
    # hash = hmac.new(channel_secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()

    # # LINE 以外からのアクセスだった場合は処理を終了させる（今回は使用しないよー）
    # signature = base64.b64encode(hash).decode('utf-8')
    # if signature != request.get('headers').get('X-Line-Signature', ''):
    #     logger.info(f'LINE 以外からのアクセス request={request}')
    #     return {'statusCode': 200, 'body': '{}'}

    # LINEbotで送信するメッセージ
    line_message_txt=request['events'][0]['message']['text']

    # 発言内容によってlambdaを実行
    if line_message_txt== 'test':
        message_txt="testですよー"
        sendMessage(message_txt,request,access_token)
    elif line_message_txt== '冷蔵庫':
        message_txt="今冷蔵庫は空っぽですよー"
        sendMessage(message_txt,request,access_token)
    elif line_message_txt== '冷蔵庫の中の食品を教えて':
        # 引数
        print("********")
        print(useId)
        input_event = {
            "UserID": useId
        }
        Payload = json.dumps(input_event) # jsonシリアライズ

        # 呼び出し
        response = boto3.client('lambda').invoke(
            FunctionName='TestMakeJson',
            # FunctionName='RMS_PostJson',
            InvocationType='RequestResponse',
            Payload=Payload
        )

        # レスポンス読出し
        response_payload = json.loads(response["Payload"].read()) # jsonデコード
        print("****getAll出来てる？****")
        print(response_payload)
        sendMessage("冷蔵庫の中身はこれだよ。",request,access_token)
        showcarousel(request,access_token,response_payload)

    elif line_message_txt== '期限間近の食品を教えて':
        # 引数
        print("********")
        print(useId)
        input_event = {
            "UserID": useId
        }
        Payload = json.dumps(input_event) # jsonシリアライズ

        # 呼び出し
        # sendMessage("3日以内に期限が切れる食品だよ。",request,access_token)
        # sendMessage("賞味期限が切れちゃう前に食べてね。",request,access_token)
        response = boto3.client('lambda').invoke(
            FunctionName='RMS_AlarmExData',
            InvocationType='RequestResponse',
            Payload=Payload
        )
        # sendMessage("3日以内に期限が切れる食品だよ。",request,access_token)
        # レスポンス読出し
        response_payload = json.loads(response["Payload"].read()) # jsonデコード
        print(response_payload)

    else:
        message_txt="どうせ私は冷たい冷蔵庫です。"
        message_txt="何もしてあげられません。\n冷めた対応ですみません。"
        sendMessage(message_txt,request,access_token)
    return {'statusCode': 200, 'body': '{}'}

# 実際にLINEに送信する処理
def sendMessage(message_txt,request,access_token):
    # LINE に発言する
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +access_token,
    }
    body = {
        'replyToken': request['events'][0]['replyToken'],
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
def showcarousel(request,access_token,jsonData):
    # LINEServerへ"push"
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +access_token,
    }
    # 表示するJson
    body = {
        "to":request['events'][0]['source']['userId'],
        'messages': [jsonData]
    }

    print("============")
    print("body")
    print(body)
    # 実際の送信処理
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)

    with urllib.request.urlopen(req) as res:
        res_body = res.read().decode('utf-8')
        if res_body != '{}':
            logger.info(res_body)

def getAll(userID):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('RMS_DB')

    res = table.query(
        IndexName='UserID-index',
        KeyConditionExpression=Key('UserID').eq(userID)
    )

    #
    for row in res['Items']:
        print(row)

    return res['Items']
