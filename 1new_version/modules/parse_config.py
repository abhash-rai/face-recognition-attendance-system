import json

def parse_config_file(config_file_path):

    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)

    server = config_data['server']
    username = config_data['username']
    password = config_data['password']
    database = config_data['database']

    return server, username, password, database
