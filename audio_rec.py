import pyaudio
import wave
import statistics
import numpy as np
import time
from time import gmtime
import noisereduce as nr
import collections

# ------------ Audio Setup ---------------
# constants
CHUNK = 1024 * 2             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 44100                 # samples per second
THRESHOLD = 100

# Signal range is -32k to 32k
# limiting amplitude to +/- 4k
AMPLITUDE_LIMIT = 8096
RECORD_SECONDS = 2.0

# pyaudio class instance
p = pyaudio.PyAudio()

# stream object to get data from microphone
stream = p.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	output=True,
	frames_per_buffer=CHUNK
)

def run(rec, init_time, frames, last_frames):
	while True:
		# binary data
		data = stream.read(CHUNK)  
		
		# Open in numpy as a buffer
		data_np = np.frombuffer(data, dtype='h')
		# data_np = nr.reduce_noise(y=data_np, sr=RATE)
		
		dataTime = gmtime()
		# stream.write(data)
        # if(data_np[-1] > THRESHOLD) and not rec:
		last_frames.append(data_np[-1])
		if not rec:
			print(data_np[-1])
			rec = True
			init_time = time.time()	
			print("---- GRAVACAO INICIADA ----")
		if rec:
			frames.append(data)
		if frames != [] and (time.time() - init_time) >= RECORD_SECONDS and (abs(statistics.median(last_frames)) < THRESHOLD):
			# wf = wave.open(str(init_time).replace('.', '-') + '_' + str(time.time()).replace('.', '-') + '.mp3', 'wb')
			wf = wave.open('audios/' + str(dataTime[0]) + str(dataTime[1]) + str(dataTime[2]) + '_' + str(dataTime[3]) + '-' + str(dataTime[4]) + '-' + str(dataTime[5]) + '.mp3', 'wb')
			wf.setnchannels(CHANNELS)
			wf.setsampwidth(p.get_sample_size(FORMAT))
			wf.setframerate(RATE)
			wf.writeframes(b''.join(frames))
			wf.close()
			frames = []
			print("---- GRAVACAO FINALIZADA ----")
			rec = False


if __name__ == '__main__':
	start_time = time.time()
	rec = False
	init_time = time.time()
	frames = []
	last_frames = collections.deque(maxlen=30)

	run(rec, init_time, frames, last_frames)