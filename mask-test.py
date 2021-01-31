import cv2
import sys

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# for camera, It doesn't work on MacOS cause of security features
# video_capture = cv2.VideoCapture(0)

# hence we are using a new version
video_capture = cv2.VideoCapture('linus.webm')

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    faces = faceCascade.detectMultiScale(
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
        scaleFactor=2,
        minNeighbors=4,
        minSize=(10, 10),
        maxSize=(30,30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(45) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
