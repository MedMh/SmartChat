from django.shortcuts import render
from django.http import HttpResponse
from . import models
import pyttsx3
from threading import Thread
import speech_recognition as sr
import asyncio
import websockets
from .modules.chatbot.ChatBot import ChatBot

# Create your views here.

id_u = 0

def speak(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()

def rec():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		try:
			return r.recognize_google(audio)
		except:
			print("Something went wrong...")
			return "ok"


def sendMessage():
	engine = pyttsx3.init()
	ms = input("your message: ")
	#ms = rec()
	engine.say("your message is "+ms+", do you want me to send it?")
	engine.runAndWait()
	ans = input("answer: ")
	#ms = rec()
	if((ans == 'yes') or (ans == 'y')):
		msg = models.Message()
		msg.message = ms
		msg.sender_msg = id_u
		msg.receiver_msg = models.User.objects.filter(id = 2)[0]
		msg.save()
		print("sent")


async def sendCommand(websocket, path):
	c = 0
	p = ''
	async for message in websocket:
		engine = pyttsx3.init()
		if(c == 0):
			engine.say("Hello i am kora, this is the smart chat application. welcome.")
			engine.runAndWait()
			engine.say("sir now i will wait for your commands.")
			engine.runAndWait()
			c+=1
		print("waiting your commands...")
		msg = input("you: ")
		#msg = rec()
		print("command: "+msg)
		if((msg == 'write') or (msg == 'right')):
			engine.say("okay, what are you going to send?")
			engine.runAndWait()
			sendMessage()
			await websocket.send(msg)
		elif(msg == 'show contact list'):
			engine.say("loading the contact list...")
			engine.runAndWait()
			await websocket.send(msg)
		elif(msg == 'show user list'):
			engine.say("loading user list...")
			engine.runAndWait()
			await websocket.send(msg)
		elif(msg == 'show requests list'):
			engine.say("loading the requests...")
			engine.runAndWait()
			await websocket.send(msg)
		elif(msg == 'i am alone'):
			engine.say("okay, i am here to keep you company ...")
			engine.runAndWait()
			kora = ChatBot()
			kora.chatting()
		else:
			engine.say("sorry, i didn't understand your command")
			engine.runAndWait()
			await websocket.send(msg)


def runThread(id_u):
	l = asyncio.new_event_loop()
	asyncio.set_event_loop(l)
	l.run_until_complete(websockets.serve(sendCommand, 'localhost', 9000))
	l.run_forever()


def index(request):
	return render(request, 'chatting/index.html')

def signup(request):
	return render(request, 'chatting/SignUp.html')

def home(request):
	return render(request, 'chatting/home.html')

def createAccount(request):
	user = models.User()
	user.email = request.POST['email']
	user.nickname = request.POST['nname']
	user.f_name = request.POST['fname']
	user.l_name = request.POST['lname']
	user.password = request.POST['pwd']
	user.save()
	return render(request, 'chatting/index.html')

def login(request):
	mail = request.POST['mail']
	pwd = request.POST['pwd']
	users = models.User.objects.filter(email = mail)
	if(len(users)>0):
		c_user = users[0]
		if(c_user.password == pwd):
			request.session['user_id'] = c_user.id
			request.session['req_rec'] = '';
			request.session['msg_rec'] = '';
			id_u = c_user.id
			users_list = models.User.objects.exclude(email = mail)
			thr = Thread(target = runThread, args=[request.session['user_id']])
			context = {
				'user_list': users_list,
				'c_user': c_user,
				'thr': thr,
			}
			return render(request, 'chatting/home.html', context)
		else:
			#return HttpResponse("<h3> password incorrect! </h3>")
			return render(request, 'chatting/index.html')
	else:
		#return HttpResponse("<h3> email incorrect! </h3>")
		return render(request, 'chatting/index.html')

def getContacts(request):
	text = ''
	list_user = models.Contact.objects.filter(user = request.session['user_id'])
	if (len(list_user) > 0 ):
		for user in list_user:
			text = text+'<div style="display: flex;"><h3 style="margin-right: 10px;">'+user.nickname+' </h3></div><br>'
	else:
		text = text+'<h3> No Contacts </h3>'
	return HttpResponse(text)

def getUsers(request):
	text = ''
	list_user = models.User.objects.exclude(id = request.session['user_id'])
	for user in list_user:
		text = text+'<div style="display: flex;"><input id="userId" type="hidden" value="'+str(user.id)+'"><h3 style="margin-right: 10px;">'+user.nickname+' </h3><button onclick="sendRequest()" style="height: 30px; margin-top:20px;">send request</button></div><br>'
	return HttpResponse(text)

def getRequests(request):
	text = ''
	list_user = models.invitation.objects.filter(receiver_inv = request.session['user_id'])
	if (len(list_user) > 0 ):
		for user in list_user:
			text = text+'<div style="display: flex;"><h3 style="margin-right: 10px;">'+user.nickname+' </h3><button style="height: 30px; margin-top:20px;">accept</button><button style="height: 30px; margin-top:20px;">ignore</button></div><br>'
	else:
		text = text+'<h3> No requests </h3>'
	return HttpResponse(text)


def sendRequest(request):
	invt = models.invitation()
	print(request.POST.get('id_rec'))
	#invt.sender_inv = models.User.objects.filter(id = request.session['user_id'])[0]
	#invt.receiver_inv = models.User.objects.filter(id = int(idr))[0]
	#invt.state = 'w'
	#invt.save()
	print("invitation sent")
	return HttpResponse('')