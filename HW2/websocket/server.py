import asyncio

import boto3
import websockets

BUCKET_NAME = 'elasticbeanstalk-eu-west-1-679217559293'
FOLDER = 'userfiles'

s3 = boto3.client('s3')


async def receive_file(websocket, path):
    filename = await websocket.recv()
    print(f"Recv filename: {filename}")

    await websocket.send('send file')
    print(f"> send ok filename")

    file_content = await websocket.recv()
    print(f"> received filecontent")

    s3.put_object(Body=file_content, Bucket=BUCKET_NAME, Key=FOLDER + '/' + filename)
    await websocket.send('done')


start_server = websockets.serve(receive_file, '0.0.0.0', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
