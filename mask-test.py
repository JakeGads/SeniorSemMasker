import cv2
import os
from platform import system as operating_system


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = None

if operating_system() != 'Darwin': # for the macs
    # for camera, It doesn't work on MacOS cause of security features
    video_capture = cv2.VideoCapture(0)
else:
    import youtube_dl
    from glob import glob
    # Downloads a youtube video
    
    for i in glob('*.webm'):
        os.remove(i)

    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        url = input('Enter a youtube URL, if not a valid one one will be provided')
        try:
            ydl.download([url])
        except :
            ydl.download(['https://www.youtube.com/watch?v=DXo2m_XlH4s'])
    
    
    
    video_capture = cv2.VideoCapture()

print('begining loop you might have to alt tab out')
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
