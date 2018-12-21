import chatterbot
from chatterbot.trainers import ListTrainer
import os
import pyttsx3
from threading import Thread
import speech_recognition as sr

class ChatBot:
	def __init__(self):
		print("kora Chatbot activated!")

	def speak(self, text):
		engine = pyttsx3.init()
		engine.say(text)
		engine.runAndWait()

	def rec(self):
		r = sr.Recognizer()
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)
			try:
				return r.recognize_google(audio)
			except:
				print("Something went wrong...")
				return "ok"

	def chatting(self):
		bot = chatterbot.ChatBot('Bot')
		bot.set_trainer(ListTrainer)
		for files in os.listdir('data/'):
			data = open('data/' + files, 'r').readlines()
			bot.train(data)
		v = True
		while v:
			text = input("Your message: ")
			if text != "bye":
				replay = bot.get_response(text)
				self.speak(replay)
			else:
				print("kora Chatbot closed!")
				self.speak("goodbye")
				v = False