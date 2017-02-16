from django.test import TestCase, RequestFactory
from counselapp.utils import get_serialized_meta
from counselapp.utils import RequestType, get_request_type
import json

# Create your tests here.
class RequestMetaTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	# Set up a same origin request 
	def test_serialize_meta(self):
		request = self.factory.get('/requests/passive')
		get_serialized_meta(request.META)

class UserAgentTest(TestCase):
	def setUp(self):
		pass

	def test_iphone(self):
		meta = {}
		meta["HTTP_USER_AGENT"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
		meta["HTTP_REFERER"] = "bob.loblaw.com/hello"
		request_type = get_request_type(meta)
		self.assertEqual(request_type, RequestType.DIRECT)

	def test_gmail(self):
		meta = {}
		meta["HTTP_USER_AGENT"] = "Mozilla/5.0 (Windows NT 7.1; rv:16.0) Gecko Firefox/10.0 (via ggpht.com GoogleImageProxy)"
		request_type = get_request_type(meta)
		self.assertEqual(request_type, RequestType.GMAIL)

	def test_github(self):
		meta = {}
		meta["HTTP_USER_AGENT"] = "github-camo (n644qup0)"
		request_type = get_request_type(meta)
		self.assertEqual(request_type, RequestType.GITHUB)