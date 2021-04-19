from platform import system as operating_system
import sys
import os
import cv2
import youtube_dl
from glob import glob
from ffpyplayer.player import MediaPlayer

def download(x, pasted=""):
    with x as ydl:
        try:
            # attempts to download for the provided link
            if pasted != "":
                ydl.download([pasted])
            else:    
                ydl.download([sys.argv[1]])
        except :
            # attempts to download a defaulted url
            # its an LTT video
            ydl.download(['https://www.youtube.com/watch?v=S8kaMQuqnLM&t=81s'])

def locate(pasted=""):
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
    # attempts to download a file
    try:
        download(youtube_dl.YoutubeDL(ydl_opts), pasted)
    except :
        # sometimes ssl fails this fixes that
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        download(youtube_dl.YoutubeDL(ydl_opts), pasted)        

    # returns a cv object
    return cv2.VideoCapture(f'vid.mp4')

if __name__ == '__main__':
    print(sys.argv)
    locate()    
