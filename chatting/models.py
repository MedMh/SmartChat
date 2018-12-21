from django.db import models

# Create your models here.

class User(models.Model):
	email = models.CharField(max_length = 250)
	nickname = models.CharField(max_length = 250)
	f_name = models.CharField(max_length = 250)
	l_name = models.CharField(max_length = 250)
	password = models.CharField(max_length = 250)

class Contact(models.Model):
	user = models.ForeignKey(User, related_name = 'user_name', on_delete = models.CASCADE)
	contact = models.ForeignKey(User, related_name = 'contact_name', on_delete = models.CASCADE)

class Message(models.Model):
	message = models.TextField()
	sender_msg = models.ForeignKey(User, related_name = 'sender_msg_name', on_delete = models.CASCADE)
	receiver_msg = models.ForeignKey(User, related_name = 'receiver_msg_name', on_delete = models.CASCADE)

class invitation(models.Model):
	state = models.CharField(max_length = 1)
	sender_inv = models.ForeignKey(User, related_name = 'sender_inv_name', on_delete = models.CASCADE)
	receiver_inv = models.ForeignKey(User, related_name = 'receiver_inv_name', on_delete = models.CASCADE)