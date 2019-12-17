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


# DOES: Analize language used in the content, then update version of the content.
# If this commit is first commit, then version = 1
# If this commit is not first commit, then version += 1

def main():
    # Setup environment
    workshop_name = os.environ['WORKSHOP_NAME']
    version_table_name = os.environ['VERSION_TABLE']
    dynamodb = boto3.resource('dynamodb')
    version_table = dynamodb.Table(version_table_name)
    content_current_versions = ''

    # Analize languages in toml file
    dict_toml = toml.load(open('./config.toml'))
    number_of_languages = len(dict_toml['Languages']) - 1
    for i, lang in enumerate(dict_toml['Languages']):
        content_id = workshop_name + "+" + lang

        print('Load JSON structure\n')
        with open("./public/" + lang +"/index.json", 'r') as j:
            current_structure = json.load(j)
        print('Finished Load JSON\n')

        # Send structure data to DynamoDB Table
        print('Start to send structure data\n')
        try:
            now = datetime.datetime.now().strftime('%s')
            response = version_table.query(
                KeyConditionExpression=Key('content_id').eq(content_id+"+"+lang),
                ScanIndexForward = False,
                Limit = 1 
             )
            previous_structure = response['Items'][0]['structure']
            previous_version = int(response['Items'][0]['version'])

            print('The older record is found\n')
            current_version = previous_version + 1
            
            response = version_table.update_item(
                Key = 
                {
                    'content_id': content_id,
                    'version' : current_version
                },
                UpdateExpression='SET structure = :val1, created_at = :val2',
                ExpressionAttributeValues={
                    ':val1': current_structure,
                    ':val2': now
                }
            )
            # response = version_table.update_item(
            #     Key = 
            #     {
            #         'content_id': content_id,
            #         'version' : 0
            #     },
            #     UpdateExpression='SET available_languages = :val1, updated_at = :val2',
            #     ExpressionAttributeValues={
            #         ':val1': dict_toml['Languages'],
            #         ':val2': now
            #     }
            # )
        except :
            print('This is the first record\n')
            current_version = 1
            now = datetime.datetime.now().strftime('%s')
            # Send structure to dynamoDB
            response = version_table.put_item(
                Item={
                    "content_id": content_id,
                    "version": current_version,
                    "structure": current_structure,
                    "workshop_name": workshop_name,
                    "created_at": now
                }
            )
            # response = version_table.put_item(
            #     Item={
            #         "content_id": content_id,
            #         "version": 0,
            #         "available_languages": dict_toml['Languages'],
            #         "created_at" : now
            #     }
            # )
        # list up current versions to inject toml
        content_current_versions += str(lang) + ':' + str(current_version)
        if i < number_of_languages:
            content_current_versions += ','

        print('Finished sending a structure\n')
    
    # Inject version information in toml
    dict_toml['params']['versions'] = content_current_versions
    toml.dump(dict_toml, open('./config.toml', mode='w'))
    print('All done! Returning...\n')

if __name__ == "__main__":
    debug = False
    if debug:
        logger.setLevel(logging.DEBUG)
        os.environ['WORKSHOP_NAME'] = 'your_workshop_name'
        os.environ['VERSION_TABLE'] = 'test_content_version_table'
            
    main()
