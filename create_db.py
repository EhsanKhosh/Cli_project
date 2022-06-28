import random
import peewee
from peewee import Model

db = peewee.SqliteDatabase("students.db")
db.connect()


class Student(Model):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    age = peewee.IntegerField()
    phone_num = peewee.CharField()
    student_id = peewee.IntegerField()

    class Meta:
        database = db



