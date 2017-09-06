from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
	name = models.CharField(max_length=50)	 	

	def __str__(self):
		return self.name

class Post(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
	published_date_time = models.DateTimeField(auto_now_add=True)
	header_image = models.CharField(max_length=300, null=True, blank=True)
	tags = models.ManyToManyField(Tag, related_name="posts")

	def __str__(self):
		return self.title

class Comment(models.Model):
	body = models.CharField(max_length=300)
	post = models.ForeignKey(Post, related_name="comments")
	user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
	
	def __str__(self):
		return self.body
