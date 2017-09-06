from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from blog.models import Post, Comment, Tag


class PostResource(ModelResource):
	class Meta:
		queryset = Post.objects.all()
		resource_name = 'post'
		authentication = Authentication()
		authorization = Authorization()

class CommentResource(ModelResource):
	class Meta:
		queryset = Comment.objects.all()
		resource_name = 'comment'
		authentication = Authentication()
		authorization = Authorization()

class TagResource(ModelResource):
	class Meta: 
		queryset = Tag.objects.all()
		resource_name = 'tag'
		authentication = Authentication()
		authorization = Authorization()	        