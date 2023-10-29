
# Prerequisites

<br>

Before you begin, ensure that you meet the following requirements:

- `Python 3`: You must have Python 3 installed on your system.
- `Git`: Ensure that Git is installed on your system.


# Installation

<br>

`Note:` If dlib is not installed, you can install it from here: [https://github.com/sachadee/Dlib/](https://github.com/sachadee/Dlib/) 
  
1. Clone the repository (In terminal):

   ``` 
   git clone https://github.com/AbhashChamlingRai/traffic-congestion-detector.git
   ``` 

2. Create a virtual environment:

   ``` 
   python -m venv myenv
   ``` 

3. Activate the virtual environment:

   ``` 
   myenv\Scripts\activate
   ``` 

4. Navigate to the directory requirements.txt file is located.

   ``` 
   cd <path_to_directory>
   ``` 

6. Install the required dependencies:

   ``` 
   pip install -r requirements.txt
   ``` 
   

# Usage

<br>

1. Configure the 'Config.json' file

    In the 'Config.json' file, replace only the first four placeholder values with your MySQL server IP, username, password, and database name.

<br>

2. Add face images

    All the images to encode should be inside `to_encode_faces` folder on following format `(where each sub-folder of to_encode_faces is information regardng a person)`: 

    ```
    to_encode/
    ├── <person_1_id>-<university>-<first_name>-<last_name>/
    │   ├── front.jpg
    │   ├── down.jpg
    │   ├── up.jpg
    │   ├── left.jpg
    │   └── right.jpg
    ├── <person_2_id>-<university>-<first_name>-<last_name>/
    │   ├── front.jpg
    │   ├── down.jpg
    │   ├── up.jpg
    │   ├── left.jpg
    │   └── right.jpg
    ├── <person_3_id>-<university>-<first_name>-<last_name>/
    │   ├── front.jpg
    │   ├── down.jpg
    │   ├── up.jpg
    │   ├── left.jpg
    │   └── right.jpg
    └── ...
    ```

    `front.jpg`, `down.jpg`, `up.jpg`, `left.jpg`, and `right.jpg` are the different angles images of a person.

    Don't keep `<` or `>` in the folder name! It is used to denote a variable which can have different values. The folder should be named like: 23140736-BCU-ABHASH-RAI

<br>

3. Validate and generate encodings

    Before generating encodings, it is recommended to validate the images to ensure that only one face is detected in every face angle. Run all cells in `validateData_generateEncodings.ipynb` to process the images and generate encodings the faces. If you can't detect a single face in every image, then replace the faulty image, and redo step 3. 

<br>

4. Run start.py 

    ``` 
    python start.py
    ``` 

    **Certain parameters can be changed in `start.py`:**
    
    ```Python
    session = Session(
        face_encodings_path = stored_face_encodings_path,
        unknwon_face_store_location = unknwon_face_store_location,
        face_location_model='hog', #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        face_encoding_model = 'small', #'large' model has better accuracy but is slower, 'small' model is faster
        time_between_entry_exit = 3
    )
    ``` 
    - `face_location_model`: This parameter specifies the method used for detecting faces in an image. In your code, there are two options:
        - 'hog': This method is a Histogram of Oriented Gradients (HOG) face detection model. It is faster but less accurate than the 'cnn' model. It runs on the CPU.
        - 'cnn': This model uses Convolutional Neural Networks (CNNs) for face detection. It offers better accuracy but is computationally more intensive and typically runs on a GPU for faster processing.
        
    - `face_encoding_model`: This parameter determines the model used for encoding facial features after face detection. In your code, there are two options:
        - 'small': This model is smaller and faster but may have slightly lower accuracy in encoding facial features.
        - 'large': This model is larger and slower but provides higher accuracy in encoding facial features.

    - `time_between_entry_exit`: This parameter specifies the time interval (in seconds) that must pass between two consecutive entry or exit events. It is used to control how frequently entry and exit events can be registered.
  
    ```Python
    session.start_session(
        camera_index=0, 
        show_preview=True, 
        scale_frame=0.77, 
        desired_fps=2, 
        tolerance=0.45
    )
    ```

    - `camera_index`: This parameter specifies the index of the camera or webcam to use for capturing video frames. In your code, it is set to 0, which typically refers to the default camera if you have multiple cameras connected to your system.

    - `show_preview`: This parameter is a boolean flag that determines whether a live video preview will be displayed while the session is running.
If set to True, a live video preview will be shown.
If set to False, there will be no video preview, but the system will still process frames in the background for face recognition and attendance tracking.

    - `scale_frame`: This parameter determines the scaling factor for resizing video frames. In your code, it is set to 0.77. This means that each frame will be resized to 77% of its original size. Resizing frames can help reduce computational load and improve processing speed.

    - `desired_fps`: This parameter specifies the desired frames per second (FPS) for capturing and processing video frames. In your code, it is set to 2 FPS, meaning that the system will aim to process 2 frames per second.

    - `tolerance`: This parameter controls the level of tolerance in face recognition. It is typically used to determine how closely a detected face must match a known face in order to be considered a match. In your code, it is set to 0.45, which means that a match is considered if the similarity score between the detected face and a known face is greater than or equal to 0.45.
  
<br>
