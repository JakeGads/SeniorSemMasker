import cv2
from datetime import datetime
from video import locate

# how many microseconds for a frame in 30fps
thirty_fps_as_ms = 19900
# how many times its allowed to do a switch
max_skip = 17999

def get_curr_time():
    '''returns the current secode + microsecond as microseconds'''
    return (datetime.now().second * 1_000_000) + (datetime.now().microsecond)


def main():
    # fetches the video through youtube-dl
    video_capture = locate()    

    # builds a facial casscade from
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # runs for every frame
    while True:
        # loops start time
        start = get_curr_time()
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # looks for faces in the frame
        faces = cascade.detectMultiScale(        
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), # converts the frame to B/W 
            scaleFactor=5, # large possibility
            minNeighbors=1 # very loose definition on what a face 
        )

        # Draw a rectangle around the faces
        # TODO make this place an image instead
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
            

        # Display the resulting frame
        cv2.imshow('Video', frame)
        
        skip = 0 # the amount of skips
        for i in range(max_skip):
            # calculates the difference between the booted time
            # and the time at this point
            dif = get_curr_time() - start
            # check if we are inside the desired range
            if dif < thirty_fps_as_ms:
                continue
            else:
                break
        

        # quit button
        if cv2.waitKey(4) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    # clear the ram
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    