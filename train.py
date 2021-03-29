import face_recognition
import os
import pickle
import pathlib
import glob


class Train:
    def __init__(self):
        self.FACES_DIR = 'Faces'
        self.faces = []
        self.names = []

    def train(self):
        print('starting...')

        # we train the images in each sub-folder of the FACES-DIR, also each sub-folder's name is the name of the person
        for name in os.listdir(self.FACES_DIR):

            for filename in os.listdir(f'{self.FACES_DIR}/{name}'):

                # we load the image
                image = face_recognition.load_image_file(f'{self.FACES_DIR}/{name}/{filename}')

                # return the encoding of the first face it finds in an nd-array
                encoding = face_recognition.face_encodings(image)[0]

                # we append the encodings and its name
                self.faces.append(encoding)
                self.names.append(name)
        # we store the encodings and the names in a pkl file
        pickle.dump(self.faces, open("faces_encoding.pkl", "wb"))
        pickle.dump(self.names, open("student_names.pkl", "wb"))

    def train_latest_student(self):
        print('starting...')
        self.read_training_data()
        latest_file = self.get_latest_file_name()


        # we train the images in the new added person only, and not the whole dataset

        for filename in os.listdir(f'{self.FACES_DIR}/{latest_file}'):

                # we load the image
                image = face_recognition.load_image_file(f'{self.FACES_DIR}/{latest_file}/{filename}')

                # return the encoding of the first face it finds in an nd-array
                encoding = face_recognition.face_encodings(image)[0]

                # we append the encodings and its name
                self.faces.append(encoding)
                self.names.append(latest_file)
        # we store the encodings and the names in a pkl file
        pickle.dump(self.faces, open("faces_encoding.pkl", "wb"))
        pickle.dump(self.names, open("student_names.pkl", "wb"))

    def get_latest_file_name(self):
        list_of_files = glob.glob(f"{pathlib.Path(__file__).parent.absolute()}\Faces\*")  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        only_file_name = latest_file[::-1].split('\\', 1)
        only_file_name = only_file_name[0]
        return only_file_name[::-1]

    def read_training_data(self, faces_file_location="faces_encoding.pkl", names_file_location="student_names.pkl"):
        self.faces = pickle.load(open(faces_file_location, "rb"))
        self.names = pickle.load(open(names_file_location, "rb"))

