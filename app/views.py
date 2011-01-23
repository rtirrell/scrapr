from django import http, shortcuts
import simplejson
import twitter

api = twitter.Api()

def main(request):
  return shortcuts.render_to_response('scrapr/main.html', {})

def search(request):
  q = request.POST.get('q')
  if q is None:
    return http.HttpResponseBadRequest()
  
  results = api.GetSearch(q)
  response_data = {'results': []}
  for result in results:
    response_data['results'].append(result.text)
    
  
  return http.HttpResponse(simplejson.dumps(response_data), mimetype = 'application/json')
  
  

