import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
import os


class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self) -> str:
		return self.name

	
class Definition(models.Model):
	word = models.CharField(max_length=100)
	description = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='definitions')
	categories = models.ManyToManyField(Category, related_name='definitions')

	def __str__(self) -> str:
		return self.word

	def get_absolute_url(self):
		return reverse('definition-detail', kwargs={'pk': self.pk})
	
	def total_likes(self):
		return self.likes.count()
	
	def clean(self):

		if self.categories.count() > 5:

			raise ValidationError(
				"A definition can belong to at most five categories"
				)

