from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pygame import mixer
import os
import sys
import random
import threading
import time
import mutagen
from mutagen.id3 import ID3 
from mutagen.mp3 import MP3 

# TITLE UPDATOR
# RANDOMIZE SONG TOGGLE
# Add a queue system 

""" 
I DIDN"T USE CLASSES BC IM STUPID AND DONT KNOW HOW TO USE THEM WELL.
I used pygame to intialize the music. 
The os library to check if the files in the folder are mp3 or mp4 and to search through the file
PyQt5 to make the gui and assign the Buttons, Slider and ProgressBar
Then more pygame music methods to detect things such as get_length or get_volume. 
                                    TO USE
1. Make sure you have pygame installed (pip install pygame) and PyQt5 installed (pip install PyQt5)
2. Add Music Files (.mp3 and .mp4 and .wav files) into the Music Playlist folder.
3. Run and Enjoy.  
"""
def get_mutagen(path):

    SongData.clear()

    audio = ID3(path) #path: path to file
    SongData.append(ID3(song_playlist + Music_Names)['TPE1'].text[0]) # Author 
    SongData.append(audio['TDRC'].text[0]) # Date

    
    total_length = mixer.Sound(path).get_length() # length of the Song in seconds
    mins, secs = divmod(total_length, 60)
    timeformat = '{:02d}:{:02d}'.format(round(mins), round(secs))
    print(timeformat)
    



global currentSong, status, shuffleStatus 
shuffleStatus = False 
status = "stopped"
currentSong = 0
song_playlist = "C:/Users/evync/Documents/code/For Fun/Music Player App/Music Playlist/"
Music_Names = []
SongData = []
# Populates the Music File Names into the Music_Names list. 
for file in os.listdir(song_playlist[:-1]): # Folder within the folder than holds the songs 
    if file.endswith(".mp3" or ".mp4" or ".wav"): # Only adds the song if it's a music file
        Music_Names.append(str(file)) 
 #path: path to file


# Prints out all the tags 
# TIT2 is the title of the song
# TPE1 is the author of the song 
# they are keys of a dictionary 
        
