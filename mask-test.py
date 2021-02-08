import cv2
import os
import sys
from platform import system as operating_system


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = None

if operating_system() != 'Darwin' and len(sys.argv) > 0: # for the macs
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

        # url = input('Enter a youtube URL, if not a valid one one will be provided')
        url = ""
        ydl_opts = {
            'outtmpl': 'vid',
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                try:
                    ydl.download([url])
                except :
                    ydl.download(['https://www.youtube.com/watch?v=ZX7HnNd5PB4'])
            except :
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                try:
                    ydl.download([url])
                except :
                    ydl.download(['https://www.youtube.com/watch?v=ZX7HnNd5PB4'])
    
    file = ''
    for i in '3gp,aac,flv,m4a,mp3,mp4,ogg,wav,webm,mkv'.split(','):
        for j in glob(f'*.{i}'):
            file = f'{j}'

    cap = cv2.VideoCapture(file)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'edit_{file}',fourcc, 5, (1280,720))

    print('shrinking file')

    while True:
        ret, frame = cap.read()
        if ret == True:
            b = cv2.resize(frame,(1024,576),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
            out.write(b)
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    video_capture = cv2.VideoCapture(f'{file}')
 


print('begining loop you might have to alt tab out')
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    faces = faceCascade.detectMultiScale(        cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
        scaleFactor=5,
        minNeighbors=1,
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
