import serial
import json
from aiy.voice.audio import AudioFormat, record_file_async

ser = serial.Serial('/dev/ttyACM0', 9600)

isRecording = 0

while True:
	dataString = ser.readline()
	print dataString

	try:
		data = json.loads(dataString)
		tmp = data['record']

                if tmp == 1 and not isRecording:
                        filename = 'record.wav'
                        recorder = record_file_async(AudioFormat.CD, filename=filename, filetype='wav')
                        isRecording = True
                        print 'recording'

                # end recording
                elif tmp == 0 and isRecording:
                        recorder.terminate()
                        isRecording = False
                        print 'recording ended'

        except:
                print 'something went wrong'
                pass



