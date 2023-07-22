import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
	
class Definition(models.Model):
	word = models.CharField(max_length=100)
	description = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='definitions')

	def __str__(self):
		return self.word

	def get_absolute_url(self):
		return reverse('definition-detail', kwargs={'pk': self.pk})
	
	def total_likes(self):
		return self.likes.count()
    

class Phrase(models.Model):
	content = models.CharField(max_length=200)

	def __str__(self):
		return self.content


class EnRuDictionary(models.Model):
	word_english = models.CharField(unique=True, max_length=50)
	word_russian = models.CharField(unique=True, max_length=50)
