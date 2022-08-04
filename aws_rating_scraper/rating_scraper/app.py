import json
from scraper import scrap_rating
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    content = json.loads(event['body'])
    print(content)
    data = scrap_rating(content)
    # data = scrap_rating(event)
    # logging.info(data)
    print("ATTENTION: " + data)
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json'
            # 'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps({
            "rating": data,
            "title": content['title']
        })
    }