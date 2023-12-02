from RUTTS import TTS
from ruaccent import RUAccent


class NewsTts:
    def __init__(self):
        self.tts = TTS("TeraTTS/natasha-g2p-vits", add_time_to_end=0.8)
        self.accentizer = RUAccent(workdir="./model")
        self.accentizer.load(omograph_model_size='big_poetry', use_dictionary=True)

    def play_audio(self, audio):
        self.tts.play_audio(audio)

    def save_wav_of_tts(self, audio, file_name="temp.wav", save_path="./result/speech/"):
        full_path = save_path + file_name
        self.tts.save_wav(audio, full_path)

    def get_audio(self, text):
        stressed_text = self.accentizer.process_all(text)
        audio = self.tts(stressed_text, lenght_scale=1.2)
        return audio
