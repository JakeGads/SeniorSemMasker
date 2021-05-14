import cv2
import numpy as np
from datetime import datetime
from video import locate
from ffpyplayer.player import MediaPlayer
import os

# how many microseconds for a frame in (slightly less then) 30fps
# we manually build in the skip becuase the face finding algorithm are variable 
thirty_fps_as_ms = int(30.00 * 1000)

def get_current_time():
    '''returns the current secode + microsecond as microseconds'''
    return (datetime.now().second * 1_000_000) + (datetime.now().microsecond)

def overlay(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background
       
def main(pasted:str=""):
    # fetches the video through youtube-dl
    video_capture = locate(pasted)
    # builds the audio caption
    audio_capture = MediaPlayer('vid.mp4')     

    # builds a facial cascade from
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # a cv image of of a mask (large so it an be downward)
    mask = cv2.imread('mask.png', cv2.IMREAD_UNCHANGED)
    # runs for every frame
    count = -1

    while True:
        count += 1
        # loops start time
        start = get_current_time()
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        if not ret:
            break

        # looks for faces in the frame
        faces = cascade.detectMultiScale(        
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), # converts the frame to B/W 
            scaleFactor=2   , # strict so to avoid asmaller face size 
            minNeighbors=1 # very loose definition on what a face 
        )

        # places image
        for (x, y, w, h) in faces:
            # resized masks
            resized = cv2.resize(mask, (int(w/1.4), int(h/1.4)), interpolation = cv2.INTER_AREA)
            # overlay the mask
            frame = overlay(frame, resized, int(x + w/7), int(y + h/3))
            # debug (allows for for you to see the found faces)
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 5)
            # Display the resulting frame


        audio_frame, val = audio_capture.get_frame()
        if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame


        # shows the frame
        cv2.imshow('Video', frame)

        # plays the audio
        

        for i in range(thirty_fps_as_ms):
            # calculates the difference between the booted time
            # and the time at this point
            dif = get_current_time() - start
            # check if we are inside the desired range
            if dif < thirty_fps_as_ms:
                continue
            else:
                # commented out for debugging purposes
                # print(f'{count}\t{int((i/thirty_fps_as_ms) * 100)}')
                break
        
        
        # quit button
        if cv2.waitKey(4) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    # clear the ram
    cv2.destroyAllWindows()
    # deletes the file
    os.remove('vid.mp4')


if __name__ == "__main__":
    main()
    