import boto3


class Bucket:
    def __init__(self, name):
        self.name = name
        self.s3 = boto3.client('s3')

    def upload_file(self, filename, filedata):
        key = filename
        new_filename = 'cards.txt'
        self.s3.upload_file(key, self.name, new_filename)
