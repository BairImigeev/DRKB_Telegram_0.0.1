
from pydub import AudioSegment

with open('voice.oga', 'rb') as file:
    sound = AudioSegment.from_file('voice.oga')
    sound.export("voice.wav", format="wav")