import pickle
from modules.session.session import start_session

with open('./multiple_angles_faces_encodings', 'rb') as file:
    data = pickle.load(file)

ids, encodings_list = [], []
for id, encodings in data.items():
    for _ in range(5):
        ids.append(id)
    encodings_list.extend(encodings)

start_session(encodings_list, ids, 'hog', 'small')