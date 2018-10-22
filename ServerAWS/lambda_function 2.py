import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table    = dynamodb.Table('RMS_DB')
    
    table.delete_item(Key={'ItemID': event['ItemID']})
    
    return {
        "statusCode": 200,
        "body": json.dumps('deleted')
    }
