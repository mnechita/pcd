import json
import os
import time

import boto3
import requests

QUERY_URL = r'https://api.scryfall.com/cards/search?order=name&q=game%3Aarena&unique=prints'

ses = requests.Session()
ses.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

botoses = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_ACCESSKEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRETKEY'),
)
BUCKET_NAME = 'elasticbeanstalk-eu-west-1-679217559293'
CARDS_FOLDER = 'cards'

s3 = botoses.client('s3')
dyn = botoses.resource('dynamodb')
table = dyn.Table('Test')


def crawl():
    next = QUERY_URL
    while True:
        print(next)
        content = ses.get(next).json()

        for card in content['data']:
            try:
                arena_id = card['arena_id']
                name = card['name']
                image_uri = card['image_uris']['normal']

                print(name)
                set = card['set']
                rarity = card['rarity']
                cardKey = CARDS_FOLDER + '/' + str(arena_id) + '.jpg'
                image_data = ses.get(image_uri).content
                s3.put_object(ACL='public-read', Body=image_data, Bucket=BUCKET_NAME, Key=cardKey,
                              ContentType='image/jpeg')

                s3URI = 'https://' + BUCKET_NAME + '.s3.amazonaws.com/' + cardKey
                table.put_item(Item={
                    'FirstID': str(arena_id),
                    'SecondID': str(arena_id),
                    'Name': name,
                    'Set': set,
                    'Rarity': rarity,
                    'Uri': s3URI
                })

                time.sleep(0.2)
            except:
                print('[ERR]' + json.dumps(card))

        if content['has_more']:
            next = content['next_page']
        else:
            break


def main():
    # crawl()
    return


if __name__ == '__main__':
    main()
