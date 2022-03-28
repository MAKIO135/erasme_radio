import serial
import json
import os
import pygame
from aiy.voice.tts import say
from aiy.voice.audio import AudioFormat, record_file_async

BASE_PATH = "/home/pi/radio/"

# init communication with arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

pygame.mixer.init()

menuPot = 0
menuSelection = 0
numberOfFiles = {}
menu = ["annonces", "questions", "anecdotes", "services"]
for key in menu:
        numberOfFiles[key] = len(os.listdir(BASE_PATH + key))
print numberOfFiles


recordBtn = 0
isRecording = False
recorder = 0

index = 0
playBtn = 0
isPlaying = False

nextBtn = 0


while True:
        data_string = ser.readline()
        #print data_string

        try:
                data = json.loads(data_string)


                # menu
                menuPot = data['menu']
                currentMenuSelection = 0

                # potentiometer is returning values between 0 and 672
                if menuPot < 112: #annonces
                        currentMenuSelection = 0
                elif menuPot < 336: #questions
                        currentMenuSelection = 1
                elif menuPot < 560: #anecdotes
                        currentMenuSelection = 2
                else: #services
                        currentMenuSelection = 3

                if menuSelection != currentMenuSelection:
                        # stop playing
                        if isPlaying == True:
                                pygame.mixer.stop()
                                isPlaying = False

                        menuSelection = currentMenuSelection
                        print("current menu: " + menu[menuSelection])
                        #say(menu[menuSelection], lang='fr-FR', volume=5, speed=80)

                        filename = "menu/" + menu[menuSelection] + ".wav"
                        pygame.mixer.music.load(filename)
                        pygame.mixer.music.play()
                        isPlaying = True

                        index = 0


                # recording
                recordBtn = data['record']

                if recordBtn == 1 and not isRecording:
                        filename = menu[menuSelection] + '/' + str(numberOfFiles[menu[menuSelection]]) + '.wav'
                        recorder = record_file_async(AudioFormat.CD, filename=filename, filetype='wav')
                        numberOfFiles[menu[menuSelection]] = (numberOfFiles[menu[menuSelection]] + 1) % 10
                        isRecording = True
                        print 'recording'

                elif recordBtn == 0 and isRecording:
                        recorder.terminate()
                        isRecording = False
                        print 'recording ended'



                currentPlayBtn = data['play']
                if playBtn != currentPlaybtn:
                        if 
                        isPlaying = not isPlaying


                nextBtn = data['next']


                #print(playBtn, recordBtn, nextBtn, menuPot)

        except:
                print 'could not parse data_string'
                pass

