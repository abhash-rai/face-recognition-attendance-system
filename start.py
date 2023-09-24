from modules.parse_config import parse_config_file
from modules.connect_mysql import connect_mysql_database
from modules.setup_msql import setup_mysql_db
from modules.populate_personnel_table import make_personnel_entry
from modules.face_recognition_attendance import Session




# Path to files
stored_face_encodings_path = './encodings/multiple_angles_faces_encodings'
config_file_path = './config.json'
unknwon_face_store_location = './unidentified_faces'




# Getting all MySQL server information
server, username, password, database, personnel_table_name, attendance_table_name, mysql_unknown_name_table = parse_config_file(config_file_path)

# Creating MySQL connection and cursor
connection, cursor = connect_mysql_database(server, username, password)

# Setting up MySQL Server database
setup_mysql_db(cursor, database, personnel_table_name, attendance_table_name, mysql_unknown_name_table)

# Populating personnel table to enable initilization of attendance table and making attendance
make_personnel_entry(
    pickle_encodings_path = stored_face_encodings_path, 
    connection = connection, 
    cursor = cursor, 
    database_name = database, 
    personnel_table_name = personnel_table_name
)

# Closing connection and cursor
connection.close()
cursor.close()







# Setting up session
session = Session(
    face_encodings_path = stored_face_encodings_path,
    unknwon_face_store_location = unknwon_face_store_location,
    face_location_model='hog', #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
    face_encoding_model = 'small', #'large' model has better accuracy but is slower, 'small' model is faster
    time_between_entry_exit = 3
)

# Connection to MySQL database server
session.connect_mysql_database(
    server = server,
    username = username,
    password = password,
    database = database,
    personnel_table_name = personnel_table_name, 
    attendance_table_name = attendance_table_name, 
    mysql_unknown_name_table = mysql_unknown_name_table
) 

# Initializing attendance in the 'attendance' table for the current date (only if it is not already initialized) with every individual in the 'personnel' table as absent by default
session.initialize_attendance_today()

# Setting parameters and running session
session.start_session(
    camera_index=0, 
    show_preview=True, # If false preview is not shown, but attendance will be made according to recognized face in the background
    scale_frame=0.77, 
    desired_fps=2, 
    tolerance=0.45
)