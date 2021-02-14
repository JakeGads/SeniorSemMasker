from platform import system as operating_system
import sys
import os
import cv2
import youtube_dl
from glob import glob

def download():
    try:
        # attempts to download for the provided link
        ydl.download([sys.argv[1]])
    except :
        # attempts to download a defaulted url
        # its an LTT video
        ydl.download(['https://www.youtube.com/watch?v=ZX7HnNd5PB4'])

def locate():
    '''finds a video file for analysis''''    
    if operating_system() != 'Darwin' and len(sys.argv) < 1: # for the macs
        # for camera, It doesn't work on MacOS cause of security features
        return cv2.VideoCapture(0)
    else:
        # Downloads a youtube video
        
        for i in glob('*.webm'):
            os.remove(i)

        # options for the youtube downloader
        ydl_opts = {
            'outtmpl': 'vid.mp4', # saves the file as, defaults to that extent
            'format': 'best[height<=480]', # dowloads as the best format at 480p (makes things go faster)
            'audio-format': 'mp3' # caches the audio mp3 because its complaint 
        }
    
        # uses the options in "safe mode"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # attempts to download a file
            try:
                download()
            except :
                # sometimes ssl fails this fixes that
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                download()        
        
        # returns a cv object
        return cv2.VideoCapture(f'vid.mp4')

if __name__ == '__main__':
    print(sys.argv)
    locate()    
