# URL Shortener API - AWS Lambda
# Author: Sharon | Deployed via GitHub Actions

import json
import boto3
import random
import string
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('url-shortener')

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    
    if http_method == 'POST':
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('long_url', '')
        
        if not long_url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'long_url is required'})
            }
        
        short_id = generate_short_id()
        
        table.put_item(Item={
            'short_id': short_id,
            'long_url': long_url,
            'created_at': str(datetime.utcnow())
        })
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'short_id': short_id,
                'short_url': f'https://short.ly/{short_id}',
                'long_url': long_url
            })
        }
    
    elif http_method == 'GET':
        short_id = event.get('pathParameters', {}).get('short_id', '')
        
        if not short_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'short_id is required'})
            }
        
        response = table.get_item(Key={'short_id': short_id})
        item = response.get('Item')
        
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'URL not found'})
            }
        
        return {
            'statusCode': 301,
            'headers': {'Location': item['long_url']},
            'body': json.dumps({'long_url': item['long_url']})
        }
    
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
