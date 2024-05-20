from peewee import *
from datetime import datetime
from flask_login import UserMixin

db = MySQLDatabase('stagSprinters', user='root', password='password', host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel, UserMixin):
    user_id = AutoField()
    username = CharField(max_length=50)
    email = CharField(max_length=100)
    password = CharField(max_length=100)
    is_active = BooleanField(default=True)

    def get_id(self):
        return str(self.user_id)

class Orders(BaseModel):
    order_id = AutoField(primary_key=True)
    user = ForeignKeyField(Users, backref='orders')
    stagID = CharField()
    item_id = CharField()
    quantity = IntegerField()
    order_date = DateTimeField(default=datetime.now)
    firstName = CharField()
    lastName = CharField()

class Addresses(BaseModel):
    dorm_id = AutoField(primary_key=True)
    user = ForeignKeyField(Users, backref='addresses')
    order = ForeignKeyField(Orders, backref='address')
    dorm_name = CharField()
    room_number = CharField()

class Payments(BaseModel):
    payment_id = AutoField(primary_key=True)
    order = ForeignKeyField(Orders, backref='payment')
    payment_method = CharField()
    amount = FloatField()
    payment_date = DateTimeField(default=datetime.now)

db.connect()
db.create_tables([Users, Orders, Addresses, Payments], safe=True)
