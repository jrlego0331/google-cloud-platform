from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "WithGoogle/key.json"
speechClient = speech.SpeechClient()
filename = "File location"

with io.open(filename, 'rb') as audio_file:
    voicefile = audio_file.read()

inputAudio = types.RecognitionAudio(content=voicefile)
print("test1")
config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code='en-US')
print("config done")
answer = speechClient.recognize(config, inputAudio)
print("recog done")

for result in answer.results:
    print(u'Transcript: {}'.format(result.alternatives[0].transcript))
