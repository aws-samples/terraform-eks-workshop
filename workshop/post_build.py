import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import os
import sys
import toml
import logging
import datetime
import base64
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# DOES: Analize language used in the content, then update structure of content.

def main():
    # Setup environment
    workshop_name = os.environ['WORKSHOP_NAME']
    version_table_name = os.environ['VERSION_TABLE']
    dynamodb = boto3.resource('dynamodb')
    version_table = dynamodb.Table(version_table_name)
    
    content_id = workshop_name
    content_structures = {}
    # Analize languages in toml file
    dict_toml = toml.load(open('./config.toml'))
    number_of_languages = len(dict_toml['Languages']) - 1
    for i,lang in enumerate(dict_toml['Languages']):

        print('Load JSON structure\n')
        with open("./public/" + lang +"/index.json", 'r') as j:
            current_structure = json.load(j)
        print('Finished Load JSON\n')
        content_structures.update({lang:current_structure})
    structure_json = json.loads(str(content_structures).replace("\'", "\""))

    # Send structure data to DynamoDB Table
    print('Start to send structure data\n')
    query_response = version_table.query(
        KeyConditionExpression=Key('content_id').eq(content_id),
        ScanIndexForward = False,
        Limit = 1 
        )
    # Current version is already updated in pre_build.py 
    current_version = int(query_response['Items'][0]['version'])
    unix_timestamp = datetime.datetime.now().strftime('%s')
    update_response = version_table.update_item(
            Key = 
            {
                'content_id': content_id,
                'version' : current_version
            },
            UpdateExpression='SET updated_at = :val1, structure = :val2',
            ExpressionAttributeValues={
                ':val1': unix_timestamp,
                ':val2': structure_json
            }
        )
    print('Finished sending sructure\n')

    print('Post build phase done\n')

if __name__ == "__main__":
    debug = False
    if debug:
        logger.setLevel(logging.DEBUG)
        os.environ['WORKSHOP_NAME'] = 'your_content_id'
        os.environ['VERSION_TABLE'] = 'test_content_meta_table'
            
    main()
