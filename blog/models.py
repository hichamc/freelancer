from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os


class AccountManager(BaseUserManager):
	def create_user(self, email, password=None, **kwargs):
		if not email:
			raise ValueError('Users must have a valid email address.')

		if not kwargs.get('username'):
			raise ValueError('Users must have a valid username.')

		account = self.model(
			email=self.normalize_email(email), username=kwargs.get('username')
		)

		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, email, password, **kwargs):
		account = self.create_user(email, password, **kwargs)

		account.is_admin = True
		account.save()

		return account

# class Account(AbstractBaseUser, PermissionsMixin):
class Account(AbstractBaseUser):
	
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=40, unique=True)

	first_name = models.CharField(max_length=40, blank=True)
	last_name = models.CharField(max_length=40, blank=True)
	image = models.ImageField(null=True, blank=True, default="profile.png")

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.email

	def get_full_name(self):
		return ' '.join([self.first_name, self.last_name])

	def get_short_name(self):
		return self.first_name

	def has_perm(self, perm, obj=None):

		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, blog):

		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):

		# Simplest possible answer: All admins are staff
		return self.is_admin
	
	@property
	def is_superuser(self):
		return self.is_admin


class Project(models.Model):

	title = models.CharField(max_length=110)
	category = models.CharField(max_length=50, blank=True)
	descrip = models.TextField(blank=True)
	author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="projects")
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()
	
	def __str__(self):
		return self.title

class Review(models.Model):

	review_text = models.CharField(max_length=200)
	rating = models.DecimalField(decimal_places=2, max_digits=8, default=0)
	reviewed = models.ForeignKey(Account, related_name ='reviewed' ,on_delete=models.CASCADE)
	reviewer = models.ForeignKey(Account, related_name ='reviewer' ,on_delete=models.CASCADE)
	# reviewer = models.CharField(max_length=200)
	created_date = models.DateTimeField(default=timezone.now)

	def publish(self):
		self.published_date = timezone.now()
		self.save()
	
	def __str__(self):
		return self.review_text


class Bid(models.Model):

	bidder = models.ForeignKey(Account, on_delete=models.CASCADE)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_bids')
	amount = models.DecimalField(decimal_places=2, max_digits=6, default=0)
	descrip = models.TextField()	
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.bidder.username

class Category(models.Model):
	category_name = models.CharField(max_length=30)
	category_shortname = models.CharField(max_length=20)

	def __str__(self):
		return self.category_shortname

class Pimage(models.Model):
	image = models.ImageField(upload_to='portfolio')
	title = models.CharField(max_length=100, blank=True)
	thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
	user = models.ForeignKey(Account, related_name ='user_images' ,on_delete=models.CASCADE)
	

	# def __str__(self):
	# 	return self.imagefile.url


	