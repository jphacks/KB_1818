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
    
    #
    for row in res['Items']:
        print(row)
    
    return res['Items']