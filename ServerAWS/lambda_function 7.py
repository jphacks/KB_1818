import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('RMS_DB')

    res = table.query(
        IndexName='UserID-index',
        KeyConditionExpression=Key('UserID').eq(event['UserID'])
    )
    
    # for row in res['Items']:
    #     print(row)
    
    # return res['Items']
    line_json=makeJson()
    print(res)
    
    # addJson(line_json,res['Items'])
    print("--------main--------")
    print(line_json)
    print(res['Count'])
    print(res['Items'])
    print("--------Items--------")
    print(res['Items'][0])
    for i in range(res['Count']):
        addJson(line_json,res['Items'][i])
    
    
    # line_json['contents'].append(tmp)
    line_json={
        "type": "flex",
        "altText": "【冷蔵庫の中身はこれだよ。】",
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