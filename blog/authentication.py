from tastypie.authentication import ApiKeyAuthentication

class CreateUpdateApiKeyAuthentication(ApiKeyAuthentication):
	def is_authenticated(self, request, **kwargs):
		if request.method == "GET":
			return True
		else:
			return super(CreateUpdateApiKeyAuthentication, self).is_authenticated(request, **kwargs)
