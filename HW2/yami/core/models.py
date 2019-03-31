from django.db import models

# Create your models here.
class User:

    def __init__(self, username, passwd):
        self.username = username
        self.password = passwd