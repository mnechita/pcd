import asyncio
import ssl
import websockets
import boto3

BUCKET_NAME = 'yami-bucket'


async def receive_file(websocket, path):
    file_content = await websocket.recv()
    print(f"< {file_content}")

    filename = "somefilename.txt"
    f = open(filename, "wb")
    f.write(file_content)
    f.close()

    s3 = boto3.client('s3')
    s3.upload_file(filename, BUCKET_NAME, filename)

    await websocket.send('Ok')
    print(f"> Sent ok")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(pathlib.Path(__file__).with_name('localhost.pem'))

start_server = websockets.serve(receive_file, '0.0.0.0', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()