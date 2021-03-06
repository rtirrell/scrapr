from django import http, shortcuts
from django.utils import simplejson
from django.utils.html import urlize
from app.models import Tag
import re
import twitter

api = twitter.Api()

# Match hashtags ('#tag') in tweets. Note that there are two nested capture groups here, one that
# grabs the whole hashtag including the '#', and one that grabs only the text of the tag. 
tag_re = re.compile(r'(#([0-9A-Za-z_]+))')
# Match users ('@user') in tweets.
user_re = re.compile(r'(@[0-9A-Za-z_]+)')
def format_content(content):
  '''Markup the raw text of some content with links to users and hashtags.'''
    
  # '%23' is the percent-encoded version of '#'.
  content = tag_re.sub(r'<a href="http://twitter.com/#!/search/%23\2" class="tag">\1</a>', content)
  content = user_re.sub(r'<a href="http://twitter.com/\1">\1</a>', content)
    
  # Converts link-like text into an actual <a>.
  return urlize(content)

def main(request):
  '''Just renders the template.

	Django's generic views can also do this for you, see:
	http://docs.djangoproject.com/en/dev/ref/generic-views/.
	
	Note that there are two types of generics, the 'old' function-based ones, and a newer, more
	modular and extensible class-based version (Django 1.3+).
	'''
  if request.method != 'GET':
    return http.HttpResponseNotAllowed(['GET'])
  
  return shortcuts.render_to_response('app/main.html', {})

def search(request):
  '''Handles a search request, returning a JSON object (much like python's dictionary).'''
  
  if request.method != 'POST':
    return http.HttpResponseNotAllowed(['POST'])
  
  # Make sure that the view has the correct parameter - which is just 'q', the query. This cannot
  # be the empty string.
  q = request.POST.get('q')
  if not q:
    return http.HttpResponseBadRequest()
  
  # Fetch as many results as Twitter allows. python-twitter defaults to 15.
  results = api.GetSearch(q, per_page = 100)
  response_data = {'results': []}
  tags = {}
  
  # Convert each result to a python dictionary (suitable for serialization as JSON), and add a
  # 'formatted_tweet' key to each result, containing the anchor markup from 'format_tweet'.
  for result in results:
    result_dict = result.AsDict()
    result_dict['relative_created_at'] = result.relative_created_at
    result_dict['formatted_screen_name'] = format_content('@' + result_dict['user']['screen_name'])
    result_dict['formatted_tweet'] = format_content(result_dict['text'])
    
    response_data['results'].append(result_dict)
    
    # Find all tags in this tweet.
    for tag_match in tag_re.finditer(result.text):
      # Note that 'groups()' always returns a tuple, so we get the first (0th) element.
      name = tag_match.groups(1)[0]
      
      # Update our tag counts.
      # See also collections.defaultdict in newer versions of python.
      if name in tags:
        tags[name] += 1
      else:
        tags[name] = 1
  
  # Convert the tag dictionary to a list of two-tuples, filter out tags with count = 1, 
  # and sort it by the count descending.
  response_data['tags'] = sorted(
    [i for i in tags.items() if i[1] > 1], key = lambda kv: kv[1], reverse = True
  )
  return http.HttpResponse(simplejson.dumps(response_data), mimetype = 'application/json')
  
def tags(request):
  '''Handles GET (get tags) and POST (create tag).'''
  
  if request.method == 'POST':
    tag = request.POST.get('tag')
    if tag is None:
      return http.HttpResponseBadRequest()
    
    if Tag.objects.filter(name = tag).count() == 1:
      return http.HttpResponse(simplejson.dumps({'error': 'Not Unique'}), mimetype = 'application/json')
      
    # No duplication checking - let them have what they want.
    Tag.objects.create(name = tag)
    return http.HttpResponse()
  
  # Just dump every object in the db.
  elif request.method == 'GET':
    response_data = {'tags': []}
    for tag in Tag.objects.all():
      response_data['tags'].append(format_content(tag.name))
    return http.HttpResponse(simplejson.dumps(response_data), mimetype = 'application/json')
  
  # They tried a disallowed method - bad.
  else:
    return http.HttpResponseNotAllowed(['POST', 'GET'])
