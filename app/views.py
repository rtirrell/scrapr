from django import http, shortcuts
from django.utils import simplejson
import cgi
import re
import twitter


api = twitter.Api()
tag_re = re.compile(r'(#([0-9A-Za-z_]+))')
user_re = re.compile(r'(@[0-9A-Za-z_]+)')

def main(request):
  return shortcuts.render_to_response('scrapr/main.html', {})

def search(request):
  def format_tweet(tweet):
    tweet = tag_re.sub(r'<a href="http://twitter.com/#!/search/%23\2">\1</a>', tweet)
    tweet = user_re.sub(r'<a href="http://twitter.com/\1">\1</a>', tweet)
    return tweet
  
  q = request.POST.get('q')
  if q is None:
    return http.HttpResponseBadRequest()
  
  results = api.GetSearch(q, per_page = 100)
  response_data = {'results': []}
  tags = {}
  
  for result in results:
    result_dict = result.AsDict()
    print result_dict
    result_dict['formatted_tweet'] = format_tweet(result_dict['text'])
    print result_dict
    
    response_data['results'].append(result_dict)
    
    for tag_match in tag_re.finditer(result.text):
      name = tag_match.groups(1)[0]
      
      # See also collections.defaultdict in newer versions of python.
      if name in tags:
        tags[name] += 1
      else:
        tags[name] = 1
  
  response_data['tags'] = sorted(tags.items(), key = lambda kv: kv[1], reverse = True)
  return http.HttpResponse(simplejson.dumps(response_data), mimetype = 'application/json')
  
  

