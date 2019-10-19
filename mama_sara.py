import speech_recognition as sr
import pyttsx3 as tts
import json
from rasa.nlu.model import Interpreter
from nutrition import Nutrition_Information


class Mama_Sara:

	def __init__(self):
		self.nlu_model = Interpreter.load('./models/current/nlu')
		self.r = sr.Recognizer()
		self.tts_engine = tts.init()
		with open("responses/responses.json", 'r') as f:
				self.responses = json.load(f)
		self.nutrition_information = Nutrition_Information(self.responses, self.tts_engine, self.nlu_model, self.r)

## Could change the voice.
# voices = tts_engine.getProperty('voices')
# tts_engine.setProperty('voice', voice.id)

	def converse(self):
		audio_string = ''
		while(audio_string.strip() != "stop"):

			with sr.Microphone() as source:
				print("Say something!")
				audio = self.r.listen(source)
			try:
				audio_string = self.r.recognize_sphinx(audio)
				print("Sphinx thinks you said " + audio_string + "\n")
				response = self.determine_response(audio_string)	
				self.tts_engine.say(response)
				self.tts_engine.runAndWait()

			except sr.UnknownValueError:
				print("Sphinx could not understand audio")
			except sr.RequestError as e:
				print("Sphinx error; {0}".format(e))

	def determine_response(self, input):

		print(self.nlu_model.parse(input))
		parsed_input = self.nlu_model.parse(input)
		if parsed_input["intent"]["name"] == "nutrition_information":

			response = self.nutrition_information.determine_response(parsed_input)
			print(response)
			return response
		else:
			return "I'm not sure what you mean"
			

if __name__ == "__main__":

	
	mama_sara = Mama_Sara()
	mama_sara.converse()
	# mama_sara.determine_response("My child is four months old what should they eat?")







