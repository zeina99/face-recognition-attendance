import face_recognition
import cv2
import pickle


class Recognize:
    def __init__(self, tolerance=0.5, frame_width=3, font_width=2, model='hog'):
        self.recognized_names = []
        self.cap = cv2.VideoCapture(0)
        self.TOLERANCE = tolerance
        self.FRAME_WIDTH = frame_width
        self.FONT_WIDTH = font_width
        self.MODEL = model  # model either 'hog' or 'cnn' (cnn takes more time than hog)
        

    def read_training_data(self, faces_file_location="faces_encoding.pkl", names_file_location="student_names.pkl"):
        self.known_faces=pickle.load(open(faces_file_location, "rb"))
        self.known_names=pickle.load(open(names_file_location, "rb"))

    def recognize(self):
        while True:

            ret, image = self.cap.read()

            # get the location of each face in the frame which we named as image here
            locations = face_recognition.face_locations(image, model=self.MODEL)

            # now we pass the frame(image) and the location of faces in that frame to the recognition function
            encodings = face_recognition.face_encodings(image, locations)

            # convert from rgb to bgr since opencv uses bgr
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            for face_encoding, face_location in zip(encodings, locations):

                # utilise compare faces function to compare faces in frame to the training data, returns true or false list
                results = face_recognition.compare_faces(self.known_faces, face_encoding, self.TOLERANCE)

                #  if face was found then get the index, since it's ordered
                match = None
                if True in results:  # If at least one is true, get a name of first of found labels
                    match = self.known_names[results.index(True)]
                    print(f' - {match} from {results}')

                    #add the match to a recognized faces list
                    if match not in self.recognized_names:
                        self.recognized_names.append(match)

                    # the positions in order: top, right, bottom, left
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])

                    # set frame color
                    color = [255,0,0]

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, self.FRAME_WIDTH)

                    # Now we need smaller, filled frame below for a name
                    # This time we use bottom in both corners - to start from bottom and move 50 pixels down
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)

                    # Paint frame
                    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

                    # Wite a name
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), self.FONT_WIDTH)

            # Show image
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            image = cv2.rectangle(image, (0, 500), (250, 400), (255, 0, 0), -1)
            image = cv2.putText(image, 'Press q when recognized', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), self.FONT_WIDTH, )
            cv2.imshow("Recognition", image)
            if cv2.waitKey(10) & 0xFF == ord("q"):
              break
        
        cv2.destroyWindow("Recognition")
        return self.recognized_names
#
#
# recognizer = Recognize()
# recognizer.read_training_data()
# recognizer.recognize()