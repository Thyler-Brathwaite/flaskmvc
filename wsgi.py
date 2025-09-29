import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, student, staff, serviceLog, accolade, leaderboard)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    rickFlag = student(name="Rick Sanchez", email="", totalHours=60)
    christopherSmith = student(name="Christopher Smith", email="", totalHours=20)
    emiliaHarcourt = student(name="Emilia Harcourt", email="", totalHours=10)
    harleyQuinn = student(name="Harley Quinn", email="", totalHours=40)
    leaderboard1 = leaderboard(id=1)
    adrianChase = staff(name="Adrian Chase", email="", role="Coordinator")
    leotaAdebayo = staff(name="Leota Adebayo", email="", role="Supervisor")
    accolade1 = accolade(name="Bronze", lower=0, upper=10)
    accolade2 = accolade(name="Silver", lower=25, upper=49)
    accolade3 = accolade(name="Gold", lower=50, upper=100)

    db.session.add(accolade1)
    db.session.add(accolade2)
    db.session.add(accolade3)
    db.session.add(leotaAdebayo)
    db.session.add(adrianChase)
    db.session.add(rickFlag)
    db.session.add(christopherSmith)
    db.session.add(emiliaHarcourt)
    db.session.add(harleyQuinn)
    db.session.add(leaderboard1)
    db.session.commit()

    print('database intialized')

@app.cli.command("log-hours", help="helps a staff log hours for a student")
def log_hours():
    studentid = input("Enter student ID: ")
    staffid = input("Enter staff ID: ")
    date = input("Enter date (YYYY-MM-DD): ")
    hours = input("Enter number of hours: ")
    
    staff_member = staff.query.get(staffid)
    if staff_member:
        new_log = staff_member.log_hours(studentid, date, int(hours))
        print(f"Logged {hours} hours for student ID {studentid} on {date}. Log ID: {new_log.log_id}")

@app.cli.command("request-confirm", help="helps a student request confirmation for logged hours")
def request_confirm():
    studentid = input("Enter your student ID: ")
    logid = input("Enter the log ID to request confirmation for: ")
    
    student_member = student.query.get(studentid)
    if student_member:
        result = student_member.request_confirmation(int(logid))
        print(result)


@app.cli.command("view-leaderboard", help="helps a user view the leaderboard")
def view_leaderboard_stud():
    leaderboard_id = input("Enter the leaderboard ID to view: ")
    
    board = leaderboard.query.get(leaderboard_id)
    if board:
        board.rank_students()
    else:
        print("Leaderboard not found")
    


@app.cli.command("view-accolade", help="helps a student see their earned accolades")
def view_accodale():
    studentid = input("Enter your student ID: ")
    
    student_member = student.query.get(studentid)
    if student_member:
        accolades = student_member.view_accolades()
        print("Earned Accolades:")
        for acc in accolades:
            print(f"- {acc['name']} ({acc['range']})")

@app.cli.command("confirm-hours", help="helps a staff confirm logged hours for a student")
def confirm_hours():
    staffid = input("Enter your staff ID: ")
    logid = input("Enter the log ID to confirm: ")
    
    staff_member = staff.query.get(staffid)
    if staff_member:
        staff_member.confirm_hours(int(logid))
        print(f"Confirmed hours for log ID {logid}.")

@app.cli.command("view-students", help="helps a staff view all students")
def view_students():
    all_students = student.query.all()
    print("Students:")
    for stud in all_students:
        print(f"- ID: {stud.student_id}, Name: {stud.name}, Email: {stud.email}, Total Hours: {stud.totalHours}")


@app.cli.command("view-staff", help="helps a staff student view all staff")
def view_staff():
    all_staff = staff.query.all()
    print("Staff Members:")
    for stf in all_staff:
        print(f"- ID: {stf.staff_id}, Name: {stf.name}, Email: {stf.email}, Role: {stf.role}")

@app.cli.command("view-logs", help="helps a staff view all service logs")
def view_logs():
    all_logs = serviceLog.query.all()
    print("Service Logs:")
    for log in all_logs:
        print(f"- Log ID: {log.log_id}, Student ID: {log.student_id}, Staff ID: {log.staff_id}, Date: {log.date}, Hours: {log.hours}, Status: {log.status}")

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)