from tastypie.authentication import ApiKeyAuthentication

class CreateUpdateApiKeyAuthentication(ApiKeyAuthentication):
	def is_authenticated(self, request, **kwargs):
		if request.method == "GET":
			return True
		else:
			return super(AnonymousPostAuthentication, self).is_authenticated(request, **kwargs)
