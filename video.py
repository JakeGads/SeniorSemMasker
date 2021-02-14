from platform import system as operating_system
import sys
import os
import cv2

def locate():
    
    if operating_system() != 'Darwin' and len(sys.argv) < 1: # for the macs
        # for camera, It doesn't work on MacOS cause of security features
        return cv2.VideoCapture(0)
    else:
        import youtube_dl
        from glob import glob
        # Downloads a youtube video
        
        for i in glob('*.webm'):
            os.remove(i)

        ydl_opts = {
            'outtmpl': 'vid.mp4',
            'format': 'best[height<=480]',
            'audio-format': 'mp3'
        }
    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                try:
                    ydl.download([sys.argv[1]])
                except :
                    ydl.download(['https://www.youtube.com/watch?v=ZX7HnNd5PB4'])
            except :
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                try:
                    ydl.download([sys.argv[1]])
                except :
                    ydl.download(['https://www.youtube.com/watch?v=ZX7HnNd5PB4'])
        
        file = ''
        
        for i in '3gp,aac,flv,m4a,mp3,mp4,ogg,wav,webm,mkv'.split(','):
            for j in glob(f'*.{i}'):
                file = f'{j}'

        print(file)
        return cv2.VideoCapture(f'{file}')

if __name__ == '__main__':
    print(sys.argv)
    locate()    
