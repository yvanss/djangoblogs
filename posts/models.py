from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from django.utils import timezone
#from django.core.urlresolvers import reverse

#from django.utils.text import slugify 

# Create your models here.
# MVC MODEL CONTROLLER

def upload_location(instance, filename):
	#filebase, extension = filename.spilt(".")
	#return "%s/%s" %(instance.id, instance.id, extension)
	return "%s/%s" %(instance.id, filename)


class Post(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL, default= 1)
	title= models.CharField(max_length=120) #
	#slug = models.SlugField(unique=True)
	#slug = AutoSlugField(populate_from='title', unique_with='pub_date__month')
	image= models.ImageField(upload_to=upload_location,
		null=True,
		blank=True,
		width_field="width_field",
		height_field="height_field")
	height_field=models.IntegerField(default=0)
	width_field=models.IntegerField(default=0)
	content = models.TextField()
	draft= models.BooleanField(default=False)
	pubs=models.DateField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


	
	def __unicode__(self):
		return self.title


	def __str__(self):
		return self.title

	def get_absolute_url (self):
		#return reverse("post:detail",kwargs={"id": self.id})
		return "/posts/%s/"%(self.id)

	class Meta :
		ordering =["-timestamp", "-updated"]
