from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('Bot')
bot.set_trainer(ListTrainer)

#for files in os.listdir('data/'):
#	data = open('data/' + files, 'r').readlines()
#	bot.train(data)

print("Hello i am JARVIS, an AI chatbot. this is a demo and i m gonna be a lot smarter!")
print("start chatting...")

while True:
	message = input('You: ')
	if message != "bye":
		replay = bot.get_response(message)
		print('ChatBot: ',replay)
	else:
		print('ChatBot: goodbye!')
		break;