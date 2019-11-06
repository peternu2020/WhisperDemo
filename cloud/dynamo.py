import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
audio_table = dynamodb.Table('audio_identifiers')
text_table = dynamodb.Table('text_version_audio')
mapping_table = dynamodb.Table('mapping')

#rpId = rasberrypi id {1,2,3,4} for now
def putId(id, rpId, txt):
    audio_table.put_item(
        Item={
            'audioId': id,
            'rpId' : rpId,
            'speechToText' : txt,
        }
    )

def getId(id):
    try:
        response = audio_table.get_item(
            Key={
                'audioId': id,
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])

    item = response['Item']
    return item

#for collections by fixed variables {1,2,3,4}
def getIdByRp(id):
    res = []
    try:
        response = audio_table.scan(
            FilterExpression = Attr('rpId').eq('1')
            )
        for i in response['Items']:
            res.append((i['rpId'], i['audioId'], i['speechToText']))
    except ClientError as e:
        print(e.response['Error']['Message'])
    return res
