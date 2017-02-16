import json
import re
from ua_parser import user_agent_parser
import logging
logger = logging.getLogger('django.request')

class RequestType:
	UNKNOWN = 0
	DIRECT = 1
	GMAIL = 2
	GITHUB = 3

def get_request_type(meta):
	ua_string = meta.get("HTTP_USER_AGENT", None)
	http_referer = meta.get("HTTP_REFERER", None)
	ua_dict = user_agent_parser.ParseUserAgent(ua_string)

	if http_referer == None and ua_dict['family'] == 'GmailImageProxy':
		return RequestType.GMAIL
	elif http_referer == None and ua_dict['family'] == 'Other' and "github-camo" in ua_string:
		return RequestType.GITHUB
	elif http_referer:
		return RequestType.DIRECT
	else:
		logger.info("Could not get RequestType of " + ua_string)
		return RequestType.UNKNOWN

def quote_objects(meta_str):
	return re.sub(r".(?<=<)(.*?)(?=>).", r'"\1"', meta_str)

def get_serialized_meta(meta):
	return json.dumps(meta, cls=MetaEncoder)

def get_visit_dict(meta):
	visit_dict = {}
	meta_str = get_serialized_meta(meta)
	visit_dict['metadata'] = meta_str
	if 'HTTP_REFERER' in meta.keys():
		visit_dict['estate'] = meta['HTTP_REFERER']
	if 'HTTP_X_FORWARDED_FOR' in meta.keys():
		visit_dict['visitor'] = meta['HTTP_X_FORWARDED_FOR']
	return visit_dict

class MetaEncoder(json.JSONEncoder):
	def default(self, obj):
		try:
			return super(MetaEncoder, self).default(obj)
		except TypeError as e:
			return repr(obj)