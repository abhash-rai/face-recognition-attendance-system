import pandas as pd
import numpy as np
import datetime

class Server:

    def __init__(self):

        self.__students_csv_path = './database/students.csv'
        self.__students_csv = pd.read_csv(self.__students_csv_path)

        self.__attendance_csv_path = './database/attendance.csv'
        self.__attendance_csv = pd.read_csv(self.__attendance_csv_path).set_index('unique_identifier')
    
    def get_current_date_time(self) -> tuple:
        '''Gets the current date and time stamp, converts to string and returns both'''
        date_time = datetime.datetime.now()
        return (str(date_time.date()), str(date_time.time()))

    def init_attendance_today(self) -> None:
        date, _ = self.get_current_date_time()
        for student in self.__students_csv['unique_identifier']:
            self.__attendance_csv.loc[student] = [student.split('-')[0], date, np.nan, False]
        self.__attendance_csv.to_csv(self.__attendance_csv_path, index=True) # Saving the new data

    def recieve_identified_ids_timestamps(self) -> dict:
        '''Recieves json/dict and returns it'''
        pass

    def make_attendance(self, student_id_time_dict: dict) -> None:
        '''Iterates over the given dict items and makes attendance'''
        for unique_identifier, time in student_id_time_dict.items():
            if self.__attendance_csv.loc[unique_identifier,'attendance'] == False:
                self.__attendance_csv.loc[unique_identifier,'time'] = time
                self.__attendance_csv.loc[unique_identifier,'attendance'] = True
        self.__attendance_csv.to_csv(self.__attendance_csv_path, index=True) # Saving the new data
        print(self.__attendance_csv)


server = Server()
# server.init_attendance_today()
# server.make_attendance({'23140736-BCU':'10am'})