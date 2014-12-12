from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.

def File_file(self, filename):
	''' Dynamically create a path for the File.file based on
		the user that is uploading the file '''

	# Find the username based on who called me
	username = 'not-sure'
	if type(self) is File:
		username = self.project.owner.username
	elif type(self) is Project:
		username = self.owner.username

	url = "users/%s/files/%s" % (username, filename)
	return url


class Project(models.Model):
	name = models.CharField(max_length=100)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_projects')
	reviewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects_to_review')
	last_edit = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

	project_file = models.FileField(upload_to=File_file, null=True, blank=True)

	def __unicode__(self):
		return self.name;


class Language(models.Model):
	name = models.CharField(max_length=100)
	codemirror_mode = models.CharField(max_length=100)

	def __unicode__(self):
		return "[{}]: {}".format(self.id, self.name)


class File(models.Model):
	name = models.CharField(max_length=100)
	project = models.ForeignKey(Project, related_name='files')
	language = models.ForeignKey(Language, null=True, blank=True)
	file = models.FileField(upload_to=File_file)

	def __unicode__(self):
		return "[{}]: {} of {}".format(self.id, self.name, self.project.name)

	# Override the save method
	def save(self, *args, **kwargs):
		# You have a new file coming in, so do some logic and figure
		# out what language this file is.
		# And then, set the language and call save it.
		super(File, self).save(*args, **kwargs)


class Comment(models.Model):
	commentor = models.ForeignKey(settings.AUTH_USER_MODEL)
	file = models.ForeignKey(File, related_name='comments')
	line_number = models.IntegerField(default=1)
	text = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "[{}]: Comment on line {} of {}".format(self.id, self.line_number, self.file.name)


class ReviewRequest(models.Model):
	reviewer = models.ForeignKey(settings.AUTH_USER_MODEL)
	project = models.ForeignKey(Project)

	is_reviewed = models.BooleanField(default=False)
	is_read = models.BooleanField(default=False)

	date_created = models.DateTimeField(auto_now_add=True)
	date_completed = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return "[{}]: Reviewer ({}) for {}".format(self.id, self.reviewer.username, self.project.name)