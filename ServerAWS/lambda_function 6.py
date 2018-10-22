# coding: utf-8
 
# ①ライブラリのimport
import logging
import datetime
import decimal
import boto3
import json
import traceback
import sys
from boto3.dynamodb.conditions import Key, Attr
 
# ②Functionのロードをログに出力
print('Loading function')
 
# ③DynamoDBオブジェクトを取得
dynamodb = boto3.resource('dynamodb')

 # ⑤テーブル名を指定
table_name = "RMS_DB"
   
# ⑦DynamoDBテーブルのオブジェクトを取得
dynamotable = dynamodb.Table(table_name)
 
# ④Lambdaのメイン関数
def lambda_handler(event, context):
    MaxItemID=GetMaxItemID()
    # ⑧データの書き込み
    dynamotable.put_item(
        Item={
            "ItemID":str(MaxItemID),
            "UserID":event['UserID'],
            "Barcode":event['Barcode'],
            "ExYear":event['ExYear'],
            "ExMonth":event['ExMonth'],
            "ExDay": event['ExDay'],
            "FoodName":event['FoodName'],
            "imageURL":event['imageURL']
       }
    )

    res_message = event['FoodName']+"を登録しました。\n賞味期限は"+event['ExYear']+"年"+event['ExMonth']+"月"+event['ExDay']+"日です。"
    return res_message

#maxItemId serch
def GetMaxItemID():
   #db scan
   res = dynamotable.scan(ProjectionExpression='ItemID')
   #result check
   print (res)
   #max ItemID search
   max=0;
   for i in range(res['Count']):
       if i==0:
           max=  res['Items'][i]
       else:
           t=res['Items'][i]
           if int(max["ItemID"])< int(t["ItemID"]):
               max=res['Items'][i]
   max=int(max['ItemID'])+1
   return max