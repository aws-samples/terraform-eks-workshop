import toml
import os
import logging
import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr
logger = logging.getLogger()

def main():
    # Parameters from ENV
    region = os.environ['RT_REGION']
    workshop_name = os.environ['WORKSHOP_NAME']
    kinesis_stream_name = os.environ['RT_KINESIS']
    cognito_pool_id = os.environ['RT_COGNITO']
    version_table_name = os.environ['VERSION_TABLE']

    # Query content version from DDB
    # If this commit is first commit, then version = 1, is not first commit then version += 1
    # TODO : Content id will be changed as hostName 
    
    print('Load version from DDB\n')
    content_id = workshop_name
    version_table = boto3.resource('dynamodb').Table(version_table_name)
    try:
        query_response = version_table.query(
            KeyConditionExpression=Key('content_id').eq(content_id),
            ScanIndexForward = False,
            Limit = 1 
            )
        previous_version = int(query_response['Items'][0]['version'])
        print('Older record is found\n')
        current_version = previous_version + 1
        unix_timestamp = datetime.datetime.now().strftime('%s')

        update_response = version_table.update_item(
                Key = 
                {
                    'content_id': content_id,
                    'version' : current_version
                },
                UpdateExpression='SET updated_at = :val1',
                ExpressionAttributeValues={
                    ':val1': unix_timestamp
                }
            )
        print('Update the version succeeded\n')
    except Exception as err:
        #print(err)
        print('First time record\n')
        current_version = 1
        unix_timestamp = datetime.datetime.now().strftime('%s')
        insert_response = version_table.put_item(
                Item={
                    "content_id": content_id,
                    "version": current_version,
                    "workshop_name": workshop_name,
                    "created_at": unix_timestamp,
                    "updated_at": unix_timestamp
                }
        )
        print('Insert a record succeeded\n')

    # Toml File Injection
    try:
        dict_toml = toml.load(open('./config.toml'))
        dict_toml['params']['contentid'] = content_id
        dict_toml['params']['kinesisstreamname'] = kinesis_stream_name
        dict_toml['params']['cognitopoolid'] = cognito_pool_id
        dict_toml['params']['awsregion'] = region
        dict_toml['params']['contentversion'] = current_version
        toml.dump(dict_toml, open('./config.toml', mode='w'))
    except Exception as err:
        logger.warning('Toml File Injection Failed')
        logger.exception('Raise Exception: %s', err)
        raise

    print('Pre build phase done\n')

if __name__ == "__main__":
    debug  = False
    if debug:
        logger.setLevel(logging.DEBUG)
        os.environ['RT_REGION'] = 'your_region'
        os.environ['RT_KINESIS'] = 'your_kinesisstream_name'
        os.environ['RT_COGNITO'] = 'your_cognito_pool_id'
        os.environ['WORKSHOP_NAME'] = 'your_content_id'
        os.environ['VERSION_TABLE'] = 'test_content_meta_table'
    main()