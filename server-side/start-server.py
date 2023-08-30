import subprocess
import pandas as pd
import numpy as np
import datetime

def get_current_date_time() -> tuple:
    '''Gets the current date and time stamp, converts to string and returns both'''
    date_time = datetime.datetime.now()
    return (str(date_time.date()), str(date_time.time()))

def init_attendance_today(students_csv, attendance_csv, attendance_csv_path) -> None:
    date, _ = get_current_date_time()
    for student in students_csv['unique_identifier']:
        attendance_csv.loc[student] = [student.split('-')[0], date, np.nan, False]
    attendance_csv.to_csv(attendance_csv_path, index=True) # Saving the new data

def handle_initial_setup(students_csv_path, attendance_csv_path):
    students_csv = pd.read_csv(students_csv_path)
    attendance_csv = pd.read_csv(attendance_csv_path).set_index('unique_identifier')

    while True:
        init_attendence_status = input(f'\nDo you want to initialize attendance for today? (y/n): ')
        init_attendence_status = init_attendence_status.lower()
        if init_attendence_status == 'y':
            init_attendance_today(students_csv, attendance_csv, attendance_csv_path)
            print('Attendance initialized for all students with default absent. Attendance will be made present as students are identified!')
            break
        elif init_attendence_status == 'n':
            break
        else:
            print(f'Enter a valid command - y/n')
    print()


if __name__ == "__main__":

    handle_initial_setup(
        students_csv_path = './database/students.csv',
        attendance_csv_path = './database/attendance.csv'
    )
            
    uvicorn_command = "uvicorn server:app --reload"  # Replace 'working' with your script's filename
    subprocess.run(uvicorn_command, shell=True)
