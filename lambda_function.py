import json
import boto3
import base64
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket = 'XXXX' #define ur own 
    region = 'XXXX' #define ur own 
        
    if event['httpMethod'] == 'POST' : 
        data = json.loads(event['body'])
        name = data['name'] #.png/ .jpg
        folderType = data['folderType']
        fileType = data['fileType']
        
        folder = ''
        
        #recieve base 64 image 
        image = data['file']
        #folder inside the bucket
        if folderType == 'background':
            folder = 'background/'
        if folderType == 'attribute':
            folder = 'attribute/'
        if folderType == 'character':
            folder = 'character/'
        if folderType == 'graph':
            folder = 'graph/'
        if folderType == "graphData":
            folder = 'graphData/'
            
        image = image[image.find(",")+1:] 
        dec = base64.b64decode(image + "===")
        s3.put_object(Bucket=bucket, Key=folder + name, Body=dec, ACL='public-read', ContentType=fileType)
    
        return_url = "https://" + str(bucket) + "."+ str(region) + ".amazonaws.com/" +  str(folder) + str(name)
        
        #must return the link of the image here 
        return {'statusCode': 200, 'body': json.dumps({'statusCode': 200, 'message': 'successful lambda function call', 'url': return_url}), 'headers': {'Access-Control-Allow-Origin': '*'}}
        
        
    if event['httpMethod'] == 'DELETE':
        key = event['key']
        bucket = s3.delete_object(Bucket= bucket, Key=key)
            
        return {'statusCode': 200, 'body': json.dumps({'statusCode': 200, 'message': 'successful deleted object ' }), 'headers': {'Access-Control-Allow-Origin': '*'}}
        
        
    if event['httpMethod'] == 'GET':
        output_list_url = []
        bucket = s3.list_objects_v2(Bucket= bucket)
        for key in bucket['Contents']:
            output_list_url.append(key['Key'])

        return {'statusCode': 200, 'body': json.dumps({'statusCode': 200, 'message': 'successful lambda function call', 'url': output_list_url}), 'headers': {'Access-Control-Allow-Origin': '*'}}
        
