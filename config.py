import logging
from xmlrpc.client import DateTime
from playhouse.db_url import connect
from peewee import Model
from peewee import IntegerField
from peewee import CharField
from peewee import DateTimeField
from flask_login import UserMixin
logger = logging.getLogger("peewee")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
db = connect("sqlite:///peewee_db.sqlite")
if not db.connect():
    print("接続できませんでした")
    exit()
class File(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    basyo = CharField()
    file = CharField()
    memo = CharField()
    syurui = CharField()
    hiniti = DateTimeField()
    class Meta:
        database = db
        table_name = "Files"

class User(UserMixin, Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    password = CharField()
    class Meta:
        database = db
        table_name = "users"

# db.drop_tables([File,User])
db.create_tables([File,User])