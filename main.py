import serial
import json
import os
import time
import pygame
from aiy.voice.tts import say
from aiy.voice.audio import AudioFormat, record_file_async

BASE_PATH = "/home/pi/radio/"

# init communication with arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

pygame.mixer.init()

menuPot = 0
menuSelection = -1
numberOfFiles = {}
menu = ["briseglaces", "services", "questions", "anecdotes"]
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
previousBtn = 0
startBtn = 0


def stop_playing():
	pygame.mixer.stop()
	pygame.mixer.music.unload()
	isPlaying = False

def play_file(filename):
	pygame.mixer.music.load(filname)
	pygame.mixer.music.play()

while True:
	dataString = ser.readline()
	#print dataString

	try:
		data = json.loads(dataString)

		########################################################################
		# start
		currentStartBtn = data['start']
		if startBtn != currentStartBtn:
			startBtn = currentStartBtn

			if startBtn == 1:
				stop_playing()
				play_file('menu/start.wav')

		########################################################################
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
			menuSelection = currentMenuSelection
			print("current menu: " + menu[menuSelection])

			stop_playing()
			play_file("menu/" + menu[menuSelection] + ".wav")

			index = 0

		########################################################################
		# playing
		currentPlayBtn = data['play']

		# on play button click
		if playBtn != currentPlaybtn:
			playBtn = currentPlayBtn

			# toggle play/pause state
			if playBtn == 1:
				isPlaying = not isPlaying

				if isPlaying:
					filename = menu[menuSelection] + '/' + str(index) + '.wav'
					play_file(filename)
				else:
					pygame.mixer.stop()

		# auto play next file
		if isPlaying and not pygame.mixer.music.get_busy():
				pygame.mixer.music.unload()
				index = min(index + 1, numberOfFiles[menu[menuSelection]])

				if index < numberOfFiles[menu[menuSelection]]:
					time.sleep(0.5)
					filename = menu[menuSelection] + '/' + str(index) + '.wav'
					play_file(filename)

		########################################################################
		# next
		currentNextBtn = data['next']

		# on next button click
		if nextBtn != currentNextBtn:
			nextBtn = currentNextBtn
			stop_playing()
			index = (index + 1) % numberOfFiles[menu[menuSelection]]
			filename = menu[menuSelection] + '/' + str(index) + '.wav'
			play_file(filename)

		########################################################################
		# previous
		currentPreviousBtn = data['previous']

		# on previous button click
		if previousBtn != currentPreviousBtn:
			previousBtn = currentPreviousBtn
			stop_playing()
			index = (index - 1 + numberOfFiles[menu[menuSelection]]) % numberOfFiles[menu[menuSelection]]
			filename = menu[menuSelection] + '/' + str(index) + '.wav'
			play_file(filename)

		########################################################################
		# recording
		recordBtn = data['record']

		# start recording
		if recordBtn == 1 and not isRecording:
			stop_playing()

			filename = menu[menuSelection] + '/' + str(numberOfFiles[menu[menuSelection]]) + '.wav'
			recorder = record_file_async(AudioFormat.CD, filename=filename, filetype='wav')
			numberOfFiles[menu[menuSelection]] = (numberOfFiles[menu[menuSelection]] + 1) % 10
			isRecording = True
			print 'recording'

		# end recording
		elif recordBtn == 0 and isRecording:
			recorder.terminate()
			isRecording = False
			print 'recording ended'

	except:
		print 'something went wrong'
		pass
