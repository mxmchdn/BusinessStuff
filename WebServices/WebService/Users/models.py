from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='Grant-Thornton-Default.jpeg', upload_to='profile_img')
	powerbi = models.CharField(default='', max_length=200, blank=True)
	company = models.CharField(default='', max_length=25, blank=True)
	execution_left = models.IntegerField(default=0)
	table = models.CharField(default='', max_length=50, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)
