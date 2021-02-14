import cv2

from video import locate


video_capture = locate()    

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    faces = cascade.detectMultiScale(        
        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
        scaleFactor=5,
        minNeighbors=1
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
        

    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    


    if cv2.waitKey(4) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
