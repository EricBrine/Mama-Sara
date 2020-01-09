import argparse
import requests
import pyaudio
import scipy.io.wavfile as wav
import wave

class MamaSara:

    @staticmethod
    def text_bot():
        sender = input("What is your name?\n")

        message = ""
        while message != "stop":
            message = input("What's your message?\n")

            print("Sending message now...")

            r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"sender": sender, "message": message})
            print("Bot says, ")
            for i in r.json():
                print(f"{i['text']}")

        print("Bye, ", sender)

    @staticmethod
    def record_audio(WAVE_OUTPUT_FILENAME):
      CHUNK = 1024
      FORMAT = pyaudio.paInt16
      CHANNELS = 1
      RATE = 16000
      RECORD_SECONDS = 5

      p = pyaudio.PyAudio()

      stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

      print("* recording")

      frames = [stream.read(CHUNK) for i in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

      print("* done recording")

      stream.stop_stream()
      stream.close()
      p.terminate()

      wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
      wf.setnchannels(CHANNELS)
      wf.setsampwidth(p.get_sample_size(FORMAT))
      wf.setframerate(RATE)
      wf.writeframes(b''.join(frames))
      wf.close()

    def speech_bot(self):

        audio_string = ''
        while audio_string.strip() != "stop":

            # with sr.Microphone() as source:
            #     print("Say something!")
            #     audio = self.r.listen(source)
            # try:
            #     message = self.r.recognize_sphinx(audio)
            #     # message = "what should i feed my eight month old child"
            #     print("Sphinx thinks you said " + message + "\n")
            # except sr.UnknownValueError:
            #     print("Sphinx could not understand audio")
            # except sr.RequestError as e:
            #     print("Sphinx error; {0}".format(e))

            # print("Sending message now...")

            self.record_audio("audio.wav")

            audio_data = open('audio.wav', 'rb').read()
            message = requests.post('http://127.0.0.1:8341', data=audio_data,
                    headers={'Content-Type': 'application/octet-stream'}).json().get('message')

            print("I think you said: ", message)
            r = requests.post('http://localhost:5005/webhooks/rest/webhook',
                              json={"sender": "test", "message": message})

            print("Bot says, ")
            for i in r.json():
                print(i['text'])
                self.tts_engine.say(i['text'])
                self.tts_engine.runAndWait()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Mama Sara")
    parser.add_argument(
        "-m",
        "--mode",
        default="speech",
        help="Path to the model directory which contains "
             "sub-folders for core and nlu models.",
    )
    args = parser.parse_args()
    print(args.mode)
    mama_sara = MamaSara()
    if args.mode == "speech":
        mama_sara.speech_bot()
    elif args.mode == "text":
        mama_sara.text_bot()
    else:
        print("Invalid argument.")

