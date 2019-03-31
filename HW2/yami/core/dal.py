import boto3
from yami.settings import *
from cryptography.fernet import Fernet


class KeyGenerator:

    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, plain_text):
        return self.cipher_suite.encrypt(plain_text)

    def decrypt(self, cipher_text):
        return self.cipher_suite.decrypt(cipher_text)


encryption_helper = KeyGenerator()


class DAL:

    def __init__(self):
        # dynamodb configuration
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION)

        self.users = self.dynamodb.Table('Players')
        self.cards = self.dynamodb.Table('Cards')

    def create_user(self, user):
        self.users.put_item(Item=
        {
            'Firstname': user.first_name,
            'Surname': user.last_name,
            'Email': user.email,
            'Password': encryption_helper.encrypt(bytes(user.password, 'utf-8')),
            'PlayerId': user.username
        })

    def check_user(self, user):
        enc_pass = encryption_helper.encrypt(bytes(user.password, 'utf-8')).decode("utf-8")
        response = self.users.get_item(TableName='Players', Key={'PlayerId': user.username})
        return response is not None
