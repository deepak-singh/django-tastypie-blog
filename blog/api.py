from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie import fields
from blog.models import Post, Comment, Tag
from django.contrib.auth.models import User

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		authentication = Authentication()
		authorization = Authorization()

class CommentResource(ModelResource):
	class Meta:
		queryset = Comment.objects.all()
		resource_name = 'comment'
		authentication = Authentication()
		authorization = Authorization()


class TagResource(ModelResource):
	posts = fields.ToManyField('blog.api.PostResource', 'posts')
	class Meta: 
		queryset = Tag.objects.all()
		resource_name = 'tag'
		authentication = Authentication()
		authorization = Authorization()	    

class PostResource(ModelResource):
	author = fields.ForeignKey(UserResource, 'author')
	comments = fields.ToManyField(CommentResource, 'comments')
	tags = fields.ToManyField(TagResource, 'tags')
	class Meta:
		queryset = Post.objects.all()
		resource_name = 'post'
		authentication = Authentication()
		authorization = Authorization()

    