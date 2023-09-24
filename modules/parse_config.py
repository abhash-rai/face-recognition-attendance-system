import json

def parse_config_file(config_file_path):

    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)

    server = config_data['server']
    username = config_data['username']
    password = config_data['password']
    database = config_data['database']
    personnel_table_name = config_data['personnel_table_name']
    attendance_table_name = config_data['attendance_table_name']
    mysql_unknown_name_table = config_data['mysql_unknown_name_table']

    return server, username, password, database, personnel_table_name, attendance_table_name, mysql_unknown_name_table
