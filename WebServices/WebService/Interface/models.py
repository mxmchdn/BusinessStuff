from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

import magic

def validate_file(value):
	name = value.name.lower()
	list_ext = name.split('.')
	if len(list_ext) != 2 or not(list_ext[1].lower() in ['csv', 'txt']):
		raise ValidationError(u'Your are not allowed to upload this file type! Just .csv or .txt files')
	content = value.file.content_type
	if not(content == 'application/vnd.ms-excel' or content == 'text/plain'):
		raise ValidationError(u'Your are not allowed to upload this file type! Code injection protection')

class Post(models.Model):
	name = models.CharField(max_length=25, help_text=("~ Enter max 25 characters."))
	description = models.TextField(blank=True)
	file = models.FileField(upload_to='tables_inputs', help_text=("~ Upload .csv or .txt file, see About page for more informations!"), validators=[validate_file])
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	Services = [
		('TVA', 'TVA')
	]
	service = models.CharField(default='TVA', max_length=10, choices=Services, help_text=("~ Select for which service you want to upload a file."))
	output_file = models.FileField(default='default.csv')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('file-detail', kwargs={'pk': self.pk})
			
	def delete(self, *args, **kwargs):
		self.file.delete()
		if self.output_file != 'default.csv':
			self.output_file.delete()
		super().delete(*args, **kwargs)