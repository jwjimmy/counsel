import json
import re

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