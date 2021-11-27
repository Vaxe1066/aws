import json
import requests
import boto3
from boto3.dynamodb.conditions import Key
import main as m
from dotenv import load_dotenv
import os


#url = "https://en.wikipedia.org/wiki/Arsenal_F.C."
#wordString = 'ball, cup, football, beautiful'
#print(m.getDataFromUrl(url, wordString))

def lambda_handler(event):
    
    #get url string here, load json body first then extract url string
    body = json.loads(event["body"])
    url = body["url"]

    if(m.validUrl(url)==True and 'en.wikipedia.org/wiki/' in url):
        #get word string here
        wordString = body["wordString"]

        client = boto3.resource('dynamodb')

        load_dotenv('.env')
        #define database
        tableName = os.environ.get('TABLE')
        table = client.Table(tableName)

        newVals = m.getDataFromUrl(url, wordString)

        #update item - using this as it'll create new item if the item doesnt exist
        table.update_item(
            Key={
                'urlString': url
            },
            UpdateExpression="SET wordCounts = :updated",
            ExpressionAttributeValues={
                ':updated': newVals
                }
            )

        resBody = json.dumps({"output": newVals})
        #ideally would have a error handling of the update function

        #successful 'update' send 200 response 
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": resBody
        }



    else:
        response = {
                "statusCode": '400',
                "body": json.dumps({ "error": 'Enter a valid URL, root path must also begin with: en.wikipedia.org/wiki/' }),
                "headers": {
                    "Content-Type": "application/json",
                }
            }

    return response

    