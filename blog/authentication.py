from tastypie.authentication import ApiKeyAuthentication

class ReadWithoutKeyAuthentication(ApiKeyAuthentication):
	def is_authenticated(self, request, **kwargs):
		if request.method == "GET":
			return True
		else:
			return super(ReadWithoutKeyAuthentication, self).is_authenticated(request, **kwargs)


class WriteWithoutKeyAuthentication(ApiKeyAuthentication):
	def is_authenticated(self, request, **kwargs):
		if request.method == "GET":
			return super(WriteWithoutKeyAuthentication, self).is_authenticated(request, **kwargs)
		else:
			return True

