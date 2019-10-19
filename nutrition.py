import speech_recognition as sr



class Nutrition_Information:

	def __init__(self, responses, tts_engine, nlu_model, r):
		self.months = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve']
		self.responses = responses
		self.tts_engine = tts_engine
		self.nlu_model = nlu_model
		self.r = r


	def determine_response(self, parsed_input):

		entities = parsed_input["entities"]

		entity = self.entity_finder("months", entities)
		print(entity)
		if not entity:
			months_old = self.query_additional_information('age')
		else:
			months_old = self.months.index(entity[0]['value'])
		print('absfdd')
		if months_old < 6:
			return self.responses["nutrition_information"]['6']
		if months_old < 9:
			return self.responses["nutrition_information"]['9']
		if months_old < 12:
			return self.responses["nutrition_information"]['12']
		if months_old < 24:
			return self.responses["nutrition_information"]['24']
			

	def query_additional_information(self, info):

		if info == 'age':
			return self.query_age()

	def query_age(self):
		audio_string = ''
		got_it = False
		while(got_it == False):

			self.tts_engine.say("How many months old is your child?")
			self.tts_engine.runAndWait()
			with sr.Microphone() as source:
				audio = self.r.listen(source)
			try:
				audio_string = self.r.recognize_sphinx(audio)
				print("Sphinx thinks you said " + audio_string + "\n")
				age = self.parse_age(self.nlu_model.parse(audio_string))

				if age != None:
					print("ayyayaya")
					return age

			except sr.UnknownValueError:
				print("Could you repeat that?")
				self.tts_engine.say("Could you repeat that?")
				self.tts_engine.runAndWait()

			except sr.RequestError as e:
				print("Sphinx error; {0}".format(e))

	def parse_age(self, parsed_input):
		entities = parsed_input["entities"]

		entity = self.entity_finder("months", entities)
		print(entity)
		if entity:
			return self.months.index(entity[0]['value'])
		else:
			return None

	def entity_finder(self, entity, entities):
		return list(filter(lambda x: x["entity"] == "months", entities))