def main():
    global status
    global currentSong

    app = QApplication(sys.argv)
    
    window = QWidget()
    window.setWindowTitle('Music Player')
    window.setGeometry(0,0, 500, 500)  
    window.setWindowIcon(QIcon('C:/Users/evync/Documents/code/For Fun/Music Player App/musicplayer.png'))
    window.move(710, 290)
    window.setStyleSheet(
        'background-color: black;')   
    window.setWindowFlags(Qt.WindowStaysOnTopHint)

    if len(Music_Names) == 0: 
        print("Make sure there are songs in the folder Or the paths are all correct.")
        sys.exit(app.exec_())

    mixer.init()
    mixer.music.load(song_playlist + Music_Names[currentSong])
    mixer.music.set_volume(0)
    mixer.music.play()
    mixer.music.pause()
    mixer.music.set_volume(0.5)

    previous = QPushButton('\u23EA', window)
    previous.setGeometry(150, 400, 50, 50)
    previous.setStyleSheet(
        'color: white;'
        'font-size: 45px;') 

    play_pause = QPushButton('\u23EF', window)
    play_pause.setGeometry(225,400,50,50)
    play_pause.setStyleSheet(
        'border-radius: 16px;'
        'font-size: 45px;') 

    next = QPushButton('\u23E9', window)
    next.setGeometry(300,400,50,50)
    next.setStyleSheet(
        'border-radius: 16px;'
        'font-size: 45px;') 

    shuffle = QPushButton('\U0001F500', window)
    shuffle.setGeometry(375,400,50,50)
    shuffle.setStyleSheet(
        'border-radius: 16px;'
        'font-size: 45px;') 

    restart = QPushButton('\U0001F504', window)
    restart.setGeometry(75,400,50,50)
    restart.setStyleSheet(
        'border-radius: 16px;'
        'font-size: 45px;') 

    lbl = QLabel(window)
    lbl.setPixmap(QPixmap('C:/Users/evync/Documents/code/For Fun/Music Player App/musicplayer.png').scaled(50, 50, Qt.KeepAspectRatio, Qt.FastTransformation))
    lbl.move(25, 25)
    lbl.show() 

    speaker = QPushButton('\U0001F50A', window)
    speaker.setGeometry(425,25,50,50)
    speaker.setStyleSheet(
        'border-radius: 16px;'
        'font-size: 45px;') 

    volume = QSlider(Qt.Vertical, window)
    volume.setGeometry(425, 75, 50, 50)
    volume.setMinimum(0)
    volume.setMaximum(100)
    volume.setValue(50)
    volume.setSingleStep(5)
    volume.hide()
    
    progressBar = QProgressBar(window)
    # progressBar.setMaximumSize(mixer.music.Sound.get_length())

    progressBar.setGeometry(75, 375, 350, 10)
    progressBar.setStyleSheet(
    "border: 2px solid #2196F3;"
    "border-radius: 5px;"
    "background-color: #E0E0E0;"
    )

    title = QLabel(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0],window)
    title.setGeometry(125, 25, 250, 70)
    title.setAlignment(Qt.AlignCenter)
    title.setWordWrap(True)
    title.setStyleSheet(
        "color: white;"
        "font-size: 20px;"
    )

    author = QLabel(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0],window)
    author.setGeometry(125, 100, 250, 30)
    author.setAlignment(Qt.AlignCenter)
    author.setWordWrap(True)
    author.setStyleSheet(
        "color: white;"
        "font-size: 15px;"
    )

    # year = QLabel(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]) ,window)
    # year.setGeometry(125, 135, 250, 25)
    # year.setAlignment(Qt.AlignCenter)
    # year.setWordWrap(True)
    # year.setStyleSheet(
    #     "color: white;"
    #     "font-size: 15px;"
    # )
    
    shuffle.clicked.connect(lambda: shuffleSong())
    play_pause.clicked.connect(lambda: playOrPause())
    previous.clicked.connect(lambda: previousSong())
    restart.clicked.connect(lambda: restartSong())
    next.clicked.connect(lambda: nextSong())
    speaker.clicked.connect(lambda: volumeHider())
    volume.valueChanged.connect(lambda: VolumeChanged(volume.value())) 

    def volumeHider():
        if volume.isHidden() == True: 
            volume.show()
        elif volume.isHidden() == False:
            volume.hide()

    def check_if_finished(var): # Threading makes it run constantly inside it loops 
        global shuffleStatus
        global currentSong
        while True:
            if status == "playing" and mixer.music.get_busy() == False: # Checks if the song is playing (Even though it's over) and the music mixer is off THIS MEANS THAT THE SONG IS DONE
                if shuffleStatus == False:
                    nextSong()
                elif shuffleStatus == True: 
                    shuffleSong()
                print(mixer.music.get_busy)
            # if mixer.music.get_busy():
            #     print('hi')
            #     get_mutagen(song_playlist + Music_Names[currentSong])
            #     print(SongData[0])
            #     print(SongData[1])
            #     print(SongData[2])
            time.sleep(1)
            


            if var.is_set(): 
                break
                
    event = threading.Event()
    thread = threading.Thread(target=check_if_finished, args=(event, )) # Creates the threading
    thread.start()

    def closer(event):
        event.set()

    def playOrPause():  
        global status
        
        if status == "playing":
            mixer.music.pause()
            title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0]) # Title
            author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0]) # Author
            # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0])) # year
            print('paused')
            status = "stopped"
            
        elif status == "stopped":
            mixer.music.unpause()
            title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0]) 
            author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
            # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
            print('unpaused')
            status = "playing"
            print(Music_Names[currentSong])



    def nextSong(): 
        global currentSong
        if shuffleStatus == True: 
            shuffler()
        else: 
            if currentSong > (len(Music_Names) - 2):
                currentSong = 0
            else: 
                currentSong += 1
            mixer.music.load(song_playlist + Music_Names[currentSong])
            mixer.music.set_volume(0)
            mixer.music.play()
            mixer.music.set_volume(0.5)
            if status == "playing":
                mixer.music.play()
                print(Music_Names[currentSong])
                title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
                author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
                # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
            else: 
                mixer.music.pause()
                title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
                author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0]) 
                # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
       


    def previousSong():
        global currentSong
        if shuffleStatus == True: 
            shuffler()
        else: 
            if currentSong == 0: 
                currentSong = len(Music_Names) - 1
            else: 
                currentSong -= 1

            mixer.music.load(song_playlist + Music_Names[currentSong])
            mixer.music.set_volume(0)
            mixer.music.play()
            mixer.music.set_volume(0.5)
            if status == "playing":
                mixer.music.play()
                print(Music_Names[currentSong])
                title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
                author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
                # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
            else: 
                mixer.music.pause()
                title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
                author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
                # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
            
    def restartSong():
        global currentSong

        mixer.music.load(song_playlist + Music_Names[currentSong])
        mixer.music.set_volume(0)
        mixer.music.play()
        mixer.music.set_volume(0.5)
        if status == "playing":
            mixer.music.play()
            print(Music_Names[currentSong])
            title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
            author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
            # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
        else: 
            mixer.music.pause()
            title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
            author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
            # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))

    def shuffleSong():
        global shuffleStatus

        if shuffleStatus == True: 
            shuffleStatus = False 
        elif shuffleStatus == False: 
            shuffleStatus = True
        
    def shuffler(): 
        global currentSong

        randomInt = random.randint(0,(len(Music_Names) - 1))
        if randomInt == currentSong: 
            randomInt = random.randint(0,(len(Music_Names) - 1))
        currentSong = randomInt
        mixer.music.load(song_playlist + Music_Names[currentSong])
        mixer.music.set_volume(0)
        mixer.music.play()
        mixer.music.set_volume(0.5)
        if status == "playing":
            mixer.music.play()
            print(Music_Names[currentSong])
            title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
            author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
            # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))
        else: 
            mixer.music.pause()
            title.setText(ID3(song_playlist + Music_Names[currentSong])['TIT2'].text[0])
            author.setText(ID3(song_playlist + Music_Names[currentSong])['TPE1'].text[0])
            # year.setText(str(ID3(song_playlist + Music_Names[currentSong])['TDRC'].text[0]))

    def VolumeChanged(volume):
        mixer.music.set_volume(volume/50)


    app.aboutToQuit.connect(lambda: closer(event))
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__': 
    main()  