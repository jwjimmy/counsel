from django.test import TestCase, RequestFactory
from counselapp.utils import get_serialized_meta
import json

# Create your tests here.
class RequestMetaTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	# Set up a same origin request 
	def test_serialize_meta(self):
		request = self.factory.get('/requests/passive')
		get_serialized_meta(request.META)
