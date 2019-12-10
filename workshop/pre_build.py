import toml
import os
import logging
logger = logging.getLogger()

def main():
    # Parameters from ENV
    region = os.environ['RT_REGION']
    deliveryId = os.environ['WORKSHOP_NAME']
    kinesisStreamName = os.environ['RT_KINESIS']
    cognitoPoolId = os.environ['RT_COGNITO']

    # Toml File Injection
    try:
        dict_toml = toml.load(open('./config.toml'))
        dict_toml['params']['deliveryid'] = deliveryId
        dict_toml['params']['kinesisstreamname'] = kinesisStreamName
        dict_toml['params']['cognitopoolid'] = cognitoPoolId
        dict_toml['params']['awsregion'] = region
        toml.dump(dict_toml, open('./config.toml', mode='w'))
    except Exception as err:
        logger.warning('Toml File Injection Failed')
        logger.exception('Raise Exception: %s', err)
        raise

if __name__ == "__main__":
    debug  = False
    if debug:
        logger.setLevel(logging.DEBUG)
        os.environ['RT_REGION'] = 'your_region'
        os.environ['RT_KINESIS'] = 'your_kinesisstream_name'
        os.environ['RT_COGNITO'] = 'your_cognito_pool_id'
        os.environ['WORKSHOP_NAME'] = 'your_delivery_id'
            
    main()