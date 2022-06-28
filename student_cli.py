import os
import random
import sys
import re
import inquirer
import peewee
from create_db import Student

sys.path.append(os.path.realpath("."))
db = peewee.SqliteDatabase('students.db')
db.connect()


def phone_validation(answers, current):
    if not re.match(r"\+\d{12}", current):
        raise inquirer.errors.ValidationError("", reason="Your number isn't valid !")
    return True


def add_student():
    student = [
        inquirer.Text("FirstName", message="Student's first name"),
        inquirer.Text("LastName", message="Student's last name"),
        inquirer.Text("Age", message="Student's age"),
        inquirer.Text("CellphoneNum", message="Student's cellphone number (+989123456789)",
                      validate=phone_validation),
        inquirer.List("SaveConfirmation", message="Are you sure to save this student?", choices=["yes", "no"],
                      default="no"),
    ]
    answers = inquirer.prompt(student)
    return answers


def modify_student(option):
    if option == 'u':
        search = [
            inquirer.Text("get_id",
                          message="Please enter student ID",
                          ),
        ]
        student_id = inquirer.prompt(search)
        student = Student.get(Student.student_id == student_id['get_id'])
        change = [
            inquirer.List('field',
                          message='Which field you want change?',
                          choices=[
                              ("First name", "f"),
                              ("Last name", "l"),
                              ("Phone number ", "p"),
                              ('Age', 'a'),
                          ],
                          )
        ]
        field = inquirer.prompt(change)
        if field['field'] == 'f':
            questions = [
                inquirer.Text("name",
                              message=f"Student's first name is {student.first_name}.Please enter your changes")]
            change_name = inquirer.prompt(questions)
            student.first_name = change_name['name']
            student.save()
        if field['field'] == 'l':
            questions = [
                inquirer.Text("lname",
                              message=f"Student's first name is {student.last_name}.Please enter your changes")]
            change_lname = inquirer.prompt(questions)
            student.last_name = change_lname['lname']
            student.save()
        if field['field'] == 'p':
            questions = [
                inquirer.Text("phone_num",
                              message=f"Student's phone number is {student.phone_num}.Please enter your changes")]
            change_phone = inquirer.prompt(questions)
            student.phone_num = change_phone['phone_num']
            student.save()
        if field['field'] == 'a':
            questions = [
                inquirer.Text("age", message=f"Student's age is {student.age}.Please enter your changes")]
            change_age = inquirer.prompt(questions)
            student.age = change_age['age']
            student.save()

    if option == 'd':
        search = [
            inquirer.List('field',
                          message='Enter which field you want to search with',
                          choices=[
                              ("First name", "f"),
                              ("Last name", "l"),
                              ("Phone number ", "p"),
                              ("Age", "a"),
                              ('ID', "id")
                          ],
                          )
        ]
        search_field = inquirer.prompt(search)
        if search_field['field'] == 'f':
            questions = [
                inquirer.Text("name",
                              message="Please enter their first name")]
            name = inquirer.prompt(questions)
            query = Student.select().where(Student.first_name == name['name'])
            for s in query:
                s.delete_instance()
        if search_field['field'] == 'l':
            questions = [
                inquirer.Text("lname",
                              message="Please enter their last name")]
            lname = inquirer.prompt(questions)
            query = Student.select().where(Student.last_name == lname['lname'])
            for s in query:
                s.delete_instance()
        if search_field['field'] == 'p':
            questions = [
                inquirer.Text("phone_num",
                              message="What's the student's cellphone number?")]
            phone = inquirer.prompt(questions)
            query = Student.select().where(Student.phone_num == phone['phone_num'])
            for s in query:
                s.delete_instance()
        if search_field['field'] == 'a':
            questions = [
                inquirer.Text("age", message="How old are these students that you want to delete them")]
            age = inquirer.prompt(questions)
            query = Student.select().where(Student.age == age['age'])
            for s in query:
                print(s.student_id)
                s.delete_instance()


def show_student():
    search = [
        inquirer.List('field',
                      message='Enter which field you want to search with',
                      choices=[
                          ("First name", "f"),
                          ("Last name", "l"),
                          ("Phone number ", "p"),
                          ("Age", "a"),
                          ('ID', "id")
                      ],
                      )
    ]
    search_field = inquirer.prompt(search)
    if search_field['field'] == 'f':
        questions = [
            inquirer.Text("name",
                          message="Please enter their first name")]
        name = inquirer.prompt(questions)
        query = Student.select().where(Student.first_name == name['name'])
        for s in query:
            print(f'{s.first_name} {s.last_name}: {s.student_id}')
    if search_field['field'] == 'l':
        questions = [
            inquirer.Text("lname",
                          message="Please enter their last name")]
        lname = inquirer.prompt(questions)
        query = Student.select().where(Student.last_name == lname['lname'])
        for s in query:
            print(f'{s.first_name} {s.last_name}: {s.student_id}')
    if search_field['field'] == 'p':
        questions = [
            inquirer.Text("phone_num",
                          message="What's the student's cellphone number?")]
        phone = inquirer.prompt(questions)
        query = Student.select().where(Student.phone_num == phone['phone_num'])
        for s in query:
            print(f'{s.first_name} {s.last_name}: {s.student_id}')
    if search_field['field'] == 'a':
        questions = [
            inquirer.Text("age", message="How old are these students that you want to show them")]
        age = inquirer.prompt(questions)
        query = Student.select().where(Student.age == age['age'])
        for s in query:
            print(f'{s.first_name} {s.last_name}: {s.student_id}')


start = [
    inquirer.List("start",
                  message="Please choose an option",
                  choices=[
                      ("Add new student", "a"),
                      ("Modify available students", "m"),
                      ("Show information of available students ", "s"),
                  ],

                  ),
]
answers = inquirer.prompt(start)
if answers["start"] == 'a':
    f = add_student()
    new_student = Student.create(first_name=f["FirstName"], last_name=f["LastName"],
                                 age=f["Age"], phone_num=f["CellphoneNum"],
                                 student_id=random.randrange(1110, 9999))

if answers["start"] == 'm':
    modify_options = [
        inquirer.List("modify",
                      message="Please choose an option",
                      choices=[
                          ("Delete", "d"),
                          ("Update", "u"),
                      ],

                      ),
    ]

    mod = inquirer.prompt(modify_options)
    modify_student(mod['modify'])

if answers["start"] == 's':
    show_student()

db.close()
