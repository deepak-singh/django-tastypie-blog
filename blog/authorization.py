from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

# Custom auth for no updates and deletes - for now.
class CustomAuthorization(Authorization):
	def update_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no updates.")

	def update_detail(self, object_list, bundle):
		raise Unauthorized("Sorry, no updates.")

	def delete_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no deletes.")

	def delete_detail(self, object_list, bundle):
		raise Unauthorized("Sorry, no deletes.")

class UserAuhtorization(CustomAuthorization):
	def read_list(self, object_list, bundle):
		# Only return my own records
		print(bundle.request.user.id)
		return object_list.filter(id=bundle.request.user.id)

	def read_detail(self, object_list, bundle):
		return bundle.obj.id == bundle.request.user.id

	def create_list(self, object_list, bundle):
		return object_list

	def create_detail(self, object_list, bundle):
		# Allow User creation by anyone. No Auth.
		return True

class PostAuthorization(CustomAuthorization):
	def read_list(self, object_list, bundle):
		return object_list

	def read_detail(self, object_list, bundle):
		return True

	def create_list(self, object_list, bundle):
		raise Unauthorized("Sorry, no multiple creation at once")

	def create_detail(self, object_list, bundle):
		# Allow creation
		return bundle.obj.author == bundle.request.user
