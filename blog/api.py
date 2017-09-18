from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from blog.authentication import WriteWithoutKeyAuthentication, ReadWithoutKeyAuthentication
from tastypie.authorization import Authorization
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.utils.timezone import now
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpNotFound
from tastypie import fields
from blog.models import Post, Comment, Tag
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from tastypie.exceptions import BadRequest
from django.db import IntegrityError
from blog.authorization import UserAuhtorization, PostAuthorization

class UserResource(ModelResource):
	# TO DO: Add some username and password validations
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		authentication = WriteWithoutKeyAuthentication()
		authorization = UserAuhtorization()
		fields = ['username', 'first_name', 'last_name', 'email', 'last_login']

	def obj_create(self, bundle, request=None, **kwargs):
		try:
			bundle = super(UserResource, self).obj_create(bundle)
			bundle.obj.set_password(bundle.data.get('password'))
			bundle.obj.save()
		except IntegrityError:
			raise BadRequest('Username already exists')

		return bundle

	def __get_api_key_for_user(self, user):
		return '%s' % (user.api_key.key)

	def prepend_urls(self):
		return [ url(r"^(?P<resource_name>%s)/login%s$" %
					(self._meta.resource_name, trailing_slash()),
					self.wrap_view('login'), name="api_login") ]


	def login(self, request, **kwargs):
		self.method_check(request, allowed=['post'])
		data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
		username = data.get('username', '')
		password = data.get('password', '')
		user = authenticate(username=username, password=password)
		if user and user.is_active:
			last_login = user.last_login
			login(request, user)
			return self.create_response(request, {
					'api_key': self.__get_api_key_for_user(user),
					'last_login': last_login,
					'username': username,
					'user_first_name': user.first_name
					})
		else:
			return self.create_response(request, {
				'success': False,
				'reason': 'Incorrect user name or password',
				}, HttpUnauthorized )



class CommentResource(ModelResource):
	class Meta:
		queryset = Comment.objects.all()
		resource_name = 'comment'
		authentication = ReadWithoutKeyAuthentication()
		authorization = Authorization()


class TagResource(ModelResource):
	posts = fields.ToManyField('blog.api.PostResource', 'posts')
	class Meta: 
		queryset = Tag.objects.all()
		resource_name = 'tag'
		authentication = ReadWithoutKeyAuthentication()
		authorization = Authorization()	    

class PostResource(ModelResource):
	author = fields.ForeignKey(UserResource, 'author')
	comments = fields.ToManyField(CommentResource, 'comments', null=True, blank=True)
	tags = fields.ToManyField(TagResource, 'tags', null=True, blank=True)
	class Meta:
		queryset = Post.objects.order_by('-published_date_time').all()
		resource_name = 'post'
		authentication = ReadWithoutKeyAuthentication()
		authorization = PostAuthorization()
		always_return_data = True

	def hydrate(self, bundle):
		bundle.data['author'] = bundle.request.user
		return bundle

	def dehydrate(self, bundle):
		bundle.data['author_name'] = bundle.obj.author.first_name	
		return bundle

